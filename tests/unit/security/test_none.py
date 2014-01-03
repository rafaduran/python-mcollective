"""Test NoneProvider security provider"""
import pytest

from pymco.test.utils import mock


@pytest.fixture
def security(config):
    from pymco.security import none
    return none.NoneProvider(config)


@mock.patch('getpass.getuser')
def test_sign(getuser, security, msg):
    getuser.return_value = 'foo'
    signed = security.sign(msg)
    assert signed[':callerid'] == 'user=foo'
    getuser.assert_called_once_with()


def test_verify_does_nothing(security, msg):
    assert security.verify(msg) == msg
