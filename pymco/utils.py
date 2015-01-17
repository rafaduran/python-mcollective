"""
:py:mod:`pymco.utils`
---------------------
python-mcollective utils that don't fit elsewhere.
"""
import binascii
import importlib
import logging


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


def pem_to_der(pem):
    """Convert an ascii-armored PEM certificate to a DER encoded certificate

    See http://stackoverflow.com/a/12921889 for details. Python ``ssl`` module
    has it own method for this, but it shouldn't work properly and this method
    is required.

    :arg str pem: The PEM certificate as string.
    """
    # TODO(rafaduran): report and/or fix Python ssl method.

    # Importing here since Crypto module is only require for the SSL security
    # provider plugin.
    from Crypto.Util.asn1 import DerSequence
    lines = pem.replace(" ", '').split()
    der = binascii.a2b_base64(''.join(lines[1:-1]))

    # Extract subject_public_key_info field from X.509 certificate (see RFC3280)
    cert = DerSequence()
    cert.decode(der)
    tbs_certificate = DerSequence()
    tbs_certificate.decode(cert[0])
    subject_public_key_info = tbs_certificate[6]
    # this can be passed to RSA.importKey()
    return subject_public_key_info


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
    logger = logging.getLogger(__name__)
    logger.debug("reading RSA key from {f}".format(f=filename))
    with open(filename, 'rt') as key:
        content = key.read()

    if content.startswith('-----BEGIN CERTIFICATE-----'):
        # TODO(rafadruan): this lacks testing.
        logger.debug("found ASCII-armored PEM certificate; converting to DER")
        content = pem_to_der(content)
    logger.debug("Importing RSA key")
    k = RSA.importKey(content)
    logger.debug("returning key")
    return k
