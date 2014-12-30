"""Tests for pymco.security.ssl"""
import base64
import os

import pytest

from pymco import exc
from pymco.security import ssl
from pymco.test import ctxt
from pymco.test.utils import mock


@pytest.fixture
def ssl_provider(config):
    return ssl.SSLProvider(config=config)


@pytest.fixture
def hash_():
    txt = ''
    with open(os.path.join(ctxt.ROOT, 'fixtures/hash.txt'), 'rt') as file_:
        txt = file_.read()

    return txt


@pytest.fixture
def reply(hash_):
    return {
        'body': '--- pong\n...\n',
        'hash': hash_,
        'msgtime': 1388859129,
        'requestid': 'ZGRkZmRhNDhiMTFjZTJkM2YxNzliYWIyNWFlOWExZDM=',
        'senderagent': 'discovery',
        'senderid': 'mco1',
    }


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


@mock.patch('base64.b64encode')
@mock.patch('Crypto.Signature.PKCS1_v1_5.new')
@mock.patch('pymco.security.ssl.SSLProvider.private_key',
            new_callable=mock.PropertyMock)
@mock.patch('Crypto.Hash.SHA.new')
def test_get_hash(sha, private_key, signer, encode, ssl_provider, msg):
    assert ssl_provider.get_hash(msg) == encode.return_value

    private_key.assert_called_once_with()
    sha.assert_called_once_with(msg[':body'].encode('utf8'))
    signer.assert_called_once_with(private_key.return_value)
    encode.assert_called_with(signer.return_value.sign.return_value)


@mock.patch('Crypto.Signature.PKCS1_v1_5.new')
@mock.patch('pymco.security.ssl.SSLProvider.server_public_key',
            new_callable=mock.PropertyMock)
@mock.patch('Crypto.Hash.SHA.new')
def test_verify__ok(sha, server_public, verifier, ssl_provider, reply):
    assert ssl_provider.verify(reply) == reply
    sha.assert_called_once_with(reply['body'].encode('utf8'))
    verifier.assert_called_once_with(server_public.return_value)
    signature = base64.b64decode(reply['hash'])
    verifier.return_value.verify.assert_called_once_with(sha.return_value, signature)


@mock.patch('Crypto.Signature.PKCS1_v1_5.new')
@mock.patch('pymco.security.ssl.SSLProvider.server_public_key',
            new_callable=mock.PropertyMock)
@mock.patch('Crypto.Hash.SHA.new')
def test_verify__error(sha, server_public, verifier, ssl_provider, reply):
    verifier.return_value.verify.return_value = False
    with pytest.raises(exc.VerificationError):
        ssl_provider.verify(reply)
