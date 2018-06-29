from client.utils.osutils import ssh
from client.utils.osutils import network

def ping_resource(tv_ip, resource):
    # grep package percentage lost
    cmd = r"ping -c 5 -q {} | sed -n 's/.*\s\([0-9]\+\)%.*/\1/p'".format(resource)

    try:
        client = ssh.ssh_connect(tv_ip)
        _, stdout, _ = client.exec_command(cmd, timeout=10)
    except:
        raise
    else:
        p = stdout.read().decode()
        if not p:
            raise RuntimeError('Bad Address')

    finally:
        client.close()

    return int(p)

def check_ip(ip, timeout=3):
    is_pingable = network.is_pingable(ip, timeout)
    return is_pingable
