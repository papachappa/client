from client.constants import TEST_STATUS
from client.utils import general
from client.utils.tv.nonsoap_commands import ping

from client.controllers import Controller
from client.mixins import (CheckTestFilesMixin, DCMMonitorMixin,
                            PlaybackMixin, PreconPlaybackMixin,
                            ParseTestLogMixin, TPSLoggingMixin, TVStandbyMixin)


class ControllerForCIPlusNightDCM(Controller,
                                  DCMMonitorMixin,
                                  CheckTestFilesMixin,
                                  PlaybackMixin,
                                  PreconPlaybackMixin,
                                  TVStandbyMixin,
                                  TPSLoggingMixin,
                                  ParseTestLogMixin,
                                  ):
    """
       ControllerForCIPlusNightDCM
       1. Execute precondition webiz script(_ciprecondition.*) like
          initial scan. If "PASSED" execute main script and exit from
          controller, else execute
          NightDCM controller and finally execute main last WeBiz script
          like check service list.
          Fields in gdoc:
          controller=for_ci_plus_nightdcm
          interpreter=python
          timeout=10
          standbymin=10
    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        self._timeout = params.timeout
        self._interpreter = params.interpreter
        self._test_step_patern = params.test_step_patern
        self._testscript_pattern = '.*'
        self._preconscript_pattern = '_ciprecondition.*'

        self._serial_log_setting = params.serial_log_setting
        self._player_settings = params.player_settings

        self._utils_dir = params.utils_dir
        self._confirm_wakeup_script = params.confirm_wakeup_script

        # mixins
        self._standby = params.standby
        self._log_dir = params.log_dir
        self._test_dir = params.test_dir
        self._libs_dir = params.libs_dir
        self._player_settings = params.player_settings


    def _execute_test(self):
        self.remove_camlog_file()

        try:
            res = self.__exec_precondition_script()
        except:
            raise

        if not res:
            return

        self._testlog('\n No need to execute night dcm test. '
                      'Executing main script instead'
                     )
        try:
            self.start_test_script(self._interpreter, self._test_script,
                                   self._timeout)
        except:
            raise

    def __exec_precondition_script(self):
        self.check_test_files()

        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable')

        self.start_serial_logging()
        self.start_precon_playback()
        try:
            self.start_test_script('WeBiz', self._precon_script, self._timeout)
            result, *_ = self.parse_log()
        except:
            raise
        finally:
            self.stop_precon_playback()

        if result == TEST_STATUS.passed:
            self._testlog('Scheduled scan is executed')
            self._testlog('Test result: TEST_PASSED')
            return True
        elif result == TEST_STATUS.blocked:
            raise RuntimeError('Can not go to night dcm script execution')
        else:
            self._testlog(
                'Scheduled scan was not executed. Transfer TV to standby'
            )

            # Delete precondition failed result from log file
            general.replace_in_log(
                self._testlog_fd, 'Test result: TEST_FAILED', ''
            )

            self.__exec_night_dcm()

    def __exec_night_dcm(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable')

        self.move_to_standby()
        self.dcm_monitor()

        self.start_test_script('WeBiz', self._confirm_wakeup_script, 30)
        self.start_test_script('WeBiz', self._test_script, self._timeout)
