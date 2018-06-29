import os
import time
import subprocess
import requests

from pathlib import Path

from client.utils import general
from client.settings import WEBIZ_SCRIPTS_DIR
from client.utils.tv.soap_commands import get_sysinfo, check_connection
from client.utils.tv.soap_commands.soap_modules import loshell


WEBIZ_ERROR_MESSAGES = (
    'ERROR', 'TV update failed', 'cannot connect to X server'
)


def _execute_webiz_script(host, script_name, logfile):
    script_path = Path(WEBIZ_SCRIPTS_DIR, script_name)

    if not script_path.is_file():
        logfile.write("\n#Error: Can not find Webiz script. "
              "But main execution will be continued\n")
        return False

    try:
        p = general.start_webiz(script_path, host, logfile)
    except:
        return False
    else:
        # assuring tv updated
        p.wait(180)
        last_pos = logfile.tell()
        logfile.seek(0)

        is_failed = lambda x: any(map(lambda msg: msg in x, WEBIZ_ERROR_MESSAGES))
        failed = any(map(is_failed, logfile))

        logfile.seek(last_pos)

        return not failed


def _press_end_button(host, logfile):
    res = _execute_webiz_script(host, "press_button.html", logfile)
    if not res:
        logfile.write(
            "\nCan not connect to TV with WeBiz script or "
            "Webiz script return failure. Update window dialog appears\n"
        )


def _execute_tv_command(host, cmd):
    res = loshell.loshell(host, cmd)
    if not res:
        raise RuntimeError("Can not execute command")


def _is_tv_reboot_needed(func):
    def check_for_reboot(host, url, logfile):
        cmd = 'pckurl {}'.format(url)

        try:
            _execute_tv_command(host, cmd)
        except RuntimeError:
            logfile.write(
                "\nCommand {} returned fail. "
                "Need to restart tv\n".format(cmd)
            )

            _execute_tv_command(host, 'restarttv 0')

            logfile.write("\nWaiting for TV's reboot...\n")
            time.sleep(50)

            _execute_tv_command(host, cmd)

        return func(host, url, logfile)
    return check_for_reboot


def _update(host, logfile):
    logfile.write("\nStart to update TV...\n")

    res = _execute_webiz_script(host, "get_update_status.html", logfile)
    if not res:
        logfile.write("\nProblems occurred, depends on Webiz fail"
                      " or other problems, tv update may continue\n")
        return False

    logfile.write("\nWait for TV's reboot after successful update\n")
    time.sleep(70)
    _press_end_button(host, logfile)

    try:
        version = get_tv_version(host)
    except RuntimeError:
        return False
    else:
        logfile.write("\nVersion after update {}\n".format(version))
        return True


def is_avail_for_update(host, url, logfile):
    tv_avail = check_connection.check_availability(host)
    if not tv_avail:
        logfile.write("\nTV is not available\n")
    file_avail = check_file_availability(url, logfile)
    return tv_avail, file_avail


def update_tv(host, url, logfile):
    tv_avail, file_avail = is_avail_for_update(host, url, logfile)

    if not (tv_avail and file_avail):
        return False

    res = exec_update_tv(host, url, logfile)    
    return res


def get_tv_version(host):
    try:
        chassis = get_sysinfo.getInfo(host)
        tv_firmware = chassis['package']
    except KeyError:
        raise RuntimeError(
            "#Error of getting info from TV. "
            "Probably not all services have started")
    else:
        return tv_firmware[:-1]


def tv_has_same_version(host, to_be_ver):
    current_ver = get_tv_version(host)
    return current_ver in to_be_ver


@_is_tv_reboot_needed
def exec_update_tv(host, url, logfile):
    ver = tv_has_same_version(host, url)

    if ver:
        logfile.write(
            "\nTV already has this version installed. "
            "No need to update\n"
        )
        return True

    try:
        _execute_tv_command(host, 'pckupdatep')
    except RuntimeError:
        # Expect only RuntimeError exception, other will be intercepted in
        # modules
        pass
    finally:
        return _update(host, logfile)


def check_file_availability(url, logfile):
    try:
        req = requests.head(url, allow_redirects=True, timeout=10)
        req.raise_for_status()
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        logfile.write("\n#Connection error occured. Server unavailabile\n")
        return False
    except requests.exceptions.HTTPError:
        logfile.write("\n#Error. File not found on server\n")
        return False
    else:
        return req.status_code == 200
