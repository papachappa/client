import time
from pathlib import Path

from client.settings import TOOLS_DIR
from client.utils import general
from client.utils.tv.soap_commands import debug_show, logging_commands

from .tvpcpairingmixin import TVPCPairingMixin


class SerialLoggingMixin(TVPCPairingMixin):
    """ Initialize file descriptor and open serial log file for appending
        serial message logs. Closing it on exit/end test run 
        Also mixin for setting serial log levels, executing logger.py, getting
        serial logs from TV and writing them on serial log file. """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)
        self.__serial_log_file = params.serial_log
        self.__seriallogger = None
        self._collect_serial_logs = params.collect_serial_logs
        self._serial_log_setting_global = params.serial_log_setting_global
        self._serial_log_setting = params.serial_log_setting
        self._serial_logger_script = Path(TOOLS_DIR, 'serial_logger', 'logger.py')

    def __exit__(self, *eargs):
        if self.__seriallogger: self.__seriallogger.close()
        super().__exit__(*eargs)

    def _seriallog(self, text):
        self._created_logs.add('serial')
        with self.__serial_log_file.open('a+') as f:
            f.write(text + '\n')

    @property
    def _seriallog_fd(self):
        if self.__seriallogger is None or self.__seriallogger.closed:
            self.__seriallogger = self.__serial_log_file.open('a+')
            self._created_logs.add('serial')
        return self.__seriallogger

    @_seriallog_fd.deleter
    def _seriallog_fd(self):
        self.__seriallogger.close()
        self.__seriallogger = None

    def start_serial_logging(self):
        self._testlog('\n--- Logger info ---')

        try:
            self._start_serial_logging()
        except Exception as e:
            self._seriallog('Logger was not started')
            self._seriallog('Reason: ' + str(e))
            self._testlog('#WARN: Test will be continued without log collection')
        finally:
            self._testlog('--- Logger info (END) ---')

    def _start_serial_logging(self):
        if not self._serial_log_setting or not self._collect_serial_logs:
            self._testlog('Test does not require log collection.')
            return
        self._pair_tv_pc()
        self._start_serial_logger()
        try:
            self.__set_serial_logging_settings()
        except:
            raise

        try:
            debug_show.debug_show(self._tvip)
        except Exception as e:
            self._testlog('INFO: Set debug levels are not shown {}' + str(e))

    def _start_serial_logger(self):
        try:
            p = general.start_serial_logger(
                self._serial_logger_script, self._tvip, self._seriallog_fd
            )
        except:
            raise
        else:
            self._seriallog('Collection of serial logs was started')
            self._processes.append(p)

        return p

    def __set_serial_logging_settings(self):
        """set test log levels, steps logic:
           clear existing settings
           set global levels if exists
           set specific levels for current step if exists
           if failed log should not be collected"""
        self._testlog('Clearing debug levels...')
        try:
            cleared = logging_commands.clear_dubug_levels(self._tvip)
            if not cleared:
                raise RuntimeError("clear_dubug_levels returned 'False'")
        except Exception as e:
            self._testlog('\n#WARN: debug levels were not cleared: ' + str(e))
            raise

        if self._serial_log_setting_global.is_file():
            self._testlog('Setting global debug levels...')
            try:
                self.__set_log_settings(self._serial_log_setting_global)
            except:
                self._testlog('#WARN: global debug levels were not set')
                raise

        self._testlog('Setting test debug levels...')
        try:
            self.__set_log_settings(self._serial_log_setting)
        except:
            self._testlog(
                '#WARN: requested debug levels are not set correctly'
            )
            raise

    def __set_log_settings(self, log_setting):
        """Set serial loggings"""
        is_setting_str = lambda l: l and not l.startswith('#')

        with log_setting.open() as content:
            for setting in filter(is_setting_str, content):
                self.__apply_log_setting(setting)

    def __apply_log_setting(self, setting):
        if setting == "clear":
            try:
                logging_commands.clear_dubug_levels(self._tvip)
            except Exception as e:
                self._testlog('\n#WARN: debug levels were not cleared '+str(e))
            return

        # if setting != clear
        module, level, *_ = setting.split()
        self._testlog(
            "Setting debug level '{}' for module '{}'".format(level, module)
        )

        try:
            logging_commands.set_dubug_level(module, level, self._tvip)
        except AssertionError:
            self._testlog("\n#WARN: Current level is not as expected")
        except NameError:
            self._testlog("\n#WARN: Unknown debug level" + str(level))
            raise
        except RuntimeError:
            self._testlog("\n#WARN: Unknown module '{}'".format(module))
            raise
        except Exception as e:
            self._testlog('\n#WARN: Connection via SOAP failed')
            self._testlog("\nReason: " + str(e))
            raise

        self._testlog("The debug level was set")
        time.sleep(1)
