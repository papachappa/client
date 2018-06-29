from pathlib import PurePath

import paramiko
from scp import SCPClient


_TV_USERNAME = 'root'
_TV_PASSWORD = ''


def ssh_connect(tv_ip):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(tv_ip, 22, _TV_USERNAME, _TV_PASSWORD, timeout=10)
    except Exception as e:
        raise RuntimeError(*e.args)
    else:
        return client


def get_file(tv_ip, remote_path_file, local_path_file):
    if isinstance(remote_path_file, PurePath):
        remote_path_file = remote_path_file.as_posix()
    if isinstance(local_path_file, PurePath):
        local_path_file = local_path_file.as_posix()

    client = ssh_connect(tv_ip)
    try:
        scp = SCPClient(client.get_transport())
        scp.get(remote_path_file, local_path=local_path_file)
    except Exception as e:
        raise RuntimeError(*e.args)
    finally:
        scp.close()
        client.close()


def remove_file(tv_ip, remote_file):
    if isinstance(remote_file, PurePath):
        remote_file = remote_file.as_posix()

    cmd = r"rm -f {}".format(remote_file)

    client = ssh_connect(tv_ip)
    try:
        client.exec_command(cmd, timeout=10)
    except:
        raise
    finally:
        client.close()
