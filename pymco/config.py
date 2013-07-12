'''python-mcollective configuration module'''
import functools
import os

import six
from six.moves import configparser

from . import exc

def lookup_with_default(fnc):
    @functools.wraps(fnc)
    def decorator(self, name, *args, **kwargs):
        try:
            return fnc(self, name)
        except configparser.Error as exc:
            if 'default' in kwargs:
                return kwargs['default']
            raise exc
    return decorator


class Config(object):
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

    @lookup_with_default
    def get(self, name):
        '''Get string option by name'''
        return self.parser.get(self.section, name)

    @lookup_with_default
    def getint(self, name):
        '''Get int option by name.'''
        return self.parser.getint(self.section, name)

    @lookup_with_default
    def getboolean(self, name):
        return self.parser.getboolean(self.section, name)
