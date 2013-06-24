'''Tets for the configuration class'''
import pytest

from pymco import config
from pymco import exc


def test_init_error():
    with pytest.raises(exc.ImproperlyConfigured):
        config.Config()


def test_init_configstr(configstr):
    conf = config.Config(configstr=configstr)


def test_get(config):
    assert config.get('identity') == 'mco1'
