from client.utils import general

from .reboottvmixin import RebootTVMixin


class StartScriptMixin(RebootTVMixin):
    """ Mixin to execute test script. Test script can be Webiz or Python file
        with statements. Three attempts to execute are set. If it fails or test 
        file is absent reboot TV will be started """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tvip = None
        self._player_settings = None
        self._test_dir = None
        self._log_dir = None

    def start_test_script(self, interpreter, script, timeout):
        self._testlog('\n--- Test script info ---')

        try:
            self._start_test_script(interpreter, script, timeout)
        except Exception as e:
            self._testlog('Script execution failed. Reason: ' + str(e))
            self._testlog('TV will be rebooted for preparation for next test')
            self.reboot_tv()
            raise
        finally:
            self._testlog('--- Test script info (END) ---')

    def _start_test_script(self, interpreter, script, timeout):
        if not interpreter:
            self._testlog('Script execution was not requested')
            return

        max_attempts = 3

        for i in range(max_attempts):
            self._testlog('Attempt {} to execute test script'.format(i+1))

            try:
                self.__run_script(interpreter, script, timeout)
            except:
                raise

            connected = self.__check_connection()

            if connected:
                self._testlog(
                    'Connection to TV was executed from {} attempt'.format(i+1)
                )
                break

    def __run_script(self, interpreter, script, timeout):
        if interpreter == 'python':
            start = general.start_python
        elif interpreter == 'WeBiz':
            start = general.start_webiz

        try:
            p = start(script, self._tvip, self._testlog_fd, self._test_dir,
                      self._player_settings, self._log_dir
                     )
        except:
            raise
        else:
            self._processes.append(p)

        try:
            p.wait(timeout)
        except:
            p.terminate()
            raise

    def __check_connection(self):
        connected = False

        not_connected_f = lambda line: "cannot connect" in line
        connected = not any(filter(not_connected_f, self._testlog_r_fd))

        return connected
