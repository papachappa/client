from client.constants import TEST_STATUS

from .basemixin import BaseMixin

_is_warn =  lambda l: 'WARN' in l
_is_error = lambda l: 'ERROR:' in l or 'FAILED:' in l

_is_blocked = lambda s, l: s == TEST_STATUS.blocked or 'TEST_BLOCKED' in l
_is_failed = lambda s, l: s == TEST_STATUS.failed or 'TEST_FAILED' in l
_is_passed = lambda _, l: 'TEST_PASSED' in l


class ParseTestLogMixin(BaseMixin):
    """ Mixin for parsing test log file. Gettting result, warnings and errors"""

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

    def parse_log(self):
        return self.__parse_log()

    def __parse_log(self):
        line_counter = 0
        errors, warnings = [], []

        status = None

        for line in self._testlog_r_fd:
            if line.startswith('#'):
                line_counter += 1

                if _is_warn(line):
                    warnings.append('{}: {}'.format(line_counter, line))
                if _is_error(line):
                    errors.append('{}: {}'.format(line_counter, line))

            elif line.startswith('Test result'):
                if _is_blocked(status, line):
                    status = TEST_STATUS.blocked
                elif _is_failed(status, line):
                    status = TEST_STATUS.failed
                elif _is_passed(status, line):
                    status = TEST_STATUS.passed

        return status, warnings, errors
