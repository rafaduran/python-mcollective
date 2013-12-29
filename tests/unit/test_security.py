"""Tests for Security Providers"""
import mock
import pytest

from pymco import security


def test_secuity_provider_is_abstract():
    """Tests SecurityProvider is an abstract class."""
    with pytest.raises(TypeError):
        security.SecurityProvider()


class FakeProvider(security.SecurityProvider):
    serializer = mock.Mock()

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
            FakeProvider.serializer.serialize.return_value)
    FakeProvider.serializer.serialize.assert_called_once_with(msg)


def test_deserialize(sec_provider):
    assert (sec_provider.deserialize(msg) ==
            FakeProvider.serializer.deserialize.return_value)
    FakeProvider.serializer.deserialize.assert_called_once_with(msg)
