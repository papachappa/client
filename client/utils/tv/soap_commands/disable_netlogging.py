from utils.tv import soap_commands


def turnLogOff(client, server):
    try:
        clientId = soap_commands.connectFi(client)
    except Exception:
        raise

    request = soap_commands.DisableNetlogging(client, clientId, server)
    return request.getResponse()
