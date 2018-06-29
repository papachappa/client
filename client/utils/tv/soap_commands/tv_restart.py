from utils.tv import soap_commands


def tv_restart(ip, chassis):
    if 'HL' in chassis:
        command = 'pwc_restarttv'
    elif 'SL220' in chassis:
        command = 'iic 2 "<B0 1B 00 00 01>"'
    elif 'SL' in chassis:
        command = 'pwc_restarttv'
    elif 'Mizar' in chassis:
        command = 'restarttv 1'
    else:
        raise RuntimeError("No such chassis name")

    return soap_commands.loshell(ip, command)
