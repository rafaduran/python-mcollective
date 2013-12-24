import mock
import pytest


@pytest.fixture
def conn_mock():
    return mock.Mock()


@pytest.fixture
def stomp_connector(config_stomp, conn_mock):
    from pymco.connector import stomp
    return stomp.StompConnector(config_stomp, connection=conn_mock)
