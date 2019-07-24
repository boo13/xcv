# -*- coding: utf-8 -*-
""" XCV - An open-source project to make py-2-serial communication, particularly to control hacked controllers/switches/GPIO-pins etc. 

Main entry point for the XCV module

"""

from cli import cli

import sys

sys.exit(cli.main_input())  # pragma: no cover
