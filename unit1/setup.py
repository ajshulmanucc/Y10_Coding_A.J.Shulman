"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['LyricsTranslate.py']
DATA_FILES = ['--iconfile', 'native_lang.txt', 'native_lang_settings.txt', 'settings.png']
OPTIONS = {'iconfile': '/Users/ajshulman/Downloads/unit1/icon.icns'}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
