'''python-mcollective configuration module'''
import os

import six
from six.moves import configparser

from . import exc


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

    def get(self, name):
        '''Get string option by name'''
        return self.parser.get(self.section, name)

    def getint(self, name):
        pass

    def getfloat(self, name):
        pass

    def getboolean(self, name):
        pass
