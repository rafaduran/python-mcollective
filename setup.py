from distutils.core import setup
import sys
import mcollective


setup(name='mcollective',
      version=mcollective.__version__,
      author='Aaron Brady',
      author_email='bradya@gmail.com',
      url='https://github.com/insom/mcollective-python',
      description="Python library for using Marionette Collective's RPC",
      #long_description=mcollective.__doc__,
      py_modules=['mcollective',],
      provides=['mcollective',],
      keywords='mcollective',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                  ],
     )
