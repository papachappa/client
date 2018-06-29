import time
from pathlib import Path

from client.settings import CAM_LOG_FILE
from client.utils import general
from client.utils.tv.nonsoap_commands import ping
from client.utils.tv.soap_commands import get_last_wakeupreason

from .startscriptmixin import StartScriptMixin


class DCMMonitorMixin(StartScriptMixin):
    """ Mixin for executing TV DCMMonitoring while TV is in sleeping state.
        Getting and analyzing wake up reason and execute cam log script
        if necessary.
    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._tvip = None
        self._log_dir = None
        self._test_dir = None
        self._player_settings = None
        self._test_script = None
        self._timeout = None
        self._libs_dir = params.libs_dir
        self._utils_dir = params.utils_dir
        self.__timejump_script = Path(self._utils_dir, "DCMTimeJumpControl.html")
        self.__get_camlog_script = Path(self._libs_dir, 'CAM_libs', "get_cam_log.py")
        self.__wait_time = 10

    def dcm_monitor(self):
        while self._timeout:
            if self._timeout % 60 == 0:
                self._testlog('\n#INFO: DCM monitor timeout: '+str(self._timeout))

            if ping.check_ip(self._tvip, 1):
                self._testlog('TV woke up')
                reason = self._get_last_wakeupreason()

                if not self._is_reason_got(reason):
                    continue

                if not self._alarm_reason(reason):
                    self._testlog("Wait while TV goes to standby...")
                    while ping.check_ip(self._tvip, 1):
                        time.sleep(0.5)
                        self._timeout -= 1
                    self._testlog('TV in standby state')
                    continue

                return

            self._timeout -= 1

        raise RuntimeError('Timeout was occurred. TV did not wake up')

    def _get_last_wakeupreason(self):
        for tryn in range(10):
            self._testlog('Attempt: {} to get wakeup reason.'.format(tryn))

            time.sleep(self.__wait_time)
            self._timeout -= self.__wait_time

            try:
                reasons = get_last_wakeupreason.getReasons(self._tvip)
            except:
                pass
            else:
                if reasons:
                    return reasons.rsplit(';', 1)[-1]

        return None

    def _is_reason_got(self, reason):
        if reason:
            self._testlog('Wake up reason: {}'.format(reason))
            return True

        if not ping.check_ip(self._tvip):
            return False

        raise RuntimeError('Woke up reason was not got')

    def _alarm_reason(self, reason):
        if reason != 'night-update':
            self._testlog('TV woke by not DCM reason, test can be continued.')
            return True

        # for CIPlus execute python get_cam_log.py
        is_camlog_script = "camlog" in self._test_script.name

        if is_camlog_script:
            self.exec_get_camlog_script()

        self._testlog('DCM is on. Wait for standby')
        try:
            self.start_test_script('WeBiz', self.__timejump_script, 30)
        except:
            raise

        if is_camlog_script:
            self.exec_get_camlog_script()

        return False

    def exec_get_camlog_script(self):
        self._testlog("#INFO Getting cam log...")
        with CAM_LOG_FILE.open('a+', 1) as cam_log_fd:
            try:
                p = general.start_python(
                    self.__get_camlog_script, self._tvip, cam_log_fd, self._test_dir,
                    self._player_settings, self._log_dir
                )
            except Exception as e:
                raise RuntimeError(
                    'Cam log script was not started. Reason: {}'.format(e)
                )

        try:
            res = p.wait(180)
        except:
            p.terminate()
            self._testlog('#WARN: Cam log script timed out')
        else:
            if res != 0:
                self._testlog('#WARN: Cam log script return non zero exit code')

        self._testlog("#INFO: Finished getting cam log")

    def remove_camlog_file(self):
        try:
            CAM_LOG_FILE.unlink()
        except OSError:
            pass
