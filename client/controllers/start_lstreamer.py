import time

from client.controllers import Controller
from client.mixins import PlaybackMixin, TPSLoggingMixin
from client.utils.tv.nonsoap_commands import ping


class ControllerStartLstreamer(Controller, PlaybackMixin, TPSLoggingMixin):
    """ Controller for executing lstreamer with defined streams in UI """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        # mixins
        self._player_settings = params.player_settings
        self._test_dir = params.test_dir
        self._log_dir = params.log_dir

    def _execute_test(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        if not self._player_settings:
            raise RuntimeError("Can not start playback. "
                               "Player settings ini files was not found")

        self.start_serial_logging()

        try:
            self.start_playback()
        except Exception as e:
            self._testlog('\nAn a error occurred: {}.'.format(e))
            raise

        # wait untill cancel button will be pushed
        while True:
            pass
