"""
:py:mod:`pymco.listeners`
-------------------------
stomp.py listeners for python-mcollective.
"""
import functools
import logging
import threading
import time

from stomp import listener

LOG = logging.getLogger(__name__)


class CurrentHostPortListener(listener.ConnectionListener):
    """Listener tracking current host and port.

    Some connectors, like ActiveMQ connector, may provide different user and
    password for each host, so we need track the current host and port in order
    to be able to get the right user and password when logging.
    """
    def __init__(self, *args, **kwargs):
        self.current_host = None
        self.curent_port = None

    def on_connecting(self, host_and_port):
        """Track current host and port.

        :arg host_and_port: A two-tuple with host as first element and port
            as the second.
        """
        self.current_host, self.current_port = host_and_port

    def get_host(self):
        """Return current host.

        :return: current host.
        """
        return self.current_host

    def get_port(self):
        """Return current host.

        :return: current port.
        """
        return self.current_port


class ResponseListener(listener.ConnectionListener):
    """Listener that waits for a message response.

    :arg config: :py:class:`pymco.config.Config` instance.
    :arg count: number of expected messages.
    :arg timeout: seconds we should wait for messages.
    :arg condition: by default a :py:class:`threading.Condition` object
        for synchronization purposes, but you can use any object
        implementing the :py:meth:`wait` method and accepting a ``timeout``
        argument.
    """
    def __init__(self, config, connector, count, timeout=30, condition=None,
                 logger=LOG):
        self.logger = logger
        self.config = config
        self.connector = connector
        self._security = None
        self.timeout = timeout
        if not condition:
            condition = threading.Condition()

        self.condition = condition
        self.received = 0
        self.responses = []
        self.count = count
        self.logger.debug("initializing ResponseListener, timeout={t}".format(t=timeout))

    @property
    def security(self):
        """Security provider property"""
        if not self._security:
            self._security = self.config.get_security()

        return self._security

    def on_message(self, headers, body):
        """Received messages hook.

        :arg headers: message headers.
        :arg body: message body.
        """
        self.logger.debug("on_message headers={h} body={b}".format(h=headers, b=body))
        self.condition.acquire()
        useb64 = self.connector.use_b64
        # TODO(jantman): for testing purposes at least, if an exception is raised when
        # decoding the message, we log the exception and continue on like we never got
        # the message.
        try:
            decoded = self.security.decode(body, b64=useb64)
            self.responses.append(decoded)
            self.received += 1
            self.condition.notify()
            self.condition.release()
        except Exception as e:
            self.logger.debug("Exception caught when decoding message body")
            self.logger.exception(e)

    def wait_on_message(self):
        """Wait until we get a message.

        :return: ``self``.
        """
        self.logger.debug("waiting until we receive a message")
        self.condition.acquire()
        self._wait_loop(self.timeout)
        self.logger.debug("left wait loop")
        self.condition.release()
        self.received = 0
        return self

    def _wait_loop(self, timeout):
        while self.received < self.count:
            init_time = time.time()
            self.condition.wait(timeout)
            current_time = time.time()
            timeout -= (current_time - init_time)
            if timeout <= 0:
                break


SingleResponseListener = functools.partial(ResponseListener, count=1)
