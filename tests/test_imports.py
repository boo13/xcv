import pytest

def test_imports():
    try:
        import cv2
        import numpy
        import loguru
        import mypy
        import black
        import serial
        import click
        import PyQt5
        import PySimpleGUIQt
        import pytz
        import streamlink
    except:
        raise

    assert True


def test_RaiseErrors():
    with pytest.raises(ImportError):
        import cv
