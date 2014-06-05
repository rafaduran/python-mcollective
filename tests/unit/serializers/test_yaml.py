"""Tests YAML serializer"""
import mock

from pymco.serializers import yaml as _yaml


def test_serialize(yaml, msg):
    """Test msg serialization"""
    assert yaml.serialize(msg) == """:agent: discovery
:body: ping
:collective: mcollective
:filter:
  agent: []
  cf_class: []
  compound: []
  fact: []
  identity: []
:msgtime: 123
:requestid: 6ef11a5053008b54c03ca934972fdfa45448439d
:senderid: mco1
:ttl: 60
"""


def test_deserialize(yaml, yaml_response):
    assert yaml.deserialize(yaml_response) == {
        ':senderid': 'mco1',
        ':requestid': '335a3e8261e4589499d366862b328816',
        ':senderagent': 'discovery',
        ':msgtime': 1384022186,
        ':body': 'pong',
    }


def test_symbol_constructor():
    loader, node = mock.Mock(), mock.Mock()
    assert _yaml.symbol_constructor(loader, node) == loader.construct_scalar.return_value
    loader.construct_scalar.assert_called_once_with(node)
