metamagic.json
==============

An ultra-fast Python 3 implementation of a JSON encoder for Python objects designed
to be compatible with native JSON decoders in various web browsers.

Can either encode to a python string (see ``dumps``) or a sequence
of bytes (see ``dumpb``). The string returned by dumps() is guaranteed
to have only 7-bit ASCII characters [#f1]_ and ``dumps(obj).encode('ascii') = dumpb(obj)``.

Supports a special encoder class method `encode_hook(obj)` which, if present, is applied to
the input object and the rest of the processing is applied to the output of encode_hook().
Note: encode_hook() should always return an object; for objects which should not be
specially encoded encode_hook() should return the original object.

Supports custom encoders by using objects' ``__mm_json__()`` or ``__mm_serialize__()``
method, if available. It is guaranteed that for all non-native types ``__mm_json__`` and
then ``__mm_serialize__`` will be tried before any other attempt to encode the object [#f2]_.
The output of ``__mm_serialize__`` is in turn encoded as any other object (and may in turn have
an ``__mm_serialize__`` method or not be supported).

Natively supports strings, integers, floats, True, False, None, lists, tuples,
dicts, sets, frozensets, collections.OrderedDicts, colections.Set,
collections.Sequence [#f3]_, collections.Mapping, uuid.UUIDs [#f4]_, decimal.Decimals,
datetime.datetime and objects derived form all listed objects.

For all objects which could not be encoded in any other way an
attempt is made to convert an object to an encodeable one using ``Encoder.default(obj)``
method. If ``Encoder.default`` succeeds, the output is again encoded as any other object.

In case there is a need to custom-handle natively supported primitive types, an
``Encoder.encode_hook`` method exists.


Examples
--------

Encoding custom objects::

    >>> from metamagic.json import dumps, dumpb

    >>> class Foo:
    ...     def __mm_serialize__(self):
    ...         return "Im foo"
    ...

    >>> dumps(Foo())
    '"Im foo"'

    >>> dumps({Foo(): 123})
    '{"Im foo":123}'

Dumping straight to bytes::

    >>> dumpb(Foo())
    b'"Im foo"'

Bypassing serialization for JSON buffers::

    >>> class JSONData:
    ...     def __init__(self, data):
    ...         self.data = data
    ...
    ...     def __mm_json__(self):
    ...         return self.data

    >>> a = JSONData('["abc", "def"]')
    >>> dumps([1,2,3,a])
    '[1,2,3,["abc", "def"]]'


Exceptions raised
-----------------

* Both ``dumps()`` and ``dumpb()`` raise a TypeError for unsupported objects and
  for all dictionary keys which are not strings (or UUIDs [#f5]_) and
  which are not representable as strings (or UUIDs) by their ``__mm_serialize__`` method.

* ``default()`` raises a TypeError for all unsupported objects, and overwritten ``default()``
  is also expected to raise a TypeError for all objects it does not support.

* When encoding integers, ``dumps()`` and ``dumpb()`` raise a ValueError if integer
  value is greater than the maximum integer value supported by JavaScript
  (``9007199254740992``, see http://ecma262-5.com/ELS5_HTML.htm#Section_8.5).

* When encoding a nested object a ValueError is raised when going deeper than
  the allowed nesting level (100 by default, can be overwritten by passing the
  desired value as the second argument to ``dumps()`` and ``dumpb()`` methods)


Benchmarks
----------

::

    Array with 256 short ascii strings:
      std json:   2.6581 sec,      11286 req/sec
     mm c json:  0.90321 sec,      33214 req/sec  ( 2.9x )
     mm c 1ini:  0.85578 sec,      35055 req/sec  ( 3.1x )
    mm c dumpb:  0.84517 sec,      35495 req/sec  ( 3.1x )
       marshal:  1.77567 sec,      16895 req/sec

    Array with 2048 3-char ascii strings:
      std json:  0.47259 sec,       4231 req/sec
     mm c json:  0.12481 sec,      16024 req/sec  ( 3.8x )
     mm c 1ini:  0.12261 sec,      16311 req/sec  ( 3.9x )
    mm c dumpb:  0.11732 sec,      17047 req/sec  ( 4.0x )
       marshal:  0.41334 sec,       4838 req/sec

    Array with 256 long ascii strings:
      std json:  1.30821 sec,       3822 req/sec
     mm c json:  0.47144 sec,      10605 req/sec  ( 2.8x )
     mm c 1ini:  0.44159 sec,      11322 req/sec  ( 3.0x )
    mm c dumpb:   0.4346 sec,      11504 req/sec  ( 3.0x )
       marshal:  0.85593 sec,       5841 req/sec

    Array with 256 long utf-8 strings:
      std json:  1.52419 sec,       1312 req/sec
     mm c json:   1.4438 sec,       1385 req/sec  ( 1.1x )
     mm c 1ini:  1.43666 sec,       1392 req/sec  ( 1.1x )
    mm c dumpb:  1.40142 sec,       1427 req/sec  ( 1.1x )
       marshal:   1.3413 sec,       1491 req/sec

    Medium complex object:
      std json:   3.5078 sec,       2850 req/sec
     mm c json:  1.45764 sec,       6860 req/sec  ( 2.4x )
     mm c 1ini:  1.43357 sec,       6975 req/sec  ( 2.4x )
    mm c dumpb:  1.47626 sec,       6773 req/sec  ( 2.4x )
       marshal:  1.04175 sec,       9599 req/sec

    Array with 256 doubles:
      std json:  3.37919 sec,       2959 req/sec
     mm c json:  2.23615 sec,       4471 req/sec  ( 1.5x )
     mm c 1ini:  2.48201 sec,       4028 req/sec  ( 1.4x )
    mm c dumpb:  2.23184 sec,       4480 req/sec  ( 1.5x )
       marshal:  0.14098 sec,      70932 req/sec

    Array with 256 ints:
      std json:   1.0185 sec,      19636 req/sec
     mm c json:   0.2752 sec,      72674 req/sec  ( 3.7x )
     mm c 1ini:  0.25349 sec,      78898 req/sec  ( 4.0x )
    mm c dumpb:  0.28252 sec,      70791 req/sec  ( 3.6x )
       marshal:  0.15442 sec,     129516 req/sec

    Array with 256 small ints:
      std json:  1.04397 sec,     191576 req/sec
     mm c json:  0.28152 sec,     710429 req/sec  ( 3.7x )
     mm c 1ini:  0.09222 sec,    2168726 req/sec  ( 11.3x )
    mm c dumpb:  0.27627 sec,     723929 req/sec  ( 3.8x )
       marshal:  0.08306 sec,    2407897 req/sec

    Array with 256 Decimals:
      std json:     failed to serialize
     mm c json:  0.77161 sec,      10367 req/sec  ( 0.0x )
     mm c 1ini:  0.76022 sec,      10523 req/sec  ( 0.0x )
    mm c dumpb:  0.78671 sec,      10168 req/sec  ( 0.0x )
       marshal:     failed to serialize

    Array with 256 True values:
      std json:  2.08432 sec,      38381 req/sec
     mm c json:  0.47159 sec,     169638 req/sec  ( 4.4x )
     mm c 1ini:  0.39814 sec,     200934 req/sec  ( 5.2x )
    mm c dumpb:  0.45191 sec,     177026 req/sec  ( 4.6x )
       marshal:  0.24776 sec,     322893 req/sec

    Array with 256 False values:
      std json:   2.0099 sec,      39802 req/sec
     mm c json:  0.50992 sec,     156887 req/sec  ( 3.9x )
     mm c 1ini:  0.43001 sec,     186042 req/sec  ( 4.7x )
    mm c dumpb:  0.50839 sec,     157359 req/sec  ( 4.0x )
       marshal:  0.25551 sec,     313099 req/sec

    Array with 256 dict{string, int} pairs:
      std json:  1.96227 sec,       4076 req/sec
     mm c json:  0.36569 sec,      21876 req/sec  ( 5.4x )
     mm c 1ini:  0.34565 sec,      23144 req/sec  ( 5.7x )
    mm c dumpb:  0.36583 sec,      21868 req/sec  ( 5.4x )
       marshal:  0.51862 sec,      15425 req/sec

    Array with 256 dict-based{string, int} pairs:
      std json:  4.20194 sec,       1903 req/sec
     mm c json:  3.74071 sec,       2138 req/sec  ( 1.1x )
     mm c 1ini:  3.70554 sec,       2158 req/sec  ( 1.1x )
    mm c dumpb:  3.77039 sec,       2121 req/sec  ( 1.1x )
       marshal:     failed to serialize

    Array with 256 orderedDict{string, int} pairs:
      std json:  2.31765 sec,        431 req/sec
     mm c json:  0.70724 sec,       1413 req/sec  ( 3.3x )
     mm c 1ini:  0.69506 sec,       1438 req/sec  ( 3.3x )
    mm c dumpb:  0.70373 sec,       1420 req/sec  ( 3.3x )
       marshal:     failed to serialize

    Dict with 256 arrays with 256 dict{string, int} pairs:
      std json:  3.78828 sec,         13 req/sec
     mm c json:  0.69496 sec,         71 req/sec  ( 5.5x )
     mm c 1ini:  0.69522 sec,         71 req/sec  ( 5.4x )
    mm c dumpb:  0.68382 sec,         73 req/sec  ( 5.5x )
       marshal:  1.02776 sec,         48 req/sec


Tests
-----

``pytest`` is required to run tests.


.. [#f1] All characters required to be escaped by the JSON spec @ http://json.org are escaped
.. [#f2] If present, encode_hook() is applied before and independently of all other encoders
.. [#f3] To avoid errors in the metamagic framework ``bytes()``, ``bytearray()`` and derived
        classes are deliberately not encoded using the built-in sequence encoder;
        the only way to encode these objects is to either overwrite the encoders' default()
        method or to provide __mm_serialize__ method in the object being serialized.
.. [#f4] UUIDs and Decimals are encoded as strings.
.. [#f5] JSON specification only supports string dictionary keys; since UUIDs
        are also encoded to strings and are a common key in the metamagic framework,
        this encoder also supports UUIDs as dictionary keys.
