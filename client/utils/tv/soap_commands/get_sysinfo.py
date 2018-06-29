from utils.tv import soap_commands


def getInfo(host):
    try:
        clientId = soap_commands.connectFi(host)
    except Exception:
        raise

    sysInfoRequest = soap_commands.GetSystemInfo(host, clientId)
    return sysInfoRequest.getResponse()
