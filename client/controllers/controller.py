from datetime import datetime
from abc import ABC, abstractmethod

from client.constants import TEST_STATUS
from client.controllers import TestResult
from client.mixins import BaseMixin, ParseTestLogMixin
from client.utils.tv.soap_commands import get_chassis_info, get_crash_logs


class Controller(ParseTestLogMixin, # TODO: temporary
                BaseMixin,
                ABC
                ):
    """ Main controller for other controllers. Sets several environment vars. 
        Runs and finishing tests, prints overall result """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        self.__start_time = datetime.now()

        self._tvip = params.tvip
        self._result = TestResult(tv_ip=self._tvip)

        self.__test_script = None
        self._test_step_patern = None
        self._testscript_pattern = None

        self.__precon_script = None
        self._preconscript_pattern = None

    # TODO: find a correct place
    @property
    def _test_script(self):
        if self.__test_script is None:
            self.__test_script = self._check_and_get_unique_script(
                    self._test_step_patern, self._testscript_pattern
                )
        return self.__test_script
    
    # TODO: find a correct place
    @_test_script.setter
    def _test_script(self, val):
        self.__test_script = val

    # TODO: find a correct place
    @property
    def _precon_script(self):
        if self.__precon_script is None:
            self.__precon_script = self._check_and_get_unique_script(
                    self._test_step_patern, self._preconscript_pattern
                )
        return self.__precon_script
    
    # TODO: find a correct place
    @_precon_script.setter
    def _precon_script(self, val):
        self.__precon_script = val

    @property
    def result(self):
        return self._result

    @abstractmethod
    def _execute_test(self):
        return

    def _get_status_data(self):
        return self.parse_log()

    def __get_crash_log(self):
        exceptions = []
        try:
            exceptions = get_crash_logs.getList(self._tvip)
        except Exception as e:
            self._testlog('#WARN: {}'.format(e))
            self._testlog('Crash logs were not retrieved from TV')
        return exceptions

    def run_the_test(self, **kwargs):
        start = datetime.strftime(self.__start_time, '%Y-%m-%d %H:%M:%S')
        self._testlog('Start test: ' + start)

        initial_exceptions = set(self.__get_crash_log())
        try:
            self._execute_test()
        except Exception as e:
            self._testlog('\n\n#ERROR: {}'.format(e))
            self._testlog('Test will be terminated')
            self._testlog('Test result: TEST_BLOCKED\n')

        final_exceptions = set(self.__get_crash_log())
        duration = datetime.now() - self.__start_time
        self._finish_test(initial_exceptions, final_exceptions, duration)

        self._testlog("\n\nTest duration: {} sec".format(duration.seconds))

    def _finish_test(self, initial_exceptions, final_exceptions, duration):
        self._result.logs = self._created_logs
        self._result.duration = duration

        try:
            tv_chassis, tv_software = get_chassis_info(self._tvip)
        except:
            pass
        else:
            self._result.tv_chassis = tv_chassis
            self._result.tv_software = tv_software
            self._testlog("\nTested configuration:")
            self._testlog("Software Version: " + (tv_software or 'N/A'))
            self._testlog("Chassis: " + (tv_chassis or 'N/A'))

        try:
            status, warnings, errors = self._get_status_data()
        except Exception as e:
            self._testlog("\nUnable to parse log file: {}".format(e))
        else:
            if status is None:
                status = TEST_STATUS.blocked
                self._testlog('\nTest result: TEST_BLOCKED\n')

            self._result.status = status
            if status != TEST_STATUS.passed:
                self._result.detailed_result = ''.join(errors)

            self.__print_status_data('Warnings', warnings)
            self.__print_status_data('Errors', errors)

        new_logs = list(final_exceptions - initial_exceptions)
        if new_logs:
            self._result.crashes.extend(new_logs)
            self._testlog('\nINFO: List of new crash logs: ' + str(new_logs))

    def __print_status_data(self, head, data):
        if not data:
            return

        __get_prefix = '\n--- {} ---'.format
        __get_postfix = '--- {} (END)---'.format
        __join_messages = lambda m: '\n'.join(map(lambda x: x.strip(), m))

        self._testlog(__get_prefix(head))
        self._testlog(__join_messages(data))
        self._testlog(__get_postfix(head))
