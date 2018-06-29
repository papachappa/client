import subprocess
from pathlib import Path

from client.utils import general

from .basemixin import BaseMixin


class CIPlusAuthMixin(BaseMixin):
    """ Mixin for CIPlus authentication tests. Executes
        checkCamAutentication.html script and waits for its termination"""

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        self._tvip = None
        self._timeout = None
        self._suite_dir = params.suite_dir

        self.__cam_auth_script = Path(self._suite_dir.parent,
                                     'checkCamAutentication.html')
        self.__webiz_script = None

    def exec_webiz_auth_script(self):
        if not self.__cam_auth_script.is_file():
            raise RuntimeError('checkCamAutentication.html file not found')

        try:
            self.__webiz_script = general.start_webiz(
                self.__cam_auth_script, self._tvip, self._testlog_fd
            )
        except Exception as e:
            self._testlog('\n#ERROR: Auth script was not started')
            self._testlog('Reason: {}'.format(e))
            raise
        else:
            self._processes.append(self.__webiz_script)

    def wait_for_webiz_termination(self):
        try:
            self.__webiz_script.wait(self._timeout)
        except subprocess.TimeoutExpired:
            self._testlog('\n#ERROR: Script execution timeout expired')
            raise
        except:
            raise
        finally:
            self.__webiz_script.terminate()
