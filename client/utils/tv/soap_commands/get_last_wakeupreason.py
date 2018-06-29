from utils.tv import soap_commands


def getReasons(host):
    try:
        clientId = soap_commands.connectFi(host)
    except:
        raise
    wakeupReasonsRequest = soap_commands.GetWakeupReasons(host, clientId)
    return wakeupReasonsRequest.getResponse()
