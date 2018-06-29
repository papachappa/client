import datetime
import time

from .basemixin import BaseMixin


class TimeoutMixin(BaseMixin):
    """ Mixin for performing timeouts. For example between test runs """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._timeout = None

    def execute_timeout(self):
        for i in range(self._timeout, 0, -1):
            time.sleep(1)
            if i % 60 != 0:
                continue
            t = datetime.timedelta(seconds=i)
            self._testlog('Sleeping for {} (h:mm:ss) time'.format(t))
