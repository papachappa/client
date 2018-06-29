from client.controllers import Controller
from client.mixins import TestLoggingMixin, TVServiceListMixin
from client.utils.tv.nonsoap_commands import ping


class ControllerForTVServiceList(Controller,
                                 TVServiceListMixin,
                                 TestLoggingMixin
                                ):
    """ Controller is designed to get Service List DB file from TV.
    File saves in step log directory with db extension. """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._timeout = params.timeout
        self._service_list_path = params.db_log

    def _execute_test(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        try:
            self.get_service_list()
        except Exception as e:
            self._testlog('\nFailed to get service list from TV: {}'.format(e))
            self._testlog('Test result: TEST_FAILED')
            return
        else:
            self._testlog(
                '\nService list available at: {}'.format(self._service_list_path)
            )
            self._testlog('Test result: TEST_PASSED')
