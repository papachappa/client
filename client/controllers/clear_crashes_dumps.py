from client.controllers import Controller
from client.mixins import ClearCrashesDumpsMixin, TestLoggingMixin
from client.utils.tv.nonsoap_commands import ping


class ControllerForClearCrashesDumps(Controller,
                                     ClearCrashesDumpsMixin,
                                     TestLoggingMixin
                                    ):
    """
    Controller is designed to clear crash and dump core files from TV.
    Crash files reside on /var/local/clogs/dvbcrash_20100927005913.log
    Dump files reside /mnt/lo_004/clogs/dvbcrash_20160412101636.core
    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._timeout = params.timeout

    def _execute_test(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        try:
            self.clear_dump_files()
        except Exception as e:
            self._testlog('\nError getdump files from TV. Reason: {}.'.format(e))
            self._testlog('Removal of dump files failed')
            self._testlog('Test result: TEST_FAILED')
            return

        try:
            self.clearing_crash_logs()
        except Exception as e:
            self._testlog('\nRemoval crash files failed. Reason: {}'.format(e))
            self._testlog('Test result: TEST_FAILED')
            return

        self._testlog('\nTest result: TEST_PASSED')
