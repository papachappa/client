import time
from pathlib import Path

from client.utils.tv.nonsoap_commands import ping

from .startscriptmixin import StartScriptMixin


class TVStandbyMixin(StartScriptMixin):
    """ Mixin for preparing and transfer TV to standby state """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self._tvip = None
        self._standby = None
        self._utils_dir = params.utils_dir
        self.__standby_temp = Path(self._utils_dir, "Standby_temp.html")
        self.__standby_script = Path(self._utils_dir, "Standby.html")

    def _replace_duration_timeout(self):
        with self.__standby_script.open() as f:
            standby_script_data = f.read()

        replaced = standby_script_data.replace('SleepDuration_timeout',
                                               str(self._standby * 60))
        with self.__standby_temp.open('w') as f:
            f.write(replaced)

    def move_to_standby(self):
        self._replace_duration_timeout()

        self._testlog('\nSet alarm time and transfer TV to standby.')
        try:
            self.start_test_script('WeBiz', self.__standby_temp, 20)
        except:
            raise RuntimeError('Can not execute standby script')

        self._testlog('\nWait 60 sec to make sure TV is unreachable')
        time.sleep(60)

        if not ping.check_ip(self._tvip):
            self._testlog('#VERIFICATION PASSED: TV transferred to standby')
        else:
            raise RuntimeError('#VERIFICATION FAILED: TV did not go to standby.')
