from utils.tv import soap_commands


def check_availability(host):
    try:
        soap_commands.connectFi(host)
    except soap_commands.FIError:
        return False
    else:
        return True
