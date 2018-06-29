import copy
from pathlib import Path


class ControllerParams():
    def __init__(self, *args, **kwargs):
        self.__kwargs = copy.deepcopy(kwargs)
        self.__log_dir = kwargs['log_dir']
        nkey = kwargs['nkey']
        _, *suites, self.__step = nkey.split('.', maxsplit=nkey.count('.') - 2)
        self.__suite = Path(*suites)

        self.__test_log = None
        self.__serial_log = None
        self.__player_log = None
        self.__cam_log = None
        self.__timeout = None
        self.__interpreter = None
        self.__tvip = None
        self.__test_dir = None
        self.__libs_dir = None
        self.__utils_dir = None
        self.__suite_dir = None
        self.__test_step_pattern = None
        self.__player_settings = None
        self.__precon_interpreter = None
        self.__precon_player_settings = None
        self.__collect_serial_logs = None
        self.__serial_log_setting = None
        self.__serial_log_setting_global = None
        self.__standby = None
        self.__cam_script = None
        self.__db_log = None
        self.__confirm_wakeup_script = None

    @property
    def log_dir(self):
        return self.__log_dir

    @property
    def test_log(self):
        if self.__test_log is None:
            self.__test_log = Path(self.__log_dir, self.__step + '_test.log')
        return self.__test_log

    @property
    def serial_log(self):
        if self.__serial_log is None:
            self.__serial_log = Path(self.__log_dir, self.__step + '_serial.log')
        return self.__serial_log

    @property
    def player_log(self):
        if self.__player_log is None:
            self.__player_log = Path(self.__log_dir, self.__step + '_player.log')
        return self.__player_log

    @property
    def cam_log(self):
        if self.__cam_log is None:
            self.__cam_log = Path(self.__log_dir, self.__step + '_cam.log')
        return self.__cam_log

    @property
    def timeout(self):
        if self.__timeout is None:
            self.__timeout = int(self.__kwargs['timeout']) * 60
        return self.__timeout

    @property
    def interpreter(self):
        if self.__interpreter is None:
            self.__interpreter = self.__kwargs['interpreter']
        return self.__interpreter

    @property
    def tvip(self):
        if self.__tvip is None:
            self.__tvip = self.__kwargs['dut']
        return self.__tvip

    @property
    def test_dir(self):
        if self.__test_dir is None:
            self.__test_dir = self.__kwargs['test_dir']
        return self.__test_dir

    @property
    def libs_dir(self):
        if self.__libs_dir is None:
            self.__libs_dir = Path(self.test_dir, 'test_scripts', 'Libs')
        return self.__libs_dir

    @property
    def utils_dir(self):
        if self.__utils_dir is None:
            self.__utils_dir = self.libs_dir / 'Utilities'
        return self.__utils_dir

    @property
    def suite_dir(self):
        if self.__suite_dir is None:
            self.__suite_dir = Path(self.test_dir, 'test_scripts', self.__suite)
        return self.__suite_dir

    @property
    def test_step_patern(self):
        if self.__test_step_pattern is None:
            self.__test_step_pattern = self.suite_dir / self.__step
        return self.__test_step_pattern

    @property
    def player_settings(self):
        if self.__player_settings is None:
            try:
                self.__player_settings = [
                    Path(self.test_dir, 'player_settings', stream)
                    for stream in self.__kwargs.get('streams', [])
                ]
            except TypeError:
                self.__player_settings = []
        return self.__player_settings

    @property
    def precon_interpreter(self):
        if self.__precon_interpreter is None:
            self.__precon_interpreter = self.__kwargs['precon_interpreter']
        return self.__precon_interpreter

    @property
    def precon_player_settings(self):
        if self.__precon_player_settings is None:
            self.__precon_player_settings = [
                Path(self.test_dir, 'player_settings', stream)
                for stream in self.__kwargs.get('precon_streams', [])
            ]
        return self.__precon_player_settings

    @property
    def collect_serial_logs(self):
        if self.__collect_serial_logs is None:
            self.__collect_serial_logs = self.__kwargs.get('is_log', True)
        return self.__collect_serial_logs

    @property
    def serial_log_setting(self):
        if self.__serial_log_setting is None:
            try:
                self.__serial_log_setting = Path(
                    self.test_dir, 'log_settings', self.__kwargs['log']
                )
            except TypeError:
                self.__serial_log_setting = None
        return self.__serial_log_setting

    @property
    def serial_log_setting_global(self):
        if self.__serial_log_setting_global is None:
            self.__serial_log_setting_global = Path(
                self.test_dir, 'log_settings', 'global.conf'
            )
        return self.__serial_log_setting_global

    @property
    def standby(self):
        if self.__standby is None:
            self.__standby = self.__kwargs.get('standby', 0)
        return self.__standby

    @property
    def cam_script(self):
        if self.__cam_script is None:
            cam_script_name = self.test_step_patern.name + "_autostart.profile"
            self.__cam_script = self.test_step_patern.with_name(cam_script_name)
        return self.__cam_script

    @property
    def db_log(self):
        if self.__db_log is None:
            self.__db_log = Path(self.log_dir, self.__step + '.service_list.db')
        return self.__db_log

    @property
    def confirm_wakeup_script(self):
        if self.__confirm_wakeup_script is None:
            self.__confirm_wakeup_script = self.utils_dir / "ConfirmWakeUP.html"
        return self.__confirm_wakeup_script
