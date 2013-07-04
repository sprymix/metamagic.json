##
# Copyright (c) 2012-2013 Sprymix Inc.
# All rights reserved.
#
# See LICENSE for details.
##


from collections import OrderedDict
from decimal import Decimal
from json import dumps as std_dumps
import random
import marshal

from metamagic.json._encoder import Encoder as CEncoder
from metamagic.json.encoder import Encoder as PyEncoder
from metamagic.test import benchmark, skip


class BaseBenchmarkJSONEncoder:
    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_short_ascii(self):
        arr = []
        for _ in range(256):
            arr.append("A pretty long string which is in a list")

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_2048_3_char_ascii(self):
        arr = []
        for _ in range(2048):
            arr.append("abc")

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_long_ascii(self):
        arr = []
        for _ in range(2048):
            arr.append("abcabc" + "z" * 150)

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_long_utf8(self):
        arr = []
        for _ in range(2048):
            arr.append("عالم " * 50)

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_medium_complex_object(self):
        user        = { "userId": 3381293, "age": 213, "username": "johndoe",
                        "fullname": "John Doe the Second", "isAuthorized": True,
                        "liked": 31231.31231202, "approval": 31.1471,
                        "jobs": [ 1, 2 ], "currJob": None }
        friends     = [ user, user, user, user, user, user, user, user ]
        testobj     = [ [user, friends],  [user, friends],  [user, friends],
                        [user, friends],  [user, friends],  [user, friends] ]

        return lambda: self.encode(testobj)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_doubles(self):
        arr = []
        for _ in range(256):
            arr.append(10000000 * random.random())

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_ints(self):
        arr = []
        for _ in range(256):
            arr.append(int(10000000 * random.random()))

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_small_ints(self):
        arr = []
        for _ in range(256):
            arr.append(int(10000 * random.random()))

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_decimals(self):
        arr = []
        for _ in range(256):
            arr.append(Decimal(str(random.random()*100000)))

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_true_false_values(self):
        arr = []
        for _ in range(128):
            arr.extend((True, False))

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_dict_string_int(self):
        arr = []
        for _ in range(128):
            arr.append({str(random.random()*20): int(random.random()*1000000)})

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_deriveddict_string_int(self):
        class DerivedDict(dict):
            pass
        arr = []
        for _ in range(128):
            arr.append(DerivedDict({str(random.random()*20): int(random.random()*1000000)}))

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_ordereddict_string_int(self):
        arr = []
        for _ in range(128):
            d = {
                str(random.random()*20): int(random.random()*1000000),
                str(random.random()*20): int(random.random()*1000000),
                str(random.random()*20): int(random.random()*1000000),
                str(random.random()*20): int(random.random()*1000000)
            }
            ordered_d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
            arr.append(ordered_d)

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=6.0)
    def benchmark_dict_256_arrays_256_string_int_pairs(self):
        dct = {}
        for _ in range(128):
            arrays = []
            for _ in range(256):
                arrays.append({str(random.random()*20): int(random.random()*1000000)})
            dct[str(random.random()*20)] = arrays

        return lambda: self.encode(dct)


class BaseBenchmarkJSONEncoderCustom:
    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_objs_with_mm_serialize(self):
        class CustomObject:
            def __init__(self, a, b):
                self.a = a
                self.b = b

            def __mm_serialize__(self):
                return {"a": self.a, "b": self.b}

        arr = []
        for _ in range(256):
            arr.append(CustomObject(a = str(random.random()*20), b = int(random.random()*20)))

        return lambda: self.encode(arr)

    @benchmark.throughput(seconds=3.0)
    def benchmark_array_256_objs_with_mm_json(self):
        class CustomObject:
            def __mm_json__(self):
                return b'{"a": "spamspamspam!", "b": 42424242}'

        arr = []
        for _ in range(256):
            arr.append(CustomObject())

        return lambda: self.encode(arr)


class BenchmarkJSONEncoder_Std(BaseBenchmarkJSONEncoder):
    def encode(self, obj):
        return std_dumps(obj)

    def benchmark_array_256_decimals(self):
        skip()


class BenchmarkJSONEncoder_C(BaseBenchmarkJSONEncoder, BaseBenchmarkJSONEncoderCustom):
    def encode(self, obj):
        return CEncoder().dumpb(obj)


class BenchmarkJSONEncoder_Python(BaseBenchmarkJSONEncoder, BaseBenchmarkJSONEncoderCustom):
    def encode(self, obj):
        return PyEncoder().dumpb(obj)


class BenchmarkJSONEncoder_Marshal(BaseBenchmarkJSONEncoder):
    def benchmark_array_256_decimals(self):
        skip()

    def benchmark_array_256_deriveddict_string_int(self):
        skip()

    def benchmark_array_256_ordereddict_string_int(self):
        skip()

    def encode(self, obj):
        return marshal.dumps(obj)
