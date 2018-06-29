from client.controllers import Controller
from client.mixins import DownloadCrashesDumpsMixin, TestLoggingMixin
from client.utils.tv.nonsoap_commands import ping


class ControllerForDownloadCrashesDumps(Controller,
                                        DownloadCrashesDumpsMixin,
                                        TestLoggingMixin
                                        ):
    """
    Controller is designed to download crash and dump core files from TV.
    Crash files reside on /var/local/clogs/dvbcrash_19700103023126.log
    Dump files reside /mnt/lo_0*/clogs/012837489920.core
    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        # mixins
        self._timeout = params.timeout
        self._log_dir = params.log_dir

    def _execute_test(self):
        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        try:
            self.get_crash_logs()
        except Exception as e:
            self._testlog('\nCrash Files was not retrieved from TV. ')
            self._testlog('Reason: {}'.format(e))
            self._testlog('\nTest result: TEST_FAILED')
            return

        try:
            self.get_dump_files()
        except Exception as e:
            self._testlog('\nDump Files was not retrieved from TV. ')
            self._testlog('Reason: {}\n'.format(e))
            self._testlog('\nTest result: TEST_FAILED')
            return

        self._testlog('\nTest result: TEST_PASSED')
