from datetime import datetime, timedelta
import pytz
from loguru import logger


class Clock:
    """Simple wrapper of datetime.
    
    Delivers pretty-string versions of formatted timedeltas.
    """
    def __init__(self, timezone="US/Eastern"):
        self.timezone = timezone
        self._start = self.now()

    def now(self):
        return datetime.now(tz=pytz.UTC).astimezone(pytz.timezone(self.timezone))

    @property
    def elapsed(self):
        return self.now() - self._start

    @property
    def elapsed_no_microseconds(self):
        _e = self.elapsed
        return _e - timedelta(microseconds=_e.microseconds)

    @property
    def elapsed_seconds(self):
        _e = self.elapsed
        return int(_e.total_seconds())

    def reset(self):
        logger.debug("Clock Reset")
        self._start = self.now()


if __name__ == "__main__":
    from time import sleep

    c = Clock()
    sleep(2)
    print(f"Elapsed: {c.elapsed}")
    print(f"Elapsed Seconds: {c.elapsed_seconds}")
    print(f"Elapsed no microseconds: {c.elapsed_no_microseconds}")
