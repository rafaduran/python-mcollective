import copy

import pytest

import mcollective

from . import base as ibase
from .. import base


@pytest.fixture(scope='module')
def config():
    return mcollective.Config(base.TEST_CFG)


@pytest.fixture(scope="module",
                params=[(('agent', 'discovery'), ('action','ping'))])
def simple_rpc_action(request, config):
    params = dict(request.param)
    params.update({'config': config})
    return params

def pytest_runtest_setup(item):
    ctxt = copy.deepcopy(base.DEFAULT_CTXT)
    ctxt.update(ibase.CTXT)
    base.configfile(ctxt=ctxt)
