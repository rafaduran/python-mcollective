"""Tests for pymco.serializers"""
import pytest

from pymco import serializers


def test_serializer_can_not_be_instantiated():
    """Tests pymco.serializers.SerializerBase  can't be instantiated."""
    with pytest.raises(TypeError):
        serializers.SerializerBase()
