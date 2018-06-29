from client.controllers import Controller
from client.mixins import (CheckTestFilesMixin, OnDemandSerialLogging,
                           TestLoggingMixin)
from client.utils.tv.nonsoap_commands import ping


class ControllerForSerialLogs(Controller,
                              CheckTestFilesMixin,
                              OnDemandSerialLogging,
                              TestLoggingMixin
                              ):
    """
    Controller is designed to get serial logs from TV
    The reason to change existing Popen subprocess creation to pexpect
    is that logger.py can not output incoming messages to stdout
    Step description:
    1. Check if tested device is available by given IP. Test will be terminated
        if IP is not reachable
    2. Start serial logging for given amount of time(timeout):
       pairing TV with current PC, set required
       logging levels, and start to collect serial logs to serial_log file.
       If something went wrong exception is rised
    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        self._timeout = params.timeout
        self._serial_log_setting = params.serial_log_setting

    def _execute_test(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        if not self._serial_log_setting:
            raise RuntimeError('Test requires to set log settings')

        try:
            self.start_serial_logging()
        except:
            raise

        self._testlog('\nTest result: TEST_PASSED')
