from distutils.core import setup
import sys

setup(name='mcollective',
      version='0.3',
      author='Aaron Brady',
      author_email='bradya@gmail.com',
      url='https://github.com/iwebhosting/mcollective-python',
      description="Python library for using Marionette Collective's RPC",
      #long_description=mcollective.__doc__,
      py_modules=['mcollective',],
      provides=['mcollective',],
      install_requires=['M2Crypto','pyyaml', 'stompy'],
      keywords='mcollective',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                  ],
     )
