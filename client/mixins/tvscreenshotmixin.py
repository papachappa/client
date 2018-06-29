import time
from datetime import datetime as dt
from pathlib import Path

from client.mixins.basemixin import BaseMixin
from client.settings import WEBIZ_SCRIPTS_DIR
from client.utils import general
from client.utils.osutils import ssh
from client.utils.tv.soap_commands import screenshot


class TVScreenshotMixin(BaseMixin):
    """ Mixin for getting screenshot of current screen on TV. Download to test 
        machine and delete from TV. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tvip = None
        self._log_dir = None

        self.__webiz_script = Path(WEBIZ_SCRIPTS_DIR, 'get_screenshot.html')
        self.__remote_file = Path('/tmp', 'tvscreen')

    def get_screenshot(self):
        self.__send_enable_command()
        self.__get_screenshot_webiz()

        # wait before file saves on tv
        time.sleep(5)
        self.__download_file()

    def __send_enable_command(self):
        self._testlog("Activate tv screenshot setting...")

        try:
            screenshot.enable(self._tvip)
        except:
            raise

    def __get_screenshot_webiz(self):
        self._testlog("Execute Webiz script...")

        try:
            p = general.start_webiz(
                self.__webiz_script, self._tvip, self._testlog_fd
            )
        except:
            raise

        try:
            p.wait(15)
        except:
            p.terminate()
            raise RuntimeError("Webiz script timeout error")

    def __download_file(self):
        self._testlog("Downloading file...")

        fname = dt.now().strftime('tvscreen_%d_%H_%M_%S.png')
        local_file = Path(self._log_dir, fname)

        try:
            ssh.get_file(self._tvip, self.__remote_file, local_file)
        except:
            raise
        else:
            self._testlog("Screenshot saved to '{}'".format(local_file))
            self._testlog('Test result: TEST_PASSED')
        finally:
            ssh.remove_file(self._tvip, self.__remote_file)
