"""
:mod:`pymco.config`
-------------------
Provides MCollective configuration parsing and an entry point for getting the
right plugin classes.
"""
import collections
import functools
import logging
import os
import socket

import six
from six.moves import configparser

from .connector import Connector
from .import exc
from .security import SecurityProvider
from .serializers import SerializerBase
from . import utils

LOG = logging.getLogger(__name__)
INFINITE = 9999999999999999999


def lookup_with_default(fnc):
    """
    Wraps ConfigParser lookups, catching exceptions and providing defaults.

    :arg fnc: Function to be decorated.
    """
    @functools.wraps(fnc)
    def decorator(self, name, *args, **kwargs):
        try:
            return fnc(self, name)
        except KeyError as exception:
            if 'default' in kwargs:
                return kwargs['default']
            raise exception
    return decorator


class Config(collections.Mapping):
    """python-mcollective confiugration class.

    :arg dict configdict: a dictionary like object containing configuration as key
        values.
    """
    def __init__(self, configdict, logger=LOG):
        self.config = configdict
        # The mcollective docs state that identity should default to hostname
        # when not explicitly set
        if not self.config.get('identity'):
            self.config['identity'] = socket.gethostname()
        self.logger = logger
        self.logger.debug("initialized Config")

    def __len__(self):
        return len(self.config)

    def __iter__(self):
        return six.iterkeys(self.config)

    def __getitem__(self, key):
        return self.config[key]

    @lookup_with_default
    def get(self, key):
        """Get option by key.

        :arg key: key to look for.
        """
        return self.__getitem__(key)

    @lookup_with_default
    def getint(self, key):
        """Get int option by key.

        :arg key: key to look for.
        """
        return int(self.__getitem__(key))

    @lookup_with_default
    def getfloat(self, key):
        """Get float option by key.

        :arg key: key to look for.
        """
        return float(self.__getitem__(key))

    @lookup_with_default
    def getboolean(self, key):
        """Get bool option by key.

        Acceptable truly values are: true, y, 1 and yes, thought MCollective
        only officially supports 1.

        :arg key: key to look for.
        """
        value = self.__getitem__(key)
        if isinstance(value, six.string_types):
            if value.lower() in ('true', 'y', '1', 'yes'):
                value = True
            else:
                value = False
            return bool(value)

    def get_connector(self):
        """Get connector based on MCollective settings."""
        import_path = Connector.plugins[self.config['connector']]
        self.logger.debug("connector import path: {i}".format(i=import_path))
        return utils.import_object(import_path, config=self)

    def get_security(self):
        """Get security plugin based on MCollective settings."""
        import_path = SecurityProvider.plugins[self.config['securityprovider']]
        self.logger.debug("securityprovider import path: {i}".format(i=import_path))
        return utils.import_object(import_path, config=self)

    def get_serializer(self, key):
        """Get serializer based on MCollective settings."""
        import_path = SerializerBase.plugins[self.config[key]]
        self.logger.debug("serializer import path: {i}".format(i=import_path))
        return utils.import_object(import_path)

    def get_host_and_ports(self):
        """Get all hosts and port pairs for the current configuration.

        The result must follow the :py:class:`stomp.Connection`
        ``host_and_ports`` parameter.

        :return: Iterable of two-tuple where the first element
            is the host and the second is the port.
        """
        if self.config['connector'] == 'stomp':
            return [(self.config['plugin.stomp.host'], self.getint('plugin.stomp.port'))]

        prefix = 'plugin.{connector}.pool.'.format(
            connector=self.config['connector'])
        host_key = prefix + '{index}.host'
        port_key = prefix + '{index}.port'
        host_and_ports = []

        for index in range(1, self.getint(prefix + 'size') + 1):
            host_and_ports.append((self.config[host_key.format(index=index)],
                                   self.getint(port_key.format(index=index))))

        return host_and_ports

    def get_user_and_password(self, current_host_and_port=None):
        """Get the user and password for the current host and port.

        :arg current_host_and_port: two-tuple iterable where the first element is the
            host and second is the port. This parameter is not required for
            :py:class:`pymco.connector.stomp.StompConnector` connector.
        :return: Two-tuple where the first element is the user and the second is
            the password for the given host and port.
        :raise ValueError: if connector isn't ``stomp`` and
            ``host_and_port`` is not provided.
        :raise pymco.exc.ConfigLookupError: if host and port are not
            found into the connector list of host and ports.
        """
        connector = self.config['connector']
        if connector == 'stomp':
            return self.config['plugin.stomp.user'], self.config['plugin.stomp.password']
        elif current_host_and_port is None:
            raise ValueError('"host_and_port" parameter is required for {0} '
                             'connector'.format(connector))

        for index, host_and_port in enumerate(self.get_host_and_ports(), 1):
            if host_and_port == current_host_and_port:
                prefix = 'plugin.{connector}.pool.'.format(
                    connector=self.config['connector'])
                user_key = prefix + '{index}.user'
                pass_key = prefix + '{index}.password'
                return (self.config[user_key.format(index=index)],
                        self.config[pass_key.format(index=index)])
        else:
            raise exc.ConfigLookupError(
                '{0} is not in the configuration for {1} connector'.format(
                    current_host_and_port, connector))

    def get_ssl_params(self):
        """Get SSL configuration for current connector

        :return: An iterable of SSL configuration parameters to be
            used with :py:meth:`stomp.Transport.set_ssl`.
        """
        connector = self.config['connector']
        if connector not in ('activemq', 'rabbitmq'):
            return ()

        params = []
        prefix = 'plugin.{0}.pool'.format(connector)
        for index in range(1, self.getint(prefix + '.size') + 1):
            current_prefix = '{prefix}.{index}'.format(prefix=prefix,
                                                       index=index)
            for_hosts = ((self.config.get(current_prefix + '.host'),
                          self.getint(current_prefix + '.port')),)
            current_prefix += '.ssl'
            if self.getboolean(current_prefix, default=False):
                params.append({
                    'for_hosts': for_hosts,
                    'cert_file': self.config.get(current_prefix + '.cert',
                                                 None),
                    'key_file': self.config.get(current_prefix + '.key', None),
                    'ca_certs': self.config.get(current_prefix + '.ca', None),
                })

        return params

    def get_conn_params(self):
        """Get STOMP connection parameters for current configuration.

        :return: Dictionary with stomp.py connection like key/values.
        """
        connector = self.config['connector']
        prefix = 'plugin.{0}.'.format(connector)

        if connector == 'stomp':
            return {'host_and_ports': self.get_host_and_ports()}

        return {
            'host_and_ports': self.get_host_and_ports(),
            'reconnect_sleep_initial':
            self.getfloat(prefix + 'initial_reconnect_delay', default=0.01),
            # 'reconnect_sleep_increase': ,
            # 'reconnect_sleep_jitter': ,
            'reconnect_sleep_max':
            self.getfloat(prefix + 'max_reconnect_delay', default=30.0),
            # Stomp gem, by default, try an infinite number of times
            # Stomp.py doesn't support it, so just use a really big number
            'reconnect_attempts_max':
            self.getfloat(prefix + 'max_reconnect_attempts', default=INFINITE),
            'timeout':
            self.getfloat(prefix + 'timeout', default=None),
        }

    @staticmethod
    def from_configfile(configfile):
        """Reads configfile and returns a new :py:class:`Config` instance

        :arg configfile: path to the configuration file to be parsed.
        :return: :py:class:`Config` instance.
        """
        configstr = open(configfile, 'rt').read()
        return Config.from_configstr(configstr)

    @staticmethod
    def from_configstr(configstr, section='default'):
        """Parses given string an returns a new :py:class:`Config` instance

        :arg configstr: configuration file content as string.
        :arg section: dummy section to be used for parsing configuration as
            INI file.
        :return: :py:class:`Config` instance.
        """
        config = six.StringIO()
        config.write('[{0}]\n'.format(section))
        config.write(configstr)
        config.seek(0, os.SEEK_SET)
        parser = configparser.ConfigParser()
        parser.readfp(config)
        return Config(dict(parser.items(section)))
