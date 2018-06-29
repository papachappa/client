import pexpect

from client.utils.osutils.timeout import Timeout

from .serialloggingmixin import SerialLoggingMixin


class OnDemandSerialLogging(SerialLoggingMixin):
    """ Mixin for getting serial logs from TV on demand. Set log settings and
        see logs in real time. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tvip = None
        self._timeout = None

    def start_serial_logging(self):
        self._testlog('\n--- Logger info ---')
        try:
            self._pair_tv_pc()
            self.__start_serial_logger()
        except Exception as e:
            self._testlog('Logging will not be started. Reason: ' + str(e))
            raise
        finally:
            self._testlog('\n--- Logger info (END) ---')

    def __start_serial_logger(self):
        # timeout=self._timeout + 10 is a time to raise exception
        # if nothing comes to pexpect pipe, need to be more than self._timeout
        # in order to avoid pexpect timeout exception
        timeout = self._timeout + 10
        cmd = '{} {}'.format(self._serial_logger_script.as_posix(), self._tvip)
        try:
            serial_collection = pexpect.spawn(cmd, timeout=timeout)
        except:
            raise
        else:
            self._seriallog('Serial log collection was started\n')
            self._processes.append(serial_collection.pid)

        self._testlog('Serial log collection was started')
        self._testlog('Look at serial log file')

        try:
            with Timeout(self._timeout):
                while True:
                    line = serial_collection.readline().rstrip()
                    self._seriallog(line.decode('utf-8'))
        except Timeout.Timeout:
            self._testlog('\nSerial log collection was finished')
        finally:
            serial_collection.close(force=True)
