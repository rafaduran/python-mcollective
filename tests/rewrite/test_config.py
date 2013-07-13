'''Tets for the configuration class'''
try:
    from unittest import mock
except ImportError:
    import mock

import pytest
from six.moves import configparser

from pymco import config as _config
from .. import base


def test_init_configfile():
    '''Tests :py:method:`Config.from_configfile` static method.'''
    conf = _config.Config.from_configfile(configfile=base.TEST_CFG)
    assert conf['connector'] == 'activemq'


def test_get(config):
    '''Tests :py:method:`Config.get` happy path.'''
    assert config.get('connector') == 'activemq'


def test_get_missing(config):
    '''Tests :py:method:`Config.get` bad path.'''
    with pytest.raises(KeyError):
        config.get('missing')


def test_get_default(config):
    '''Tests :py:method:`Config.get` bad path with default.'''
    assert config.get('missing', default='activemq') == 'activemq'


def test_getint(config):
    '''Tests :py:method:`Config.getint` happy path.'''
    assert config.getint('plugin.activemq.pool.size') == 1


def test_getint_missing(config):
    '''Tests :py:method:`Config.getint` bad path.'''
    with pytest.raises(KeyError):
        config.getint('missing')


def test_getint_default(config):
    '''Tests :py:method:`Config.getint` bad path with default.'''
    assert config.getint('missing', default=1) == 1


def test_getboolean(config):
    '''Tests :py:method:`Config.getboolean` happy path.'''
    truly = ('y', 'true', '1')
    falsy = ('n', 'false', '0')
    for expected, values in ((True, truly), (False, falsy)):
        with mock.patch.dict(config.config,
                             dict([(val, val) for val in values])):
            for val in values:
                assert config.getboolean(val) == expected


def test_getboolean_missing(config):
    '''Tests :py:method:`Config.getboolean` bad path.'''
    with pytest.raises(KeyError):
        config.getboolean('missing')


def test_getboolean_default(config):
    '''Tests :py:method:`Config.getboolean` bad path with default.'''
    assert config.getboolean('missing', default=True) == True


def test_length(config):
    '''Test configuration length'''
    assert len(config) == len(config.config)


def test_iter(config):
    '''Test configuration iteration.'''
    assert list(config) == list(config.config)
