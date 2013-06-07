import pytest

from . import base

import mcollective


class TestWithRabbitMQ(base.TestCase):
    '''RabbitMQ integration test case.'''
    def setup(self):
        self.setup_mcollective()

    def teardown(self):
        self.teardown_mcollective()


class MCollectiveTests(object):
    '''MCollective integration test case.'''
    def test_simple_agent(self, simple_rpc_action):
        '''Tests simple RPC actions.'''
        agent = mcollective.SimpleRPCAction(**simple_rpc_action)
        result = agent.send()
        assert len(result) == 1
        msg = result[0]
        assert msg[':senderagent'] == simple_rpc_action['agent']
        assert msg[':requestid'] == agent.request[':requestid']


class TestWithRabbitMco22x(TestWithRabbitMQ, MCollectiveTests):
    '''Mcollective 2.2.x branch integration tests with RabbitMQ'''
    def setup(self):
        self.get_vendor_rev('2.2.x')
        super(TestWithRabbitMco22x, self).setup()


class TestWithRabbitMco20x(TestWithRabbitMQ, MCollectiveTests):
    '''Mcollective 2.0.x branch integration tests with RabbitMQ'''
    def setup(self):
        self.get_vendor_rev('2.0.x')
        super(TestWithRabbitMco20x, self).setup()
