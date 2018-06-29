from client.utils.osutils import proc

from .playbackbasemixin import PlaybackBaseMixin


class PlaybackMixin(PlaybackBaseMixin):
    """ Mixin for executing lstreamer streams """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._player_settings = None

    def start_playback(self):
        self._testlog('\n--- Playback info ---')
        try:
            self._start_playbackbase(
                self._player_settings,
                self._lstreamer_proc['playback']
            )
        except:
            proc.terminate_processes(self._lstreamer_proc['playback'])
            raise RuntimeError('Playback was not started')
        finally:
            self._testlog('--- Playback info (END) ---')

    def stop_playback(self):
        proc.terminate_processes(self._lstreamer_proc['playback'])
