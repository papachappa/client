from utils.tv import soap_commands


def debug_show(client):
    try:
        soap_commands.loshell(client, 'debug_show')
    except:
        return False
    else:
        return True
