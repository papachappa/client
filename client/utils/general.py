import os
import re
import shlex
import subprocess

from pathlib import PurePath
from enum import Enum

from client.settings.development import TOOLS_DIR
from client.utils.osutils import proc


def replace_in_log(log_file, pattern, subst):
    log_file.seek(0)

    filedata = log_file.read()
    replace = pattern in filedata

    if replace:
        filedata = filedata.replace(pattern, subst)
        log_file.seek(0)
        log_file.truncate()
        log_file.write(filedata)

    return replace

def __get_cmd(interpreter, param):
    if isinstance(param, PurePath):
        param = param.as_posix()
    cmd_str = "{interpreter} {param}".format(
        interpreter=shlex.quote(interpreter),
        param=shlex.quote(param)
    )
    return shlex.split(cmd_str)


def start_serial_logger(logger, tv_ip, serial_log):
    if isinstance(logger, PurePath):
        logger = logger.as_posix()
    cmd = __get_cmd(logger, tv_ip)
    return proc.start_popen(cmd, serial_log)


def start_python(script, tv_ip, test_log, test_dir, p_settings, log_dir, *args, **kwargs):
    libs_dir = PurePath(test_dir, 'test_scripts', 'Libs')
    ui_lib_path = libs_dir / 'UI'
    fvp_lib_path = libs_dir / 'FVP'
    cam_lib_path = libs_dir / 'CAM_libs'

    os.environ["SOAP_UI_HOST"] = os.environ["TV_IP"] = tv_ip

    os.environ["PYTHON_LIB_PATH"] = ui_lib_path.as_posix()
    os.environ["PYTHON_LIB_PATH_FVP"] = fvp_lib_path.as_posix()
    os.environ["PYTHON_LIB_PATH_CIPLUS"] = cam_lib_path.as_posix()

    os.environ["TOOLS_DIR"] = TOOLS_DIR.as_posix()
    os.environ["LOGDIR_PATH"] = log_dir.as_posix()

    os.environ["STREAM_FILES"] = ';'.join(map(str, p_settings))

    cmd = __get_cmd('python3', script)
    return proc.start_popen(cmd, test_log)


def start_webiz(script, tv_ip, test_log, *args, **kwargs):
    os.environ["LMQR2_UDPHOST"] = "{}:12321".format(tv_ip)

    cmd = __get_cmd('WeBiz', script)
    return proc.start_popen(cmd, test_log)


def start_lstreamer(ini, player_log):
    cmd_str = (
        'lstreamer'
        ' --configfile {configfile}'
        ' --disable_numeric_progress 1 '
        ' --disable_dot_progress 1'
    ).format(configfile=shlex.quote(ini.as_posix()))

    cmd = shlex.split(cmd_str)
    p = proc.start_popen(cmd, player_log)
    try:
        p.wait(2)
    except:
        return p
    else:
        raise RuntimeError("Playback was not started after 2 sec of waiting")


def get_frame_app_dir(tv_software):
    # tv_software suppose to be string like [0-9].[0-9].[0-9].[0-9]#

    version_pattern = re.compile(r'^(\d+\.\d+)\.\d+\.\d+.*')
    version_match_ = re.match(version_pattern, tv_software)
    if not version_match_:
        raise RuntimeError("tv_software got from tv does not "
                            "look like [0-9].[0-9].[0-9].[0-9].* pattern")

    prepared_tv_version = version_match_.group(1).replace('.', '_')
    version_dir = list(TOOLS_DIR.glob('V{}*'.format(prepared_tv_version)))

    if not version_dir:
        raise RuntimeError("There is no directory matching "
                            "TV software version")
    if len(version_dir) > 1:
        raise RuntimeError("There is more than one directory with the same "
                            "TV software version")

    frame_app_dir = PurePath(version_dir[0], 'ci_apps', 'frame-app-runner')

    return frame_app_dir


def start_cam_emulator(tv_software, cam_log):
    frame_app_dir = get_frame_app_dir(tv_software)
    sslserver_path = frame_app_dir / "lmqtcpserver"

    os.environ["LMQR2_UDPHOST"] = ""
    os.environ["LMQR2_SSLSERVERPATH"] = sslserver_path.as_posix()
    os.environ["LD_LIBRARY_PATH"] = frame_app_dir.as_posix()
    os.environ["CICAM_APP_WORKING_DIR"] = frame_app_dir.as_posix()

    frame_app_runner = frame_app_dir / 'frame-app-runner'

    cmd_str = (
        '{runner}'
        ' -f libbifrost-emulator.so'
        ' -f libcicam-app.so'
    ).format(runner=shlex.quote(frame_app_runner.as_posix()))

    cmd = shlex.split(cmd_str)
    p = proc.start_popen(cmd, cam_log, stdin=subprocess.PIPE)
    try:
        p.wait(2)
    except subprocess.TimeoutExpired:
        return p
    except:
        raise
    else:
        raise RuntimeError("Cam emulator was not started after 2 sec of waiting")
