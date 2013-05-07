import os, sys, codecs

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = codecs.open(os.path.join(here, 'README.txt'), encoding='utf8').read()
CHANGES = codecs.open(os.path.join(here, 'CHANGES.txt'), encoding='utf8').read()

setup(name='pymeta',
      version='0.0.1',
      description='Prototype distribution metadata parser.',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        ],
      author='Daniel Holth',
      author_email='dholth@gmail.com',
      url='http://bitbucket.org/dholth/pymeta/',
      keywords='pymeta',
      license='MIT',
      py_modules = [ 'pymeta' ],
      include_package_data=True,
      zip_safe=False,
      test_suite = 'nose.collector',
      )

