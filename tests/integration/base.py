import threading
import os
import subprocess

from coilmq.auth import simple
from coilmq.tests import functional
import git

from .. import base

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VENDOR_PATH = os.path.join(ROOT, 'integration/vendor')
VENDOR = 'https://github.com/puppetlabs/marionette-collective.git'

BIND_ADDRESS = '127.0.0.1'
BIND_PORT = 6163

CTXT = {
    'collectives': ['mcollective'],
    'securityprovider': {
        'name': 'none',
        'options': {},
    },
    'connector': {
        'name': 'stomp',
        'options': {
            'host': 'localhost',
            'port': 61613,
            'user': 'guest',
            'password': 'guest',
        },
    },
}


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
            '--config',
            '{root}/server.cfg'.format(root=base.ROOT),
        ]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    def teardown_mcollective(self):
        self.proc.terminate()


# Most CoilMQ code is borrowed from CoilMQ functional tests
class CoilMQIntegration(IntegrationTestCaseMixin):
    def setup_server(self):
        self.clients = []
        self.server = None  # This gets set in the server thread.
        self.server_address = None # This gets set in the server thread.
        self.ready_event = threading.Event()

        addr_bound = threading.Event()
        def start_server():
            self.server = functional.TestStompServer(
                (BIND_ADDRESS, BIND_PORT),
                ready_event=self.ready_event,
                authenticator=simple.SimpleAuthenticator(
                    store={'mcollective': 'secret'}),
                queue_manager=self._queuemanager(),
                topic_manager=self._topicmanager())
            self.server_address = self.server.socket.getsockname()
            addr_bound.set()
            self.server.serve_forever()

        self.server_thread = threading.Thread(target=start_server, name='server')
        self.server_thread.start()
        self.ready_event.wait()
        addr_bound.wait()

    def _queuemanager(self):
        """
        Returns the configured L{QueueManager} instance to use.

        Can be overridden by subclasses that wish to change out any queue mgr parameters.

        @rtype: L{QueueManager}
        """
        return functional.QueueManager(
            store=functional.MemoryQueue(),
            subscriber_scheduler=functional.FavorReliableSubscriberScheduler(),
            queue_scheduler=functional.RandomQueueScheduler())

    def _topicmanager(self):
        """
        Returns the configured L{TopicManager} instance to use.

        Can be overridden by subclasses that wish to change out any topic mgr parameters.

        @rtype: L{TopicManager}
        """
        return functional.TopicManager()

    def teardown_server(self):
        for c in self.clients:
            print "Disconnecting %s" % c
            c.close()
        self.server.shutdown()
        self.server_thread.join()
        self.ready_event.clear()
        self.server.socket.close()
        del self.server_thread

    def _new_client(self, connect=True):
        """
        Get a new L{TestStompClient} connected to our test server.

        The client will also be registered for close in the tearDown method.

        @param connect: Whether to issue the CONNECT command.
        @type connect: C{bool}

        @rtype: L{TestStompClient}
        """
        client = functional.TestStompClient(self.server_address)
        self.clients.append(client)
        if connect:
            client.connect()
            r = client.received_frames.get(timeout=1)
            assert r.command == 'CONNECTED'
        return client


class TestCase(object):
    def setup(self):
        self.setup_server()
        self.setup_mcollective()

    def teardown(self):
        self.teardown_mcollective()
        self.teardown_server()
