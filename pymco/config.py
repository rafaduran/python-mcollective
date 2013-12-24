'''python-mcollective configuration module'''
import collections
import functools
import os

import six
from six.moves import configparser

from .connector import Connector
from .security import SecurityProvider
from .serializers import SerializerBase
from . import utils


def lookup_with_default(fnc):
    '''
    Wraps ConfigParser lookups, catching exceptions and providing defaults.
    '''
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
    '''python-mcollective confiugration class.'''
    def __init__(self, configdict):
        self.config = configdict

    def __len__(self):
        return len(self.config)

    def __iter__(self):
        return six.iterkeys(self.config)

    def __getitem__(self, key):
        return self.config[key]

    @lookup_with_default
    def get(self, key):
        '''Get option by key.'''
        return self.__getitem__(key)

    @lookup_with_default
    def getint(self, key):
        '''Get int option by key.'''
        return int(self.__getitem__(key))

    @lookup_with_default
    def getboolean(self, key):
        '''Get bool option by key.'''
        value = self.__getitem__(key)
        if isinstance(value, six.string_types):
            if value.lower() in ('true', 'y', '1'):
                value = True
            else:
                value = False
            return bool(value)

    def get_connector(self):
        """Get connector based on MCollective settings."""
        import_path = Connector.plugins[self.config['connector']]
        return utils.import_object(import_path, config=self)

    def get_security(self):
        """Get security plugin based on MCollective settings."""
        import_path = SecurityProvider.plugins[self.config['securityprovider']]
        return utils.import_object(import_path, config=self)

    def get_serializer(self, key):
        """Get serializer based on MCollective settings."""
        import_path = SerializerBase.plugins[self.config[key]]
        return utils.import_object(import_path)

    def get_host_and_ports(self):
        """Get all hosts and port pairs for the current configuration.

        The result must follow the :py:class:`stomp.Connection`
        ``host_and_ports`` parameter.

        Returns:
            ``host_and_ports``: Iterable of two-tuple where the first element
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

    @staticmethod
    def from_configfile(configfile):
        '''Reads configfile and returns a new :py:class:`Config` instance'''
        configstr = open(configfile, 'rt').read()
        return Config.from_configstr(configstr)

    @staticmethod
    def from_configstr(configstr, section='default'):
        '''Parses given string an returns a new :py:class:`Config` instance'''
        config = six.StringIO()
        config.write('[{0}]\n'.format(section))
        config.write(configstr)
        config.seek(0, os.SEEK_SET)
        parser = configparser.ConfigParser()
        parser.readfp(config)
        return Config(dict(parser.items(section)))
