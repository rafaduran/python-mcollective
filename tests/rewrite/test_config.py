'''Tets for the configuration class'''
try:
    from unittest import mock
except ImportError:
    import mock

import pytest
from six.moves import configparser

from pymco import config
from pymco import exc

from .. import base


def test_init_error():
    with pytest.raises(exc.ImproperlyConfigured):
        config.Config()


def test_init_configstr(configstr):
    conf = config.Config(configstr=configstr)


def test_init_configfile():
    conf = config.Config(configfile=base.TEST_CFG)


def test_getint(config):
    assert config.getint('plugin.activemq.pool.size') == 1


def test_getint_missing(config):
    with pytest.raises(KeyError):
        config.getint('missing')


def test_getint_default(config):
    assert config.getint('missing', default=1) == 1


def test_getboolean(config):
    truly = ('y', 'true', '1')
    falsy = ('n', 'false', '0')
    for expected, values in ((True, truly), (False, falsy)):
        with mock.patch.dict(config.config,
                             dict([(val, val) for val in values])):
            for val in values:
                assert config.getboolean(val) == expected


def test_getboolean_missing(config):
    with pytest.raises(KeyError):
        config.getboolean('missing')


def test_getboolean_default(config):
    assert config.getboolean('missing', default=True) == True


def test_length(config):
    '''Test configuration length'''
    assert len(config) == len(config.config)


def test_iter(config):
    '''Test configuration iteration.'''
    assert list(config) == list(config.config)
