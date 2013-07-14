'''Tests for :py:mod:`pymco.serializers`.'''
try:
    from unittest import mock
except ImportError:
    import mock

from pymco import serializers


def test_load_serializers():
    '''Tests :py:func:`pymco.serializers._load_serializer'''
    with mock.patch('importlib.import_module') as mocked:
        yaml = mock.Mock()
        mocked.return_value = yaml
        assert serializers._load_serializers() == {
            'yaml': yaml,
        }
        mocked.assert_called_with('pymco.serializers.yaml')


def test_get_deserializer():
    '''Tests :py:func:`pymco.serializers.get_deserializer'''
    des = mock.Mock()
    yaml = mock.Mock(Deserializer=des)
    with mock.patch.dict(serializers._SERIALIZERS, {'yaml': yaml}):
        assert serializers.get_deserializer('yaml') == des


def test_get_serializer():
    '''Tests :py:func:`pymco.serializers.get_serializer'''
    ser = mock.Mock()
    yaml = mock.Mock(Serializer=ser)
    with mock.patch.dict(serializers._SERIALIZERS, {'yaml': yaml}):
        assert serializers.get_serializer('yaml') == ser


def test_get_serializer_formats():
    '''Tests :py:func:`pymco.serializers.get_serializer_formats'''
    with mock.patch.dict(serializers._SERIALIZERS, {'yaml': 'whatever'}):
        assert list(serializers.get_serializer_formats()) == ['yaml']
