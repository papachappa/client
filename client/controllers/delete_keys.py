from client.controllers import Controller
from client.mixins import (DeleteLoregKeys, TestLoggingMixin)

from client.utils.tv.nonsoap_commands import ping


class ControllerDeleteKeys(Controller, DeleteLoregKeys, TestLoggingMixin):
    """ Controller for deleting loreg keys, imitating TV factory reset """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._timeout = params.timeout
        # mixins
        self._log_dir = params.log_dir

    def _execute_test(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        try:
            res = self._delete()
            self._testlog('Result of operation: {}'.format(res))
        except Exception as err:
            self._testlog('\nError: {}. Can not delete loreg keys'.format(err))
            self._testlog('\nTest result: TEST_FAILED')
        else:
            self._testlog('\nKeys were deleted')
            self._testlog('Test result: TEST_PASSED')
