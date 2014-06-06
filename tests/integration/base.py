'''Common helpers for integration tests.'''
from __future__ import print_function
import os
import signal
import subprocess
import sys
import traceback
import time

from pymco import config
from pymco import message
from pymco import rpc
from pymco.test import ctxt as test_ctxt
from pymco.test import utils

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VENDOR_PATH = os.path.join(ROOT, 'integration/vendor')
VENDOR = 'https://github.com/puppetlabs/marionette-collective.git'
PIDFILE = '{root}/mco.pid'.format(root=test_ctxt.ROOT)

CTXT = {
    'daemonize': 1,
    'securityprovider': 'none',
    'collectives': ['mcollective'],
    'topicprefix': None,
}


class BaseIntegrationTestCase(object):
    def setup_cfg(self):
        ctxt = self.get_ctxt()
        utils.configfile(ctxt=ctxt)
        self.config = config.Config.from_configfile(test_ctxt.TEST_CFG)

    def setup_mcollective(self):
        """Runs MCollective in an out-of-process shell"""
        self.setup_cfg()
        cmd = [
            'ruby',
            '-I',
            '{root}/integration/vendor_{rev}/lib'.format(root=test_ctxt.ROOT,
                                                         rev=self.rev),
            '-I',
            '{root}/fixtures/plugins/'.format(root=test_ctxt.ROOT),
            '{root}/integration/vendor_{rev}/bin/mcollectived'.format(
                root=test_ctxt.ROOT,
                rev=self.rev,
            ),
            '--pidfile',
            PIDFILE,
            '--config',
            '{root}/server.cfg'.format(root=test_ctxt.ROOT),
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        assert proc.returncode == 0
        time.sleep(2)

    def teardown_mcollective(self):
        pid = int(open(PIDFILE, 'rt').read())
        os.kill(pid, signal.SIGTERM)

    def dump_threads(self):
        """Dump all threads information for debugging purposes.

        Recipe taken from http://stackoverflow.com/a/7317379/2832939
        """
        print("\n*** STACKTRACE - START ***\n", file=sys.stderr)
        code = []
        for threadId, stack in sys._current_frames().items():
            code.append("\n# ThreadID: %s" % threadId)
            for filename, lineno, name, line in traceback.extract_stack(stack):
                code.append('File: "%s", line %d, in %s' % (filename,
                                                            lineno, name))
                if line:
                    code.append("  %s" % (line.strip()))

        for line in code:
            print(line, file=sys.stderr)
        print("\n*** STACKTRACE - END ***\n", file=sys.stderr)

    def setup(self):
        self.setup_mcollective()

    def teardown(self):
        self.teardown_mcollective()

    def get_ctxt(self):
        ctxt = test_ctxt.DEFAULT_CTXT.copy()
        ctxt.update(CTXT)
        ctxt.update(self.CTXT)
        ctxt.update({'libdir':
                     '{root}/integration/vendor_{rev}/plugins'.format(
                         root=test_ctxt.ROOT,
                         rev=self.rev)})
        return ctxt


class IntegrationTestCase(BaseIntegrationTestCase):
    def ping_call_params(self):
        self.msg = message.Message(body=test_ctxt.MSG['body'],
                                   agent=test_ctxt.MSG['agent'],
                                   config=self.config)
        return dict(agent='discovery',
                    action='ping',
                    msg=self.msg,
                    config=self.config)

    def test_ping_call(self):
        '''Tests simple RPC actions.'''
        simple_action = rpc.SimpleAction(**self.ping_call_params())
        result = simple_action.call()
        # Only one agent running, but it might send multiple pings
        assert len(result) >= 1
        msg = result[0]
        assert msg[':senderagent'] == simple_action.agent
        assert msg[':requestid'] == self.msg[':requestid']


class MCollective22x(object):
    '''Mcollective 2.2.x branch integration tests with RabbitMQ'''
    rev = '2.2.x'


class MCollective23x(object):
    '''Mcollective 2.3.x branch integration tests with RabbitMQ'''
    rev = '2.3.x'


class MCollective20x(object):
    '''Mcollective 2.0.x branch integration tests with RabbitMQ'''
    rev = '2.0.x'


class MCollective24x(object):
    '''Mcollective 2.4.x branch integration tests'''
    rev = '2.4.x'


class MCollectiveCurrent(object):
    '''Mcollective current version branch integration tests'''
    rev = '2.4.x'
