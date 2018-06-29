from client.controllers import Controller
from client.mixins import (CheckTestFilesMixin, PlaybackMixin,
                           StartScriptMixin, TPSLoggingMixin)
from client.utils.tv.nonsoap_commands import ping


class ControllerStandard(Controller,
                         CheckTestFilesMixin,
                         PlaybackMixin,
                         StartScriptMixin,
                         TPSLoggingMixin
                         ):
    """
    Controller is designed to simple execute test script.
    Step description:
    1. Check if all test files are present and terminate test
        if some of mandatory files are disappeared.
    2. Check if tested device is available by given IP. Test will be terminated
        if IP is not reachable
    3. Start serial logging: pairing TV with current PC, set required
        logging levels and start collecting serial logs to log file.
    4. Start playback in background of all requested streams.
        Test will be terminated if playback is not started for any of streams.
    5. Check if name_Standby.html file is present, ONLY if file is not exist
        create new one with standby timeout that is
        provided in input parameters.
    6. Execute test script.
    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._interpreter = params.interpreter
        self._timeout = params.timeout
        self._test_step_patern = params.test_step_patern
        self._testscript_pattern = '.*'

        # mixins
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

        try:
            self.start_test_script(
                self._interpreter, self._test_script, self._timeout
            )
        except:
            raise
