import time

from client.utils.tv.nonsoap_commands import ping
from client.controllers import Controller
from client.mixins import (CAMMixin, CheckTestFilesMixin, PlaybackMixin,
                           StartScriptMixin, TPSCLoggingMixin)


class ControllerForCAM(Controller,
                       CheckTestFilesMixin,
                       PlaybackMixin,
                       CAMMixin,
                       StartScriptMixin,
                       TPSCLoggingMixin
                       ):
    """
    Controller is designed to execute test script in condition of running
    CAM Emulator that simulate connected CA module.
    Step description:
    1. Check if all test files are present and terminate test
        if some of mandatory files are disappeared.
    2. Check if tested device is available by given IP. Test will be terminated
        if IP is not reachable
    3. Copy autostart profile to directory there CAM Emulator will be started.
        Attention! Test should be terminated if
        autostart profile is not copied.
    4. Start serial logging: pairing TV with current PC, set required
        logging levels, and start collecting serial logs to log file.
        Test will be continued without log collection if something went wrong
    5. Start playback in background of all requested step streams.
        Test will be terminated if playback is not started for any of streams.
    6. Start CAM emulator
    7. Execute TV connect to CAM emulator via sending SOAP command
    8. Start test script and wait till is finished (by the end of
        script execution, or by timeout).
    9. Reboot TV if test script hangs - it is temporary function
        for tests stabilisation. This function will reboot only TV.
        Nothing will happend if tested device is unknown.
    10. Stop logging and playback processes.
        Print footer at the end of test log
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
        self._cam_script = params.cam_script
        self._test_dir = params.test_dir
        self._log_dir = params.log_dir

    def _execute_test(self):
        self.check_test_files()

        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        self.start_serial_logging()

        self.start_playback()

        try:
            self.run_emulator()
        except:
            raise

        # Send request for CAM emulator connect
        time.sleep(10)

        # Execute main test script
        try:
            self.start_test_script(
                self._interpreter, self._test_script, self._timeout
            )
        except:
            raise
