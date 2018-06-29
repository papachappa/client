from client.utils.tv.nonsoap_commands import dumps

from .basemixin import BaseMixin


class TVServiceListMixin(BaseMixin):
    """ Mixin for getting service list from TV and saving to test machine"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tvip = None
        self._service_list_path = None
        self.__remote_path = '/var/local/loewe/servicelist.db'

    def get_service_list(self):
        try:
            dumps.get_dumps(
                self._tvip, self.__remote_path, self._service_list_path
            )
        except:
            raise
