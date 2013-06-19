import sys
try:
    import distribute_setup
    distribute_setup.use_setuptools()
except ImportError:
    pass

from pip import req
from setuptools import setup
from setuptools.command.test import test as TestCommand

REQ = [dep.name
       for dep in req.parse_requirements('requirements/base.txt')]
TREQ = (set([dep.name or dep.url
            for dep in req.parse_requirements('requirements/tests.txt')]) -
        set(REQ))


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name='mcollective',
      version='0.4',
      author='Aaron Brady',
      author_email='bradya@gmail.com',
      url='https://github.com/iwebhosting/mcollective-python',
      description="Python library for using Marionette Collective's RPC",
      #long_description=mcollective.__doc__,
      py_modules=['mcollective'],
      provides=['mcollective'],
      #install_requires=['pyyaml', 'stompy'],
      install_requires=REQ,
      extras_require={'SSL': ['M2Crypto']},
      keywords='mcollective',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
      ],
      cmdclass={'test': PyTest},
      tests_require=TREQ,
      )
