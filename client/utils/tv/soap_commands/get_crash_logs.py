from utils.tv import soap_commands


def getList(host):
    try:
        clientId = soap_commands.connectFi(host)
    except:
        raise
    exceptionList = soap_commands.GetExceptionList(host, clientId)
    return exceptionList.getResponse()

def getException(host, exceptionID):
    try:
        clientId = soap_commands.connectFi(host)
    except:
        raise
    exceptionItem = soap_commands.GetExceptionItem(host, clientId, exceptionID)
    return exceptionItem.getResponse()
