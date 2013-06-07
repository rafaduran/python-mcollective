'''Common helpers for integration tests.'''
import threading
import os
import signal
import subprocess
import time

import git

from .. import base

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VENDOR_PATH = os.path.join(ROOT, 'integration/vendor')
VENDOR = 'https://github.com/puppetlabs/marionette-collective.git'

CTXT = {
    'daemonize': 1,
    'collectives': ['mcollective'],
    'securityprovider': {
        'name': 'none',
        'options': {},
    },
    'connector': {
        'name': 'stomp',
        'options': {
            'host': '127.0.0.1',
            'port': 61613,
            'user': 'guest',
            'password': 'guest',
        },
    },
}
PIDFILE = '{root}/mco.pid'.format(root=base.ROOT)


class IntegrationTestCaseMixin(object):
    def get_vendor_rev(self, rev):
        if not os.path.exists(VENDOR_PATH):
            repo = git.Repo.clone_from(VENDOR, VENDOR_PATH)
        else:
            repo = git.Repo(VENDOR_PATH)

        if repo.active_branch.name == rev:
            return

        gcmd = git.cmd.Git(VENDOR_PATH)
        gcmd.checkout(rev)
        gcmd.pull()

    def setup_mcollective(self):
        """Runs MCollective in an out-of-process shell"""
        cmd = [
            'ruby',
            '-I',
            '{root}/integration/vendor/lib'.format(root=base.ROOT),
            '-I',
            '{root}/fixtures/plugins/'.format(root=base.ROOT),
            '{root}/integration/vendor/bin/mcollectived'.format(root=base.ROOT),
            '--pidfile',
            PIDFILE,
            '--config',
            '{root}/server.cfg'.format(root=base.ROOT),
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        assert proc.returncode == 0
        time.sleep(2)

    def teardown_mcollective(self):
        pid = int(open(PIDFILE, 'rt').read())
        os.kill(pid, signal.SIGTERM)


class TestCase(IntegrationTestCaseMixin):
    '''Base test case stub.'''
