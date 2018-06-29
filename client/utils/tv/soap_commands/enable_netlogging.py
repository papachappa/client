from utils.tv import soap_commands


def turnLogOn(client, server):
    try:
        clientId = soap_commands.connectFi(client)
    except Exception:
        raise

    request = soap_commands.EnableNetlogging(client, clientId, server)
    return request.getResponse()
