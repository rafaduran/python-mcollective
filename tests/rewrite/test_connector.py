"""Tests for python-mcollective base."""
import pytest

from pymco import connector


def test_connector_is_abstract():
    """Tests Connector is an abstract class."""
    with pytest.raises(TypeError):
        connector.Connector()
