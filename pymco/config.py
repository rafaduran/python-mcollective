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
    def __init__(self, configfile=None, configstr=None, section='default'):
        config = six.StringIO()
        config.write('[{0}]'.format(section))

        if not configstr:
            if not configfile:
                raise exc.ImproperlyConfigured
            else:
                config.write(open(configfile, 'r').read())
        else:
            config.write(configstr)

        config.seek(0, os.SEEK_SET)

        self.parser = configparser.ConfigParser()
        self.parser.readfp(config)

        self.section = section
        self.config = dict(self.parser.items(section))

    def __len__(self):
        return len(self.config)

    def __iter__(self):
        return six.iterkeys(self.config)

    def __getitem__(self, key):
        return self.config[key]

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
