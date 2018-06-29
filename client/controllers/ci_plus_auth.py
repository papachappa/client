import time

from client.controllers import Controller
from client.mixins import (CheckTestFilesMixin, CIPlusAuthMixin, PlaybackMixin,
                           StartScriptMixin, TPSLoggingMixin)
from client.utils.tv.nonsoap_commands import ping


class ControllerForCIPlusAuth(Controller,
                              CheckTestFilesMixin,
                              PlaybackMixin,
                              StartScriptMixin,
                              CIPlusAuthMixin,
                              TPSLoggingMixin
                              ):
    """
       ControllerForCIPlusAuth
       Execute WeBiz script, then in parallel execute main python script,
       Wait for Webiz Script stop and check his results.
       Fields in gdoc:
       controller=for_ci_plus_auth
       interpreter=python
       timeout=10
    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        self._interpreter = params.interpreter
        self._timeout = params.timeout
        self._test_step_patern = params.test_step_patern
        self._testscript_pattern = '.*'

        # mixins
        self._suite_dir = params.suite_dir
        self._serial_log_setting = params.serial_log_setting
        self._player_settings = params.player_settings
        self._test_dir = params.test_dir
        self._log_dir = params.log_dir


    def _execute_test(self):
        self.check_test_files()

        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        self.start_serial_logging()

        self.start_playback()

        self.exec_webiz_auth_script()

        # Wait for WeBiz script prepared to work
        time.sleep(10)

        # Exec python script
        try:
            self.start_test_script(self._interpreter, self._test_script,
                                   self._timeout)
        except:
            raise

        # Wait for Webiz Script to stop
        try:
            self.wait_for_webiz_termination()
        except:
            self._testlog('\nTest result: TEST_FAILED')
