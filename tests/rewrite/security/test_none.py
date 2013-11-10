"""Test NoneProvider security provider"""
import mock


@mock.patch('getpass.getuser')
def test_sign(getuser, none_security, msg):
    getuser.return_value = 'foo'
    signed = none_security.sign(msg)
    assert signed[':callerid'] == 'user=foo'
    getuser.assert_called_once_with()


def test_encode_delegates_to_yaml_serializer(none_security, msg):
    """Test NoneProvider delegates encode to YAML serialization"""
    with mock.patch.object(none_security.serializer, 'serialize') as ser:
        expected = 'some: yaml'
        ser.return_value = expected
        assert none_security.encode(msg) == expected
        ser.assert_called_once_with(msg)


def test_decode_delegates_to_yaml_serializer(none_security, msg):
    """Test NoneProvider delegates decode to YAML de-serialization"""
    with mock.patch.object(none_security.serializer, 'deserialize') as deser:
        expected = {'some': 'dict'}
        deser.return_value = expected
        assert none_security.decode(msg) == expected
        deser.assert_called_once_with(msg)
