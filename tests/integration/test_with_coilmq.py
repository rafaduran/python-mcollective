import pytest

import base

import mcollective


class TestWithCoilMQIntegration(base.TestCase, base.CoilMQIntegration):
    pass


class MCollectiveTests(object):
    def test_simple_agent(self, simple_rpc_action):
        agent = mcollective.SimpleRPCAction(**simple_rpc_action)
        # TODO (rafaduran): check length and content (currently broken)
        agent.send()


@pytest.mark.usefixture('simple_rpc_action')
class TestWithCoilMQ22x(TestWithCoilMQIntegration, MCollectiveTests):
    def setup(self):
        self.get_vendor_rev('2.2.x')
        super(TestWithCoilMQ22x, self).setup()

    def teardown(self):
        base.TestCase.teardown(self)


class TestWithCoilMQ20x(TestWithCoilMQIntegration, MCollectiveTests):
    def setup(self):
        self.get_vendor_rev('2.0.x')
        super(TestWithCoilMQ20x, self).setup()

    def teardown(self):
        base.TestCase.teardown(self)
