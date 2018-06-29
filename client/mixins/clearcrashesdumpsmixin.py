from client.utils.tv.nonsoap_commands import dumps
from client.utils.tv.soap_commands import clear_crash_logs

from .basemixin import BaseMixin


class ClearCrashesDumpsMixin(BaseMixin):
    """ Mixin for clearing crashes and dump files from TV """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tvip = None

    def clear_dump_files(self):
        try:
            found_dumps = dumps.find_dumps(self._tvip)
        except:
            raise

        if not found_dumps:
            self._testlog('\nNo dumps found')
            return

        for file in found_dumps:
            self._testlog('Clearing ' + file)
            dumps.clear_dumps(self._tvip, file)

    def clearing_crash_logs(self):
        try:
            res = clear_crash_logs.deleteExceptions(self._tvip).strip()
        except:
            raise

        if res == "0":
            self._testlog("\nCrash files deleted")
        elif res == "-1":
            self._testlog("\nNo crash files found")
        else:
            raise Exception('Removal of crash files failed')
