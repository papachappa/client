from client.utils.osutils import proc

from .playbackbasemixin import PlaybackBaseMixin


class PreconPlaybackMixin(PlaybackBaseMixin):
    """ Mixin for executing precondition lstreamer streams """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._precon_player_settings = None

    def start_precon_playback(self):
        self._testlog('\n--- Precondition playback info ---')
        try:
            self._start_playbackbase(
                self._precon_player_settings,
                self._lstreamer_proc['precon_playback']
            )
        except:
            proc.terminate_processes(self._lstreamer_proc['precon_playback'])
            raise RuntimeError('Precondition playback was not started')
        finally:
            self._testlog('--- Precondition playback info (END) ---')

    def stop_precon_playback(self):
        proc.terminate_processes(self._lstreamer_proc['precon_playback'])
