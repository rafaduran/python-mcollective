"""Tests for pymco.security.ssl"""
import pytest

from pymco.security import ssl
from pymco.test.utils import mock


@pytest.fixture
def ssl_provider(config):
    return ssl.SSLProvider(config=config)


def test_caller_id(config, ssl_provider):
    caller_id = config['plugin.ssl_client_public'].split('/')[-1].split('.')[0]
    caller_id = 'cert={0}'.format(caller_id)
    assert ssl_provider.callerid == caller_id


def test_caller_id_caches(ssl_provider):
    caller_id = 'foo'
    ssl_provider._caller_id = caller_id
    assert ssl_provider.callerid == caller_id


@mock.patch('pymco.utils.load_rsa_key')
def test__load_rsa_key_delegates_to_utils(load_rsa_key,
                                          config,
                                          ssl_provider):
    ssl_provider.cache = None
    assert ssl_provider._load_rsa_key(key='plugin.ssl_server_public',
                                      cache=ssl_provider.cache) == load_rsa_key.return_value
    load_rsa_key.assert_called_once_with(config['plugin.ssl_server_public'])


@mock.patch('pymco.utils.load_rsa_key')
def test_server_public_key_caches(load_rsa_key, config, ssl_provider):
    server_public_key = mock.Mock()
    ssl_provider.cache = server_public_key
    assert ssl_provider._load_rsa_key(key='plugin.ssl_server_public',
                                      cache=ssl_provider.cache) == server_public_key
    assert load_rsa_key.called is False


@mock.patch('pymco.security.ssl.SSLProvider._load_rsa_key')
def test_server_public_key_delegates__load_rsa_key(load_rsa_key, ssl_provider):
    assert ssl_provider.server_public_key == load_rsa_key.return_value
    load_rsa_key.assert_called_once_with(key='plugin.ssl_server_public',
                                         cache=ssl_provider._server_public_key)


@mock.patch('pymco.security.ssl.SSLProvider._load_rsa_key')
def test_private_key_delegates__load_rsa_key(load_rsa_key, ssl_provider):
    assert ssl_provider.private_key == load_rsa_key.return_value
    load_rsa_key.assert_called_once_with(key='plugin.ssl_client_private',
                                         cache=ssl_provider._private_key)


@mock.patch('pymco.config.Config.get_serializer')
def test_serializer_delegates_to_config(get_serializer, ssl_provider):
    assert ssl_provider.serializer == get_serializer.return_value
    get_serializer.assert_called_once_with('plugin.ssl_serializer')


@mock.patch('pymco.security.ssl.SSLProvider.callerid',
            new_callable=mock.PropertyMock)
@mock.patch('pymco.security.ssl.SSLProvider.get_hash')
def test_sign(get_hash, callerid, ssl_provider, msg):
    signed_msg = ssl_provider.sign(msg)
    assert signed_msg[':callerid'] == callerid.return_value
    assert signed_msg[':hash'] == get_hash.return_value

    callerid.asert_called_once_with()
    get_hash.assert_called_once_with(msg)


@mock.patch('Crypto.Signature.PKCS1_v1_5.new')
@mock.patch('pymco.security.ssl.SSLProvider.private_key',
            new_callable=mock.PropertyMock)
@mock.patch('Crypto.Hash.SHA.new')
def test_get_hash(sha, private_key, signer, ssl_provider, msg):
    sign = signer.return_value.sign
    encode = sign.return_value.encode
    result = encode.return_value.replace.return_value.strip.return_value
    assert ssl_provider.get_hash(msg) == result

    private_key.assert_called_once_with()
    sha.assert_called_once_with(msg[':body'])
    signer.assert_called_once_with(private_key.return_value)
