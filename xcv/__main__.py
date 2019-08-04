# -*- coding: utf-8 -*-

import datetime
import pytz
from xcv.settings import Settings

startTime = datetime.datetime.now(tz=pytz.UTC).astimezone(
    pytz.timezone(Settings.TIMEZONE)
)

from cli import cli

import sys

sys.exit(cli.main_input())  # pragma: no cover

