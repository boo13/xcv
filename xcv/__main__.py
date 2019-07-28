# -*- coding: utf-8 -*-

import datetime
import pytz

from xcv.constants import TIMEZONE
startTime = datetime.datetime.now(tz=pytz.UTC).astimezone(pytz.timezone(TIMEZONE))

from cli import cli

import sys

sys.exit(cli.main_input())  # pragma: no cover


