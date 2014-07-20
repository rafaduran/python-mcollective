from pymco import message
from pymco import rpc
from pymco.test import ctxt as test_ctxt
import pytest

from . import base


class TestMCllectiveSymbols(base.BaseIntegrationTestCase, base.MCollectiveCurrent):
    CTXT = {
        'plugin.activemq.pool.1.port': 61614,
        'plugin.activemq.pool.1.password': 'marionette',
    }

    @pytest.mark.timeout(method='thread', timeout=15)
    def test_symbols(self):
        body = {
            ':agent': 'demo',
            ':action': 'mounts',
            ':caller': 'user=rafaduran',
            ':data': {':process_results': True},
        }
        msg = message.Message(body=body, agent='demo', config=self.config)
        simple_rpc = rpc.SimpleAction(msg=msg,
                                      agent='demo',
                                      action='mounts',
                                      config=self.config)
        result = simple_rpc.call(timeout=15)
        assert len(result) == 1
        res_msg = result[0]
        assert res_msg['senderagent'] == 'demo'
        assert res_msg['requestid'] == msg[':requestid']

    def get_ctxt(self):
        ctxt = super(TestMCllectiveSymbols, self).get_ctxt()
        ctxt['libdir'] = ':'.join([
            ctxt['libdir'],
            '{root}/fixtures/plugins'.format(root=test_ctxt.ROOT),
        ])
        return ctxt
