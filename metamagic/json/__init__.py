##
# Copyright (c) 2012 Sprymix Inc.
# All rights reserved.
#
# See LICENSE for details.
##


__all__ = ('dumps', 'dumpb', 'loads', 'loadb')


try:
    from ._encoder import Encoder
except ImportError:
    from .encoder import Encoder


import json as std_json


def dumps(obj, encoder=Encoder):
    """Return a JSON representation of ``obj`` in a Python string.

       Uses the given Encoder class which is supposed to have a ``dumps``
       method.

       By default tries to use the C version of the Encoder class from the
       ``_encoder`` module. If there is no C version uses the Python version
       from the ``encoder`` module.

       See documentation for the given Encoder class for details.

       **Examples**:

       .. code-block:: pycon

           >>> dumps(True)
           'true'

           >>> dumps('foo')
           '"foo"'

       Using custom ``__mm_serialize__`` (see the Encoder class docs for more
       info):

       .. code-block:: pycon

           >>> class Foo:
           ...     def __mm_serialize__(self):
           ...         return 'foo/bar'

           >>> dumps(Foo())
           '"foo\/bar"'

       Using ``encode_hook()`` (see the Encoder class docs for more info):

       .. code-block:: pycon

           >>> class MyEncoder(Encoder):
           ...     def encode_hook(self, obj):
           ...         if isinstance(obj, int):
           ...             return '*' + str(obj)
           ...         return obj

           >>> MyEncoder().dumps([1])
           '["*1"]'
    """
    return Encoder().dumps(obj)


def dumpb(obj, encoder=Encoder):
    """Return a JSON representation of ``obj`` in a bytes() array.

       Uses the given Encoder class which is supposed to have a ``dumpb``
       method.

       By default tries to use the C version of the Encoder class from the
       ``_encoder`` module. If there is no C version uses the Python version
       from the ``encoder`` module.

       See documentation for the given Encoder class for details.

       **Examples**:

       .. code-block:: pycon

           >>> dumpb(True)
           b'true'
    """
    return Encoder().dumpb(obj)


def loads(s):
    """Deserialize ``s`` (instance of ``str``) to a Python object."""
    return std_json.loads(s)


def loadb(b):
    """Deserialize ``b`` (instance of ``bytes``) to a Python object."""
    assert isinstance(b, (bytes, bytearray))
    return std_json.loads(b.decode('utf-8'))
