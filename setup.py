##
# Copyright (c) 2012 Sprymix Inc.
# All rights reserved.
#
# See LICENSE for details.
##


import sys
from distutils.core import setup, Extension


if sys.version_info < (3, 0):
    raise RuntimeError('metamagic.json requires python 3')


readme = open('README.rst').read()


setup(
    name='metamagic.json',
    version='0.9.0',
    description='Fast JSON encoder',
    long_description=readme,
    maintainer='Sprymix Inc.',
    maintainer_email='info@sprymix.com',
    url='http://github.com/sprymix/metamagic.json',
    platforms=['any'],
    ext_modules=[
        Extension('metamagic.json._encoder',
                  sources=['metamagic/json/_encoder/_encoder.c'],
                  extra_compile_args=['-O3'])
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python :: 3'
    ],
    packages=[
        'metamagic.json',
        'metamagic.json._encoder',
        'metamagic.json.tests'
    ],
    package_data = {
        'metamagic.json._encoder': ['*.c', '*.h']
    }
)
