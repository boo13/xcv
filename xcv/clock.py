from datetime import datetime
import pytz
from loguru import logger


class Clock:
    def __init__(self, timezone="US/Eastern"):
        self.timezone = timezone
        self._start = self.now()

    def now(self):
        return datetime.now(tz=pytz.UTC).astimezone(pytz.timezone(self.timezone))

    def elapsed(self):
        return self.now() - self._start

    def reset(self):
        logger.debug("Clock Reset")
        self._start = self.now()
