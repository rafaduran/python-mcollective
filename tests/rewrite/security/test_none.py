"""Test NoneProvider security provider"""
import pytest
import mock


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


def test_encode_delegates_to_yaml_serializer(security, msg):
    """Test NoneProvider delegates encode to YAML serialization"""
    with mock.patch.object(security.serializer, 'serialize') as ser:
        expected = 'some: yaml'
        ser.return_value = expected
        assert security.encode(msg) == expected
        ser.assert_called_once_with(msg)


def test_decode_delegates_to_yaml_serializer(security, msg):
    """Test NoneProvider delegates decode to YAML de-serialization"""
    with mock.patch.object(security.serializer, 'deserialize') as deser:
        expected = {'some': 'dict'}
        deser.return_value = expected
        assert security.decode(msg) == expected
        deser.assert_called_once_with(msg)
