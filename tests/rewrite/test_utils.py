"""Tests for pymco.utils"""
import collections
import os

import pytest
import six

from pymco import utils
from pymco.test.utils import mock


@pytest.fixture
def client_public():
    path = os.path.join(os.path.dirname(__file__),
                        os.path.pardir,
                        'fixtures',
                        'client-public.pem')
    with open(path, 'rt') as cpf:
        content = cpf.read()

    return content


def test_import_class():
    assert utils.import_class('collections.defaultdict') is collections.defaultdict


def test_import_path__raises_import_error__missing_module():
    with pytest.raises(ImportError):
        utils.import_class('foo.spam')


def test_import_path__raises_import_error__missing_class():
    with pytest.raises(ImportError):
        utils.import_class('collections.spam')


def test_import_path_raises_import_error_bad_string():
    with pytest.raises(ImportError):
        utils.import_class('foo')


@mock.patch.object(utils, 'import_class')
def test_import_object_delegates_to_import_class(import_class):
    assert utils.import_object('foo.spam') == import_class.return_value.return_value
    import_class.assert_called_once_with('foo.spam')


@mock.patch.object(utils, 'import_class')
def test_import_object_instantiate_with_the_right_arguments(import_class):
    utils.import_object('foo.spam', 1, foo='spam')
    import_class.return_value.assert_called_once_with(1, foo='spam')


@mock.patch.object(six.moves.builtins, 'open')
@mock.patch('Crypto.PublicKey.RSA.importKey')
def test_load_rsa_key_delegates_to_importKey(import_key, open_, client_public):
    open_.return_value.__enter__.return_value.read.return_value = client_public
    assert utils.load_rsa_key('path/to/public.pem') == import_key.return_value
    open_.assert_called_once_with('path/to/public.pem', 'rt')
    import_key.assert_called_once_with(client_public)
