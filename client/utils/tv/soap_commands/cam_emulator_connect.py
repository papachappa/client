from utils.tv import soap_commands


def cam_emulator_connect(host, server_ip):
    command = 'cam_emulator 0 ' + server_ip
    try:
        res = soap_commands.loshell(host, command)
    except:
        raise
    return bool(res)
