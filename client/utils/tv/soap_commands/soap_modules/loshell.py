from .interface import RequestAccess, Loshell
from .ficom import connectFi, FIError

def loshell(host, cmd):
    try:
        clientId = connectFi(host)
    except FIError as e:
        raise e

    loshellRequest = Loshell(host, clientId, cmd)
    res = loshellRequest.getResponse()
    if res == 'ok':
        return True
    else:
        return False

