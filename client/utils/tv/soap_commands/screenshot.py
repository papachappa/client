from utils.tv import soap_commands


def enable(tv_ip):
    try:
        soap_commands.loshell(tv_ip, ' port option GfxScreenshots 1')
    except:
        RuntimeError('Unable to set port option GfxScreenshots 1')
