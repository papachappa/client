import time

from client.controllers import Controller
from client.mixins import CheckTestFilesMixin, PlaybackMixin, TPSLoggingMixin
from client.utils.tv.nonsoap_commands import ping


class ControllerForPlayback(Controller,
                            CheckTestFilesMixin,
                            PlaybackMixin,
                            TPSLoggingMixin
                            ):
    """
    Standard controller is designed to start some playback
    (0 or more streams at the same time).
    Step description:
    1. Check if tested device is available by given IP. Test will be terminated
        if IP is not reachable
    2. Start serial logging: pairing TV with current PC, set required
        logging levels, and starte collect serial logs to log file.
        Test will be continued without log collection if something went wrong
    3. Start playback in background of all requested streams.
        Test will be terminated if playback is not started for any of streams.
    4. Wait for set timeout. Finish test
    5. Stop logging and playback processes and print footer at the end of test log

    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._timeout = params.timeout
        self._serial_log_setting = params.serial_log_setting
        self._player_settings = params.player_settings
        self._test_dir = params.test_dir
        self._log_dir = params.log_dir

    def _execute_test(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable')

        self.start_serial_logging()

        self.start_playback()

        time.sleep(self._timeout)

        self._testlog('\nTest result: TEST_PASSED')
