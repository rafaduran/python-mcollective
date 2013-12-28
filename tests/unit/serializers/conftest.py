import pytest


@pytest.fixture
def yaml():
    from pymco.serializers import yaml
    return yaml.Serializer()


@pytest.fixture
def yaml_response():
    return """---
:senderid: mco1
:requestid: 335a3e8261e4589499d366862b328816
:senderagent: discovery
:msgtime: 1384022186
:body: pong"""
