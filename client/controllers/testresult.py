from client.constants import TEST_STATUS


class TestResult:
    """ Controller for generating detailed test run results """

    def __init__(self, status=None, duration=None, tv_ip=None, tv_mac=None):
        if status is None:
            self._status = TEST_STATUS.blocked
        else:    
            self._status = TEST_STATUS(status)

        self.duration = duration

        self.tv_ip = tv_ip
        self.tv_mac = tv_mac

        self.tv_chassis = None
        self.tv_software = None

        self.detailed_result = None
        self.crashes = []
        self.__logs = []

    @property
    def status(self):
        return self._status

    @property
    def logs(self):
        return self.__logs
    
    @logs.setter
    def logs(self, val):
        self.__logs = list(val)

    @status.setter
    def status(self, value):
        if value is None:
            self._status = TEST_STATUS.blocked
        else:
            self._status = TEST_STATUS(value)

    def to_dict(self):
        r = {
            'status': self.status.value,
            'duration': self.duration and str(self.duration),
            'tv_ip': self.tv_ip,
            'tv_mac': self.tv_mac,
            'tv_chassis': self.tv_chassis,
            'tv_software': self.tv_software,
            'detailed_result': self.detailed_result,
            'crashes': self.crashes,
            'logs': self.logs,
        }
        return r
