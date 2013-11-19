'''python-mcollective exceptions'''


class PyMcoException(Exception):
    '''Base class for all python-mcollective exceptions'''


class ImproperlyConfigured(PyMcoException):
    '''Exception raised on configuration errors.'''


class ConfigLookupError(PyMcoException):
    '''Exception raised on configuration lookups errors.'''


class BadFilterFactOperator(PyMcoException):
    '''Exception raised when trying to add an unsopported fact operator to
    filters.'''
