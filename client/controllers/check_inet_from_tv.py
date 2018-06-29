from client.controllers import Controller
from client.mixins import CheckInetMixin, TestLoggingMixin
from client.utils.tv.nonsoap_commands import ping


class ControllerForCheckInetFromTV(Controller, CheckInetMixin, TestLoggingMixin):
    """
    Controller is designed to check internet from TV
    Step description:
    1. SSH to TV and run ping command
    2. If something went wrong raise error
    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._timeout = params.timeout

    def _execute_test(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        try:
            self._ping_resource()
        except Exception as e:
            self._testlog('Ping failed. Reason: {}'.format(e))
            self._testlog('Test result: TEST_FAILED')
        else:
            self._testlog('\nAll services were pinged successfully.')
            self._testlog('Test result: TEST_PASSED')
