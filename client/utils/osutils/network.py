import os
import socket


UPNP_MSG_MAX_SIZE = 65536


def get_pc_ip(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((ip, 80))
    except:
        name = None
    else:
        name, *_ = s.getsockname()
    finally:
        s.close()
        return name


def is_pingable(tv_ip, timeout=3):
    pingc = "ping -c 1 -w {} {}".format(timeout, tv_ip)
    success = os.system(pingc) == 0
    return success


def _yield_from_socket(s):
    try:
        while True:
            yield s.recv(UPNP_MSG_MAX_SIZE)
    except socket.timeout:
        raise StopIteration
    except:
        raise


def send_upnp_request():
    multicast_ip, port = '239.255.255.250', 1900

    msg_s = (
        'M-SEARCH * HTTP/1.1\r\n'
        'HOST:{ip}:{port}\r\n'
        'ST:upnp:rootdevice\r\n'
        'MX:2\r\n'
        'MAN:"ssdp:discover"\r\n'
        '\r\n'
    ).format(ip=multicast_ip, port=port)
    msg = bytes(msg_s, 'utf-8')

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.settimeout(2)
    s.sendto(msg, (multicast_ip, port))

    output = list(_yield_from_socket(s))

    return output
