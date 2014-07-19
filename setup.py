from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

setup(
    name='python-context-logger',
    version='0.1',
    url='http://github.com/navi7/python-context-logger',
    license='LGPL v3',
    author='Ivan Mesic',
    tests_require=['pytest'],
    install_requires=['nose==1.3.3',
                    'mock==1.0.1',
                    ],
    author_email='ivanmesic@gmail.com',
    description='Context logging for python',
    long_description=long_description,
    packages=['context_logging'],
    include_package_data=False,
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: LGPL v3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        ],
    extras_require={}
)