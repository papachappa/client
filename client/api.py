import os
import subprocess
from pathlib import Path
from datetime import datetime

import requests

from client import __version__
from settings import TESTS_DIR, LOGS_DIR, TV_FIRMWARE_URI, UTIL_LOGS_DIR
from client.constants import CHASSIS_LIST
from client.controllers import strategy, TestResult, ControllerParams
from utils.tpstation import modulators, power_sockets
from utils.tv.nonsoap_commands import firmware_update, upnp


def get_log(run_name, nkey, log_type, last_pos=0, rsize=8192):
    """
    rsize=8192 for utf-8 gives in worst case 8192*4 bytes ~ 32KB
    """
    version, *suites, step = nkey.split('.', maxsplit=nkey.count('.') - 2)
    log_dir = Path(LOGS_DIR, version, run_name, *suites)
    
    path_to_log = Path(log_dir, '{}_{}.log'.format(step, log_type))

    last_pos = int(last_pos)
    rsize = int(rsize)
    result = {'status': None, 'data': {'last_pos': last_pos}, 'EOF': False}
    try:
        with path_to_log.open('r') as f:
            if last_pos != 0:
                f.seek(last_pos, os.SEEK_SET)
            res = f.read(rsize)
            last_pos = f.tell()
            result['EOF'] = f.read(1) == ''

        status = 'OK'
        data = {'text': res, 'last_pos': last_pos}
    except (OSError, IOError) as e:
        status = 'Failed'
        data = {'text': 'File not found', 'type': type(e).__name__,
                'date': datetime.now().strftime('[%Y/%M/%d %H:%m:%S]')}
    except Exception as e:
        status = 'Failed'
        data = {'text': 'Unknown error', 'type': type(e).__name__,
                'date': datetime.now().strftime('[%Y/%M/%d %H:%m:%S]')}
    finally:
        result['status'] = status
        result['data'].update(data)

    return result


def start_test(**kwargs):
    result = TestResult()

    try:
        Step = strategy.controller_choice(**kwargs)
    except Exception as err:
        result.detailed_result = str(err)
        return result

    nkey = kwargs['nkey']
    version, *suites, _ = nkey.split('.', maxsplit=nkey.count('.') - 2)
    run_name = kwargs.pop('run_name', None)

    test_dir = Path(TESTS_DIR, version)
    log_dir = Path(LOGS_DIR, version, run_name, *suites)
    log_dir.mkdir(parents=True, exist_ok=True)

    params = ControllerParams(test_dir=test_dir, log_dir=log_dir, **kwargs)
    try:
        with Step(params, **kwargs) as step:
            step.run_the_test(**kwargs)
            result = step.result
    except Exception as err:
        result.detailed_result = str(err)
    finally:
        return result


def get_station_info():
    subproc = lambda cmd: subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    dta_p = subproc('lspci -v | grep -i "kernel driver in use: dta" -c')
    dtu_p = subproc('lsusb -v | grep -i dtu -c')

    dta_count, _ = dta_p.communicate()
    dtu_count, _ = dtu_p.communicate()

    result = {
        'DTA': int(dta_count),
        'DTU': int(dtu_count),
        'version': __version__,
    }
    return result


def get_firmwares(timeout_per_request=5):
    res = dict()
    for chassis in CHASSIS_LIST:
        url = requests.compat.urljoin(TV_FIRMWARE_URI, chassis)
        r = requests.get(url, timeout=timeout_per_request)
        if r.status_code != requests.codes.ok:
            raise RuntimeError("Bad request. Status code: %s" % r.status_code)
        result = r.json()
        res[chassis] = [x['name'] for x in result if x['type'] == 'file']
    return res


def update_tv_firmwares(host, chassis, file_name, run_name=None):
    run_name = run_name or datetime.now().strftime("%Y%m%d_%H%M%S")
    log_name = 'update_tv_firmware.log'

    log_dir = Path(UTIL_LOGS_DIR, run_name)
    log_path = log_dir / log_name

    log_dir.mkdir(parents=True, exist_ok=True)

    url = requests.compat.urljoin(TV_FIRMWARE_URI, '{}/{}'.format(chassis, file_name))
    with log_path.open('w+', 1) as file_:
        firmware_update.update_tv(host, url, file_)


def reconnect_mods(run_name=None):
    run_name = run_name or datetime.now().strftime("%Y%m%d_%H%M%S")
    log_name = 'reconnect_mods.log'

    log_dir = Path(UTIL_LOGS_DIR, run_name)
    log_path = log_dir / log_name

    log_dir.mkdir(parents=True, exist_ok=True)

    with log_path.open('w+', 1) as file_:
        modulators.reconnect_mods(file_)


def socket_manipulation(cmd, socket):
    result = power_sockets.socket_manipulation(cmd, socket)
    return result


def get_available_tv():
    result = upnp.get_tv_upnp_list()
    return result
