import shutil
from pathlib import Path

from client.utils import general
from client.utils.osutils import network
from client.utils.tv import soap_commands

from .basemixin import BaseMixin


class CAMMixin(BaseMixin):
    """ Mixin for execute cam emulator and cam tests """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tvip = None
        self._cam_script = None

    def run_emulator(self):
        text = '\n--- CAM emulator info ---\nStart CAM emulator.'
        self._testlog(text)
        self._camlog(text)

        self.__start_cam_emulator()
        self.__emulator_connect()

        self._testlog('--- CAM emulator info (END)---')

    def __start_cam_emulator(self):
        try:
            _, tv_software = soap_commands.get_chassis_info(self._tvip)
        except:
            raise

        self.__prepare_to_start_cam_emu(tv_software)

        try:
            p = general.start_cam_emulator(tv_software, self._camlog_fd)
        except Exception as e:
            raise RuntimeError(
                'CAM emulator was not started. Reason: {}'.format(e)
            )
        else:
            self._testlog('CAM emulator was started.\n')
            self._processes.append(p)

    def __prepare_to_start_cam_emu(self, tv_software):
        self._testlog('Copy test CAM profile to emulator folder.\n')

        full_frame_app_dir = general.get_frame_app_dir(tv_software)
        auto_profile = Path(full_frame_app_dir, 'autostart.profile')
        if not auto_profile.is_file():
            raise RuntimeError('Can not find emulator profile')

        try:
            shutil.copy(str(self._cam_script), str(auto_profile))
        except Exception as e:
            raise RuntimeError('Error: {}'.format(e))

    def __emulator_connect(self):
        self._testlog('Try to connect TV to CAM emulator.\n')
        server_ip = network.get_pc_ip(self._tvip)

        if not server_ip:
            raise RuntimeError('Server IP was not got.')

        connect = soap_commands.cam_emulator_connect(self._tvip, server_ip)
        if not connect:
            raise RuntimeError('Connect to CAM emulator was not executed.')

        self._testlog('Successfull connect to CAM emulator\n')
