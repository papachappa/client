from pathlib import PurePath

from client.utils.osutils import ssh


def find_dumps(tv_ip):
    find_files = r"find /mnt/ -name *.core"

    try:
        client = ssh.ssh_connect(tv_ip)
        _, files, _ = client.exec_command(find_files, timeout=10)
    except:
        raise
    else:
        files = files.read().decode()
    finally:
        client.close()

    return files.split()


def clear_dumps(tv_ip, path):
    if isinstance(path, PurePath):
        path = path.as_posix()

    cmd = r"rm -rf {}".format(path)

    try:
        client = ssh.ssh_connect(tv_ip)
        _, stdout, _ = client.exec_command(cmd, timeout=10)
    except:
        raise
    else:
        stdout = stdout.read().decode()
    finally:
        client.close()

    return stdout


def get_dumps(tv_ip, remote_path_file, local_path_file):
    if isinstance(remote_path_file, PurePath):
        remote_path_file = remote_path_file.as_posix()
    if isinstance(local_path_file, PurePath):
        local_path_file = local_path_file.as_posix()

    try:
        ssh.get_file(tv_ip, remote_path_file, local_path_file)
    except:
        raise
