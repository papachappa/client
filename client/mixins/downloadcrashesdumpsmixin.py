from pathlib import Path

from client.utils.tv.nonsoap_commands import dumps
from client.utils.tv.soap_commands import get_crash_logs

from .basemixin import BaseMixin


class DownloadCrashesDumpsMixin(BaseMixin):
    ''' Mixin for download crashes and dump files from TV '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tvip = None
        self._log_dir = None

    def get_crash_logs(self):
        try:
            crashlist = get_crash_logs.getList(self._tvip)
        except:
            raise

        if not crashlist:
            self._testlog('\nNo crash logs on TV')
            return

        log_dir = Path(self._log_dir, "crashes")
        log_dir.mkdir(parents=True, exist_ok=True)

        for crashitem in crashlist:
            self._testlog('Writing {}/{}'.format(log_dir, crashitem))
            crshfile_contain = get_crash_logs.getException(self._tvip, crashitem)

            crashfile = Path(log_dir, crashitem)
            with crashfile.open("w") as f:
                f.write(crshfile_contain)

    def get_dump_files(self):
        try:
            found_dumps = dumps.find_dumps(self._tvip)
        except:
            raise

        if not found_dumps:
            self._testlog('\nNo dump files on TV')
            return

        log_dir = Path(self._log_dir, "dumps")
        log_dir.mkdir(parents=True, exist_ok=True)

        for file in found_dumps:
            dumps.get_dumps(self._tvip, file, log_dir)
            self._testlog('Writing {}/{}'.format(log_dir, Path(file).name))
