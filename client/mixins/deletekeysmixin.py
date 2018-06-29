from client.utils.tv.soap_commands import delete_loreg_keys

from .basemixin import BaseMixin


class DeleteLoregKeys(BaseMixin):
    """ Mixin for performing deletion of loreg keys. By that imitating
        TV factory reset """
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tvip = None

    def _delete(self):
        try:
            res = delete_loreg_keys.delete_keys(self._tvip)
        except:
            raise
        else:
            return res
