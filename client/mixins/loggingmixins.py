from .basemixin import BaseMixin
from .serialloggingmixin import SerialLoggingMixin

__all__ = [
    'TestLoggingMixin',
    'PlayerLoggingMixin',
    'SerialLoggingMixin',
    'CamLoggingMixin',
    'TSLoggingMixin',
    'TPLoggingMixin',
    'TPSLoggingMixin',
    'TPSCLoggingMixin',
]


class TestLoggingMixin(BaseMixin):
    """ Initialize file descriptor and open test log file for appending message
        logs. Closing it on exit/end test run """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self.__test_log_file = params.test_log
        self.__descriptors = []

    def __exit__(self, *eargs):
        for fd in self.__descriptors:
            fd.close()
        super().__exit__(*eargs)

    def _testlog(self, text):
        self._created_logs.add('test')
        with self.__test_log_file.open('a', 1) as f:
            f.write(text + '\n')

    @property
    def _testlog_fd(self):
        fd = self.__test_log_file.open('a+', 1)
        self.__descriptors.append(fd)
        self._created_logs.add('test')
        return fd

    @property
    def _testlog_r_fd(self):
        fd = self.__test_log_file.open('r')
        self.__descriptors.append(fd)
        return fd


class PlayerLoggingMixin(BaseMixin):

    """ Initialize file descriptor and open player log file for appending 
        lstreamer message logs. Closing it on exit/end test run """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        self.__player_log_file = params.player_log
        self.__playerlogger = None

    def __exit__(self, *eargs):
        if self.__playerlogger: self.__playerlogger.close()
        super().__exit__(*eargs)

    def _playerlog(self, text):
        self._created_logs.add('player')
        with self.__player_log_file.open('a', 1) as f:
            f.write(text + '\n')

    @property
    def _playerlog_fd(self):
        if self.__playerlogger is None or self.__playerlogger.closed:
            self.__playerlogger = self.__player_log_file.open('a+', 1)
            self._created_logs.add('player')
        return self.__playerlogger


class CamLoggingMixin(BaseMixin):

    """ Initialize file descriptor and open cam log file for appending cam
        emulator message logs. Closing it on exit/end test run """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        self.__cam_log_file = params.cam_log
        self.__camlogger = None

    def __exit__(self, *eargs):
        if self.__camlogger: self.__camlogger.close()
        super().__exit__(*eargs)

    def _camlog(self, text):
        self._created_logs.add('cam')
        with self.__cam_log_file.open('a', 1) as f:
            f.write(text + '\n')

    @property
    def _camlog_fd(self):
        if self.__camlogger is None or self.__camlogger.closed:
            self.__camlogger = self.__cam_log_file.open('a+', 1)
            self._created_logs.add('cam')
        return self.__camlogger

class TSLoggingMixin(TestLoggingMixin, SerialLoggingMixin): pass
class TPLoggingMixin(TestLoggingMixin, PlayerLoggingMixin): pass
class TPSLoggingMixin(TPLoggingMixin, SerialLoggingMixin): pass
class TPSCLoggingMixin(TPSLoggingMixin, CamLoggingMixin): pass
