import time
from .interface import RequestAccess
from socket import error
class FIError(Exception):
    pass

def connectFi(ipv4):
    """Connect to factory interface and return clientId. """
    request_access = RequestAccess(ipv4)
    try:
        answer = request_access.getResponse()
    except error as e:
        raise FIError('Connection to %s is timed out' % ipv4)
    # This is simplified and assumes, that access will be granted.
    if answer == 'Pending':
        time.sleep(2)
        clientId = request_access.getResponse()
        pos = clientId.find('LRemoteClient')
        if pos == -1:
            raise FIError("Couldn't connect to %s" % ipv4)
    else:
        clientId = answer
    return clientId

