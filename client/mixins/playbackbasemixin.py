from client.utils import general

from .basemixin import BaseMixin


class PlaybackBaseMixin(BaseMixin):
    """ Base mixin to inherit from for executing lstreamer """

    def _start_playbackbase(self, player_settings, playback_list):
        if not player_settings:
            self._testlog('Test does not require streaming.')
            return None

        text = 'Test requires playback of {} stream(s)'.format(
            len(player_settings)
        )
        self._testlog(text)

        # start all requested streams
        # if playback is not started stop the test.
        playback_list.extend(
            self.__start_lstreamer(ini) for ini in player_settings
        )

    def __start_lstreamer(self, ini):
        text = 'Trying to start playback of ' + str(ini)
        self._testlog(text)
        self._playerlog(text)

        try:
            p = general.start_lstreamer(ini, self._playerlog_fd)
        except Exception as e:
            self._testlog(
                'Playback of {} was not started, see player log.'
                .format(ini)
            )
            self._testlog('Reason: {}'.format(e))
            raise
        else:
            self._playerlog('\nPlayback was started')
            return p
