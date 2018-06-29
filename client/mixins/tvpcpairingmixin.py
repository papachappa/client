from client.utils.osutils import network
from client.utils.tv.soap_commands import disable_netlogging, enable_netlogging

from .basemixin import BaseMixin


class TVPCPairingMixin(BaseMixin):
    """ Mixin for performing pairing TV with test machine and enable logging """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tvip = None

    def _pair_tv_pc(self):
        server_ip = network.get_pc_ip(self._tvip)
        if not server_ip:
            msg = self._testlog('#WARN: Server IP was not got')
            raise RuntimeError(msg)
        try:
            self.__pair(server_ip)
        except:
            raise
        else:
            self._testlog('Pairing was done')

    def __pair(self, server_ip):
        pairing_result = self.__enable_logging(server_ip)

        if pairing_result == 1:
            # TV is already paired with another test station.
            self._testlog('Disable existing pairing')
            self._testlog(
                'ATTENTION! Serial log will contain full log '
                'from start of TV set'
            )

            try:
                disable_netlogging.turnLogOff(self._tvip, server_ip)
            except Exception as e:
                self._testlog(
                    '#WARN: Logging disabling returns exception ' + str(e)
                )

            pairing_result = self.__enable_logging(server_ip)

        if pairing_result != 0:
            self._testlog(
                'Result of paring is "{}". Logging will not be started'
                .format(pairing_result)
            )
            raise RuntimeError('TV was not paired')

    def __enable_logging(self, server_ip):
        self._testlog('Pair TV with PC...')
        try:
            pairing = enable_netlogging.turnLogOn(self._tvip, server_ip)
        except Exception as e:
            self._testlog('Logging was not enabled: ' + str(e))
            self._testlog('Test will be continue without log collection')
            raise
        else:
            return int(pairing)
