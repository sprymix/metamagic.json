##
# Copyright (c) 2014 Sprymix Inc.
# All rights reserved.
#
# See LICENSE for details.
##


from metamagic.json import loads, loadb


class TestJsonDecode:
    def test_json_loads(self):
        assert loads('{"a":"b"}') == {'a': 'b'}

    def test_json_loadb(self):
        assert loadb(b'{"a":"b"}') == {'a': 'b'}
