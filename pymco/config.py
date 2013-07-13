'''python-mcollective configuration module'''
import collections
import functools
import os

import six
from six.moves import configparser

from . import exc

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

    @staticmethod
    def from_configfile(configfile):
        '''Reads configfile and returns a new :py:class:`Config` instance'''
        configstr = open(configfile, 'rt').read()
        return Config.from_configstr(configstr)

    @staticmethod
    def from_configstr(configstr, section='default'):
        '''Parses given string an returns a new :py:class:`Config` instance'''
        config = six.StringIO()
        config.write('[{0}]'.format(section))
        config.write(configstr)
        config.seek(0, os.SEEK_SET)
        parser = configparser.ConfigParser()
        parser.readfp(config)
        return Config(dict(parser.items(section)))
