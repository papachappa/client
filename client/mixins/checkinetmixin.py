from client.utils.tv.nonsoap_commands import ping

from .basemixin import BaseMixin


class CheckInetMixin(BaseMixin):
    """ Mixin for check internet availability from TV. It has predefined
        resources to ping that can be changed on demand. """

    def __init__(self, params, *args, **kwargs):
        super().__init__(params, *args, **kwargs)

        self._tvip = None
        self.__resource = ('www.google.ru', 'www.google.de', 'youtube.com')

    def _ping_resource(self):
        for site in self.__resource:
            unsucceed_percent = ping.ping_resource(self._tvip, site)

            if unsucceed_percent == 0:
                self._testlog('Resource {} pinged successfully'.format(site))
            elif unsucceed_percent == 100:
                raise RuntimeError('Ping to site {} failed'.format(site))
            else:
                raise RuntimeError(
                    'Some of the packets to {} not get to destination.'
                    .format(site)
                )
