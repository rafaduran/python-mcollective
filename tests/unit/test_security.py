"""Tests for Security Providers"""
import pytest

from pymco import security


def test_secuity_provider_is_abstract():
    """Tests SecurityProvider is an abstract class."""
    with pytest.raises(TypeError):
        security.SecurityProvider()
