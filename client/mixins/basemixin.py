from subprocess import DEVNULL

from client.utils.osutils import proc


class BaseMixin():
    """ Base class to inherit/override/extend methods for mixins"""

    def __init__(self, *args, **kwargs):
        self._created_logs = set()
        self._processes = list()
        self._lstreamer_proc = {
            'playback': [],
            'precon_playback': []
        }

    def __enter__(self): return self
    def __exit__(self, *eargs):
        proc.terminate_processes(self._processes)
        proc.terminate_processes(self._lstreamer_proc['playback'])
        proc.terminate_processes(self._lstreamer_proc['precon_playback'])

    def _get_status_data(self): return None, [], []

    def _check_and_get_unique_script(self, *args, **kwargs):
        raise NotImplementedError('sorry your princess is in another castle(CheckTestFilesMixin)')

    def _testlog(self, text):   pass
    def _playerlog(self, text): pass
    def _seriallog(self, text): pass
    def _camlog(self, text):    pass

    @property
    def _testlog_fd(self):
        return DEVNULL

    @property
    def _testlog_r_fd(self):
        return DEVNULL

    @property
    def _playerlog_fd(self):
        return DEVNULL

    @property
    def _camlog_fd(self):
        return DEVNULL

    @property
    def _seriallog_fd(self):
        return DEVNULL
