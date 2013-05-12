import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup

setup(name='mcollective',
      version='0.4',
      author='Aaron Brady',
      author_email='bradya@gmail.com',
      url='https://github.com/iwebhosting/mcollective-python',
      description="Python library for using Marionette Collective's RPC",
      #long_description=mcollective.__doc__,
      py_modules=['mcollective'],
      provides=['mcollective'],
      install_requires=['pyyaml', 'stompy'],
      extras_require={'SSL': ['M2Crypto']},
      keywords='mcollective',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
      ],
      test_suite='tests',
      test_requires=['mock', 'GitPython', 'CoilMQ'],
      )
