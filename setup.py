import sys
try:
    import setuptools
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    import setuptools

from pip import download, req
from setuptools.command import test

pipsess = download.PipSession()

REQ = set(
    [dep.name for dep in
     req.parse_requirements('requirements/base.txt', session=pipsess)])
TREQ = set(
    [dep.name or dep.url for dep in
     req.parse_requirements('requirements/tests.txt', session=pipsess)]) - REQ

try:
    import importlib  # noqa
except ImportError:
    REQ.add('importlib')


class PyTest(test.test):
    def finalize_options(self):
        test.test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setuptools.setup(setup_requires=('d2to1',),
                 install_requires=REQ,
                 tests_require=TREQ,
                 extras_require={'ssl': ('pycrypto', 'PyYAML')},
                 cmdclass={'test': PyTest},
                 d2to1=True)
