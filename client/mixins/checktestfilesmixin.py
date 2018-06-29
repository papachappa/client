from .basemixin import BaseMixin


class CheckTestFilesMixin(BaseMixin):
    """ Mixin for checking and printing in the header mandatory/optional test
        files. If mandatory files are absent will be raised error. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._test_script = None
        self._player_settings = None
        self._serial_log_setting = None
        self._precon_interpreter = None
        self._precon_script = None
        self._precon_player_settings = None
        self._standby = None
        self._standby_script = None
        self._timejump_script = None
        self._confirm_wakeup_script = None

    def _check_and_get_unique_script(self, path, postfix):
        """
            Will raise RuntimeException if no test files found or
            if found more than one
        """
        pattern = path.name + postfix

        try:
            script, *more = sorted(path.parent.glob(pattern))
        except ValueError:
            raise RuntimeError("Got no files with pattern '{}'.".format(pattern))

        if more:
            raise RuntimeError(
                "Got several files with same pattern '{}'.".format(pattern)
            )

        return script

    def check_test_files(self):
        mandatory, optional = self.__get_header_files()

        if any(mandatory):
            self._testlog('\nMandatory test files:')
            self._testlog('\n'.join(map(str, mandatory)))

            missing = list(filter(lambda x: not x.is_file(), mandatory))
            if any(missing):
                self._testlog('\nNext test files are not found:')
                self._testlog('\n'.join(map(str, missing)))
                raise RuntimeError('Mandatory test files are not found')

        if any(optional):
            self._testlog('\nOptional test files:')
            self._testlog('\n'.join(map(str, optional)))

    def __get_header_files(self):
        optional = []
        mandatory = []

        if self._test_script:
            mandatory.append(self._test_script)
        if self._player_settings:
            mandatory.extend(self._player_settings)
        if self._serial_log_setting:
            optional.append(self._serial_log_setting)

        if self._precon_interpreter:
            mandatory.append(self._precon_script)
            mandatory.extend(self._precon_player_settings)

        if self._standby:
            mandatory.append(self._standby_script)
            mandatory.append(self._timejump_script)
            mandatory.append(self._confirm_wakeup_script)

        mandatory = list(filter(None, mandatory))
        optional = list(filter(None, optional))

        return mandatory, optional
