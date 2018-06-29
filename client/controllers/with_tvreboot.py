from client.controllers import Controller
from client.mixins import (CheckTestFilesMixin, PlaybackMixin,
                           StartScriptMixin, TPSLoggingMixin)
from client.utils.tv.nonsoap_commands import ping


class ControllerWithTVReboot(Controller,
                             CheckTestFilesMixin,
                             PlaybackMixin,
                             StartScriptMixin,
                             TPSLoggingMixin
                            ):
    """
    Controller is designed to start some playback
    (0 or more streams at the same time), execute test script if requested,
    and execute TV reboot as the MAIN action.
    Step description:
    1. Check is all test files are present and terminate test
        if some of mandatory files are disapper.
    2. Check if tested TV is available by given IP. Test will be terminated
        if IP is not reachable
    3. Start serial logging: pairing TV with current PC, set required
        logging levels, and start collect serial logs to log file.
        Test will be continued without log collection if something went wrong
    4. Start playback in background of all requested streams.
        Test will be terminated if playback is not started for any of streams.
    5. Start test script if it is requested (interpritator is not "None")
        and wait till is finished (by the end of script execution,
        or by timeout).
    6. Reboot tested TV.
    7. Stop logging and playback processes and print footer at the end of test log

    This controller is developed to reboot ONLY knowed TV sets.
    Nothing will happend if tested device is unknown device. Test will be
    failed if test script or reboot is not executed correctly.
    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._interpreter = params.interpreter
        self._timeout = params.timeout
        self._test_step_patern = params.test_step_patern
        # mixins
        self._serial_log_setting = params.serial_log_setting
        self._player_settings = params.player_settings
        self._test_dir = params.test_dir
        self._log_dir = params.log_dir

    def _execute_test(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        self.start_serial_logging()

        self.start_playback()

        try:
            self.reboot_tv()
        except:
            status = 'TEST_FAILED'
        else:
            status = 'TEST_PASSED'
        finally:
            self._testlog('\nTest result: {}'.format(status))
