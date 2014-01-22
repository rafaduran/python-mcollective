'''Tets for the configuration class'''
import pytest

from pymco import config as _config
from pymco.exc import ConfigLookupError
from pymco.test import ctxt
from pymco.test.utils import mock


def test_init_configfile():
    '''Tests :py:method:`Config.from_configfile` static method.'''
    conf = _config.Config.from_configfile(configfile=ctxt.TEST_CFG)
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
    assert config.getboolean('missing', default=True)


def test_length(config):
    '''Test configuration length'''
    assert len(config) == len(config.config)


def test_iter(config):
    '''Test configuration iteration.'''
    assert list(config) == list(config.config)


@mock.patch('pymco.utils.import_object')
def test_get_connector(import_object, config):
    with mock.patch.dict('pymco.connector.Connector.plugins',
                         {'activemq': 'connector.foo.FooConnector'}):
        assert config.get_connector() == import_object.return_value
        import_object.assert_called_once_with('connector.foo.FooConnector',
                                              config=config)


@mock.patch('pymco.utils.import_object')
def test_get_security(import_object, config):
    with mock.patch.dict('pymco.security.SecurityProvider.plugins',
                         {'ssl': 'security.foo.FooProvider'}):
        assert config.get_security() == import_object.return_value
        import_object.assert_called_once_with('security.foo.FooProvider',
                                              config=config)


@mock.patch('pymco.utils.import_object')
def test_get_serializer(import_object, config):
    with mock.patch.dict('pymco.serializers.SerializerBase.plugins',
                         {'yaml': 'serializer.foo.FooSerializer'}):
        assert config.get_serializer('plugin.ssl_serializer'
                                     ) == import_object.return_value
        import_object.assert_called_once_with('serializer.foo.FooSerializer')


def test_get_host_and_ports(config):
    assert config.get_host_and_ports() == [('localhost', 6163)]


def test_get_host_and_ports_stomp(config):
    with mock.patch.dict(config.config, {'connector': 'stomp',
                                         'plugin.stomp.host': 'host',
                                         'plugin.stomp.port': '6163'}):
        assert config.get_host_and_ports() == [('host', 6163)]


def test_get_user_and_password(config):
    assert ('mcollective', 'secret') == config.get_user_and_password(
        ('localhost', 6163))


def test_get_user_and_password__raises_value_error(config):
    with pytest.raises(ValueError):
        config.get_user_and_password()


def test_get_user_and_password__raises_config_lookup_error(config):
    with pytest.raises(ConfigLookupError):
        config.get_user_and_password(('host', 345))


def test_get_ssl_parameters(config):
    assert {'use_ssl': True,
            'ssl_cert_file': 'tests/fixtures/activemq_cert.pem',
            'ssl_key_file': 'tests/fixtures/activemq_private.pem',
            'ssl_ca_certs': 'tests/fixtures/ca.pem'
            } == config.get_ssl_parameters(('localhost', 6163))


def test_get_ssl_parameters__no_ssl(config):
    del config.config['plugin.activemq.pool.1.ssl.ca']
    del config.config['plugin.activemq.pool.1.ssl.key']
    del config.config['plugin.activemq.pool.1.ssl.cert']
    del config.config['plugin.activemq.pool.1.ssl']
    assert {'use_ssl': False,
            'ssl_cert_file': None,
            'ssl_key_file': None,
            'ssl_ca_certs': None,
            } == config.get_ssl_parameters(('localhost', 6163))


def test_get_ssl_parameters__no_activemq(config):
    config.config['connector'] = 'stomp'
    with pytest.raises(ValueError):
        config.get_ssl_parameters(('localhost', 6163))
