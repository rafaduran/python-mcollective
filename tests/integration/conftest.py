import pytest

from pymco.config import Config
from pymco import message
from pymco.test import ctxt as test_ctxt


@pytest.fixture
def config():
    return Config.from_configfile(test_ctxt.TEST_CFG)


@pytest.fixture
def ping_call_params(config, msg):
    params = dict(agent='discovery', action='ping', msg=msg, config=config)
    return params


@pytest.fixture
def msg(config):
    return message.Message(body=test_ctxt.MSG['body'],
                           agent=test_ctxt.MSG['agent'],
                           config=config)
