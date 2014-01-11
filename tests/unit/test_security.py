"""Tests for Security Providers"""
import pytest

from pymco import security
from pymco.test.utils import mock


def test_secuity_provider_is_abstract():
    """Tests SecurityProvider is an abstract class."""
    with pytest.raises(TypeError):
        security.SecurityProvider()


class FakeProvider(security.SecurityProvider):
    def __init__(self, *args, **kwargs):
        super(FakeProvider, self).__init__(*args, **kwargs)
        self.serializer = mock.Mock()

    def sign(self, message):
        pass

    def verify(self, message):
        pass


@pytest.fixture
def sec_provider(config):
    return FakeProvider(config=config)


@pytest.fixture
def msg():
    return mock.Mock()


def test_serialize(sec_provider):
    assert (sec_provider.serialize(msg) ==
            sec_provider.serializer.serialize.return_value)
    sec_provider.serializer.serialize.assert_called_once_with(msg)


def test_deserialize(sec_provider):
    assert (sec_provider.deserialize(msg) ==
            sec_provider.serializer.deserialize.return_value)
    sec_provider.serializer.deserialize.assert_called_once_with(msg)


@mock.patch.object(FakeProvider, 'sign')
def test_encode(sign, sec_provider, msg):
    assert (sec_provider.encode(msg) ==
            sec_provider.serializer.serialize.return_value)
    sign.assert_called_once_with(msg)
    sec_provider.serializer.serialize.assert_called_once_with(
        sign.return_value)


@mock.patch.object(FakeProvider, 'verify')
def test_decode(verify, sec_provider, msg):
    assert sec_provider.decode(msg) == verify.return_value
    sec_provider.serializer.deserialize.assert_called_once_with(msg)
    verify.assert_called_once_with(
        sec_provider.serializer.deserialize.return_value)
