from utils.tv import soap_commands


def deleteExceptions(host):
    try:
        clientId = soap_commands.connectFi(host)
    except:
        raise
    request = soap_commands.DeleteExceptionItems(host, clientId)
    return request.getResponse()
