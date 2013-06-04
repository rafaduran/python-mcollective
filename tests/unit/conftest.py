# coding: utf-8
import os

from .. import base

def pytest_runtest_setup(item):
    base.configfile()
