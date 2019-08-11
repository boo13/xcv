# -*- coding: utf-8 -*-

"""Tests for `xcv` package."""

import pytest

from click.testing import CliRunner

import xcv

from xcv import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_cli_no_options_passed():
    no_options_passed_result = CliRunner().invoke(xcv.cli.main_input)
    assert no_options_passed_result.exit_code == 0
    assert 'No options passed.' in no_options_passed_result.output

def test_cli_option_help():
    help_result = CliRunner().invoke(cli.main_input, ["--help"])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output

# def test_cli_option_port():
#     port_result = CliRunner().invoke(cli.main_input, ["--port"])
#     assert port_result.exit_code == 0
#     assert 'Controller port, default is' in port_result.output

# def test_cli_option_gui():
#     gui_result = CliRunner().invoke(cli.main_input, ["--gui"])
#     assert gui_result.exit_code == 1
#     assert 'Show the GUI' in gui_result.output
