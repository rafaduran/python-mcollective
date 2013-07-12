'''Tets for the configuration class'''
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


def test_get(config):
    assert config.get('identity') == 'mco1'


def test_get_missing(config):
    with pytest.raises(configparser.NoOptionError):
        config.get('missing')


def test_get_default(config):
    assert config.get('missing', default='1') == '1'


def test_getint(config):
    assert config.getint('plugin.activemq.pool.size') == 1


def test_getint_missing(config):
    with pytest.raises(configparser.NoOptionError):
        config.getint('missing')


def test_getint_default(config):
    assert config.getint('missing', default=1) == 1


def test_getboolean(config):
    assert config.getboolean('plugin.activemq.pool.1.ssl') == False
    # TODO(rafaduran): test 0/1/n/y/true


def test_getboolean_missing(config):
    with pytest.raises(configparser.NoOptionError):
        config.getboolean('missing')


def test_getboolean_default(config):
    assert config.getboolean('missing', default=True) == True
