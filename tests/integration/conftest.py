import pytest

import mcollective

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
