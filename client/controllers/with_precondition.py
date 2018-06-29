from client.utils import general
from client.utils.tv.nonsoap_commands import ping
from client.controllers import Controller
from client.mixins import (CheckTestFilesMixin, PlaybackMixin,
                           PreconPlaybackMixin, StartScriptMixin,
                           TPSLoggingMixin)


class ControllerWithPrecondition(Controller,
                                 CheckTestFilesMixin,
                                 StartScriptMixin,
                                 PreconPlaybackMixin, PlaybackMixin,
                                 TPSLoggingMixin,
                                 ):
    """
    Controller is designed to execute test script only if precondition
    was executed correctly. Precondition script and main test script can
    be accompanied with some playback.
    Step description:
    1. Check if all test files are present and terminate test
        if some of mandatory files are disappeared.
    2. Check if tested device is available by given IP. Test will be terminated
        if IP is not reachable
    3. Start serial logging: pairing TV with current PC, set required
        logging levels, and start collecting serial logs to log file.
        Test will be continued without log collection if something went wrong
        Attention! Levels of serial logging is the same for both scripts,
        complete serial logs with be saved in the same file for both scripts
    4. Start playback for precondition in background of all requested streams.
        Test will be terminated if playback is not started for any of streams.
    5. Start precondition script and wait until it's finished (by the end of
        script execution, or by timeout). Test will be terminated if
        precondition is not finished correctly or doesn't have
        "Test result: TEST_FAILED" label. Reboot TV if precondition script hangs
         - it is temporary function for tests stabilisation. This function will
         reboot only TV.Nothing will happend if tested device is unknown.
    6. Stop playback of started precondition streams
    7. Change precondition label "Test result: TEST_PASSED" to
        "Precondition result: PRECONDITION_PASSED". To avoid wrong result
        interpretation if test script is not executed correctly
    8. Start playback in background of all requested step streams.
        Test will be terminated if playback is not started for any of streams.
    9. Start test script and wait till is finished (by the end of
        script execution, or by timeout).Reboot TV if test script hangs
        - it is temporary function for tests stabilisation. This function
        will reboot only TV. Nothing will happend if tested device is unknown.
    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        self._precon_interpreter = params.precon_interpreter
        self._timeout = params.timeout

        self._interpreter = params.interpreter
        self._test_step_patern = params.test_step_patern
        self._testscript_pattern = '.*'
        self._preconscript_pattern = '_precondition.*'

        # mixins
        self._precon_player_settings = params.precon_player_settings
        self._serial_log_setting = params.serial_log_setting
        self._player_settings = params.player_settings
        self._test_dir = params.test_dir
        self._log_dir = params.log_dir


    def _execute_test(self):
        self.check_test_files()

        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')
        self.start_serial_logging()
        self.start_precon_playback()

        # Execute precondition script
        # Deliberatly exit without rising, return by design
        try:
            self.start_test_script(self._precon_interpreter, self._precon_script,
                                   self._timeout)
        except:
            raise
        finally:
            self.stop_precon_playback()

        # Update precondition result print
        replaced = general.replace_in_log(
            self._testlog_fd,
            'Test result: TEST_PASSED',
            'Precondition result: PRECONDITION_PASSED'
        )
        if not replaced:
            self._testlog(
                '\nPrecondition was not executed with PASS result.'
            )
            self._testlog('Test will be terminated.')
            self._testlog('Test result: TEST_FAILED')
            return

        self.start_playback()
        try:
            # Execute main test script
            self.start_test_script(self._interpreter, self._test_script,
                                   self._timeout)
        except:
            raise
