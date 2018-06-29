import time

from client.utils.tv.nonsoap_commands import ping
from client.utils.tv.soap_commands import get_chassis_info, tv_restart

from .basemixin import BaseMixin


class RebootTVMixin(BaseMixin):
    """ Mixin for performing TV reboot """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tvip = None

    def reboot_tv(self):
        self._testlog('\n--- Reboot TV ---')
        try:
            self.__reboot_tv()
        except Exception as e:
            self._testlog('Reboot failed. Reason: {}'.format(e))
            raise
        finally:
            self._testlog('--- Reboot TV (END)---')

    def __reboot_tv(self):
        try:
            tv_chassis, _ = get_chassis_info(self._tvip)
        except:
            raise

        self._testlog('TV chassis is recognized as ' + str(tv_chassis))

        try:
            reboot_result = tv_restart.tv_restart(self._tvip, tv_chassis)
        except:
            self._testlog('#WARN: Command to reboot TV returned error')
            reboot_result = None

        if reboot_result:
            self._testlog('Command to reboot TV sent successfully')
        else:
            self._testlog('#WARN: No successful response from TV')

        # make sure tv is off
        time.sleep(4)

        if ping.check_ip(self._tvip):
            raise RuntimeError('TV was not switched OFF')

        if not ping.check_ip(self._tvip, 120):
            raise RuntimeError('TV was not woke up')

        self._testlog('Wait 1 min to check TV is up and running')
        time.sleep(60)
