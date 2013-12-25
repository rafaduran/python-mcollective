import pytest


@pytest.fixture
def stomp_connector(config_stomp, conn_mock):
    from pymco.connector import stomp
    return stomp.StompConnector(config_stomp, connection=conn_mock)
