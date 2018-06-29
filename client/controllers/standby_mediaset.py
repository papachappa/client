from client.controllers import Controller
from client.mixins import (CheckTestFilesMixin, DCMMonitorMixin, PlaybackMixin,
                           PreconPlaybackMixin, TPSLoggingMixin,
                           TVStandbyMixin)
from client.utils.tv.nonsoap_commands import ping


class ControllerStandbyMediaset(Controller,
                                CheckTestFilesMixin,
                                PreconPlaybackMixin, PlaybackMixin,
                                TVStandbyMixin,
                                DCMMonitorMixin,
                                TPSLoggingMixin,
                                ):
    """
    Controller is designed to execute test script only if TV was
    transferred in standby and woken up. There is the same playback is active
    during main test script and standby.
    Step description:
    1. Check if all test files are present and terminate test
        if some of mandatory files are disappeared.
    2. Check if tested device is available by given IP. Test will be terminated
        if IP is not reachable
    3. Start serial logging: pairing TV with current PC, set required
        logging levels and start collecting serial logs to log file.
        Test will be continued without log collection if something went wrong
    4. Start playback in background of all requested streams.
        Test will be terminated if playback is not started for any of streams.
    5. Check if name_Standby.html file is present, ONLY if file is not exist
        create new one with standby timeout that is provided in input parameters.
    6. Execute XXX_Standby.html script to set alarm and transfer TV to standby.
    7. Wait 10 sec for TV set go to standby. Remove alarm and stop test
        if TV was not transferred to standby.
    8. Wait for DCM, when TV wakes up for DCM check time of set alarm,
        if time jump is appeared, set new alarm.
    9. Wait for TV wakes up.
        Attention! Standby time should be monitoried and test should be stopped if
        test is not fined during set timeout
    10. Start test script and wait till is finished (by the end of
        script execution, or by timeout).
    11. Reboot TV if test script hangs - it is temporary function
        for tests stabilisation. This function will reboot only TV.
        Nothing will happend if tested device is unknown.
    12. Stop logging and playback processes. Print footer at the end of test log

    """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        self._confirm_wakeup_script = params.confirm_wakeup_script
        self._interpreter = params.interpreter

        self._test_step_patern = params.test_step_patern
        self._testscript_pattern = '.*'

        # mixins
        self._precon_player_settings = params.precon_player_settings
        self._player_settings = params.player_settings
        self._standby = params.standby

        self._test_dir = params.test_dir

        self._libs_dir = params.libs_dir
        self._utils_dir = params.utils_dir
        self._log_dir = params.log_dir
        self._timeout = params.timeout

    def _execute_test(self):
        self.check_test_files()

        if not ping.check_ip(self._tvip):
            raise RuntimeError('Device under test is unreachable.')

        self.start_serial_logging()

        self.move_to_standby()

        self.start_precon_playback()

        try:
            self.dcm_monitor()
        except Exception as e:
            self._testlog('{}\n'.format(e))
            self._testlog('Test will be terminated.')
            self._testlog('\nTest result: TEST_FAILED')
            return
        finally:
            self.stop_precon_playback()


        self.start_playback()
        try:
            self.dcm_monitor()
        except:
            return

        try:
            # Execute middle script
            self.start_test_script('WeBiz', self._confirm_wakeup_script, 30)
            # Execute main script
            self.start_test_script(self._interpreter, self._test_script, 600)
        except:
            raise
