from client.controllers import Controller
from client.mixins import TestLoggingMixin, TVScreenshotMixin
from client.utils.tv.nonsoap_commands import ping


class ControllerGetTVScreenshot(Controller,
                                TVScreenshotMixin,
                                TestLoggingMixin
                                ):
    """ Controller is designed to get a screenshot from tv and save it in
    step log folder. """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._log_dir = params.log_dir
        self._timeout = params.timeout

    def _execute_test(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable')

        self.get_screenshot()
