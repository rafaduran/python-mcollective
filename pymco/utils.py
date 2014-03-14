"""
:py:mod:`pymco.utils`
---------------------
python-mcollective utils that don't fit elsewhere.
"""
import importlib


def import_class(import_path):
    """Import a class based on given dotted import path string.

    It just splits the import path in order to geth the module and class names,
    then it just calls to :py:func:`__import__` with the module name and
    :py:func:`getattr` with the module and the class name.

    :arg import_path: dotted import path string.
    :return: the class once imported.
    :raise: :py:exc:`ImportError` if the class can't be imported.
    """
    parts = import_path.split('.')
    mod_str, klass_str = '.'.join(parts[:-1]), parts[-1]
    try:
        mod = importlib.import_module(mod_str)
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

    :arg import_path: Same argument as :py:func:`import_class`.
    :arg \*args: extra pPositional arguments for object instantiation.
    :arg \*\*kwargs: extra Keyword arguments for object instantiation.
    :returns: an object the imported class initialized with given arguments.
    """
    return import_class(import_path)(*args, **kwargs)


def load_rsa_key(filename):
    """Read filename and try to load its contents as an RSA key.

    Wrapper over :py:meth:`Crypto.PublicKey.RSA.importKey`, just getting the
    file content first and then just loading the key from it.

    :param filename: RSA key file name.
    :returns: loaded RSA key.
    """
    # Importing here since Crypto module is only require for the SSL security
    # provider plugin.
    from Crypto.PublicKey import RSA
    with open(filename, 'rt') as key:
        content = key.read()

    return RSA.importKey(content)
