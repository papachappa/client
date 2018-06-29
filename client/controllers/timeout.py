from client.controllers import Controller
from client.mixins import (CheckTestFilesMixin, PlaybackMixin, TimeoutMixin,
                           TPSLoggingMixin)


class ControllerTimeout(Controller,
                        CheckTestFilesMixin,
                        TimeoutMixin,
                        PlaybackMixin,
                        TPSLoggingMixin
                        ):
    """ Controller is designed to implement timeout between tests  """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._timeout = params.timeout

    def _execute_test(self):
        self.execute_timeout()
        self._testlog('\nTest result: TEST_PASSED')
