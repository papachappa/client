import re

from utils.tv import soap_commands


def clear_dubug_levels(ip):
    try:
        test_result = soap_commands.loshell(ip, 'debug_clear all')
    except:
        raise
    if not test_result:
        return False
    return True


def set_log_level(host, cmd):
    client_id = soap_commands.connectFi(host)
    set_level_request = soap_commands.ControlDebug(host, client_id, cmd)
    return set_level_request.getResponse()


def set_dubug_level(module, level, ip):
    cmd  = " ".join(["debug_level", module, level])
    try:
        setLevelRes = set_log_level(ip, cmd)
    except:
        raise
    
    if setLevelRes.startswith('err'):
        raise NameError("Unknown debug level")
    else:
        resultLvl = re.findall("%s\s\(\slevel:(.{3})" % module, setLevelRes)
        if len(resultLvl) < 2:
            raise RuntimeError("Unknown module")
        elif resultLvl[-1] != level:
            raise AssertionError("Not expected level")
