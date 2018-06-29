from celery import shared_task
from celery_once import QueueOnce

from client import settings
from celeryapp import app
import api


ERR_STATUS = 'ERROR'


@app.task(base=QueueOnce, name='start_test')
def start_test(*args, **kwargs):
    rval = {'status': ERR_STATUS, 'detailed_result': 'unknown error'}
    try:
        rval = api.start_test(**kwargs)
    except Exception as e:
        raise e
        rval = {'status': ERR_STATUS, 'detailed_result': str(e)}
    else:
        rval = rval.to_dict()
    # finally block sometimes leads to celery backend error:
    # undefined reference
    return rval


@app.task(name='get_log')
def get_log(run_name, step_nkey, log_type, last_pos):
    return api.get_log(run_name, step_nkey, log_type, last_pos)


@app.task(name='get_station_info')
def get_station_info():
    return api.get_station_info()


@app.task(name='get_tv_firmware')
def get_tv_firmware():
    return api.get_firmwares()


# TODO: pass run_name
@app.task(name='update_tv_firmware')
def update_tv_firmware(host, chassis, file_name):
    result = {'status': ERR_STATUS, 'detailed_result': 'unknown error'}

    try:
        api.update_tv_firmwares(host, chassis, file_name)
    except Exception as e:
        result['detailed_result'] = str(e)
    else:
        result['status'] = 'OK'
        result['detailed_result'] = None

    return result


# TODO: pass run_name
@app.task(name='reconnect_mods')
def reconnect_mods():
    result = {'status': ERR_STATUS, 'detailed_result': 'unknown error'}

    try:
        api.reconnect_mods()
    except Exception as e:
        result['detailed_result'] = str(e)
    else:
        result['status'] = 'OK'
        result['detailed_result'] = None

    return result


@app.task(name='socket_manipulation')
def socket_manipulation(cmd, socket):
    result = {'status': ERR_STATUS, 'detailed_result': 'unknown error'}

    try:
        rval = api.socket_manipulation(cmd, socket)
    except Exception as e:
        result['detailed_result'] = str(e)
    else:
        result['status'] = 'OK'
        result['detailed_result'] = rval

    return result

@app.task(name='get_available_tv')
def get_available_tv():
    result = {'status': ERR_STATUS, 'detailed_result': 'unknown error'}

    try:
        rval = api.get_available_tv()
    except Exception as e:
        result['detailed_result'] = str(e)
    else:
        result['status'] = 'OK'
        result['detailed_result'] = rval

    return result
