"""
:py:mod:`pymco.test.utils`
--------------------------
Utils for testing purposes.
"""
try:
    from unittest import mock
except ImportError:
    import mock  # noqa

import jinja2

from . import ctxt as _ctxt


def get_template(name, package=__package__):
    """Load Jinja 2 template from given package.

    :arg name: template name.
    :arg package: package to be used for loading the template, default is
        current package.
    :return: :py:class:`jinja2.environment.Template` object.
    """
    env = jinja2.Environment(loader=jinja2.PackageLoader(package, 'templates'))
    return env.get_template(name)


def configfile(ctxt=None):
    """Create a MCollective configuration file.

    :arg dict ctxt: the ctxt to be used for rendering MCollective configuration
        template.
    :return: The path where the configuration file has been placed
        (:py:data:`pymco.test.ctxt.TEST_CFG`).
    """
    if not ctxt:
        ctxt = _ctxt.DEFAULT_CTXT
    with open(_ctxt.TEST_CFG, 'wt') as cfg:
        cfg.write(get_template('server.cfg.jinja').render({'config': ctxt}))
    return _ctxt.TEST_CFG
