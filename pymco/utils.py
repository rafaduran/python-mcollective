"""
:py:mod:`pymco.utils`
---------------------
python-mcollective utils.
"""


def import_class(import_path):
    """Import a class based on given dotted import path string.

    It just splits the import path in order to geth the module and class names,
    then it just calls to :py:func:`__import__` with the module name and
    :py:func:`getattr` with the module and the class name.

    Params:
        ``import_path``: A dotted import path string.
    Returns:
        ``class``: The class once imported.
    Raises:
        :py:exc:`ImportError`
    """
    parts = import_path.split('.')
    mod_str, klass_str = '.'.join(parts[:-1]), parts[-1]
    try:
        mod = __import__(mod_str)
        return getattr(mod, klass_str)
    except (AttributeError, ValueError):
        raise ImportError('Unable to import {klass} from module {mod}'.format(
            klass=klass_str,
            mod=mod_str,
        ))


def import_object(import_path, *args, **kwargs):
    """Import a class and instantiate it.

    Uses :py:func:`import_class` in order to import the given class by its
    import path and instantiate it using given positional and keyword
    arguments.

    Params:
        ``import_path``: Same argument as :py:func:`import_class`.

        ``args``: Positional arguments for object instantiation.

        ``kwargs``: Keyword arguments for object instantiation.
    """
    return import_class(import_path)(*args, **kwargs)
