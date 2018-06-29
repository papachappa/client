from utils.tv.soap_commands import get_sysinfo


def get_chassis_info(tv_ip):
    try:
        chassis = get_sysinfo.getInfo(tv_ip)
    except:
        raise
    else:
        tv_chassis = chassis.get('ChassisName')
        tv_software = chassis.get('package')

    if not (tv_chassis and tv_software):
        raise Exception("Can not get 'ChassisName' or 'package'")

    # remove & at the end
    if tv_software and isinstance(tv_software, str):
        tv_software = tv_software[:-1]

    return tv_chassis, tv_software
