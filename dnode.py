# dnode v0.11

import json
import pprint


class DNode(object):
    data = {}

    def __init__(self, data):
        self.load_data(data)

    def __repr__(self):
        return '<DNode: %s>' % self.json

    def __str__(self):
        return '<DNode: %s>' % self.json

    def __getattr__(self, item):
        if item == 'data':
            raise AttributeError

        if item not in self.fields:
            raise AttributeError

        value = self.data[item]

        val = self._get_node_value(value)

        self.data[item] = val

        return val

    def __setattr__(self, key, value):

        if key == 'data' or key not in self.fields:
            return super(DNode, self).__setattr__(key, value)

        self.data[key] = value

    @property
    def fields(self):
        return self.data.keys()

    @property
    def json(self):
        return self._dumps()

    def _get_node_value(self, value):

        if isinstance(value, dict):
            return DNode(value)
        elif isinstance(value, list):
            rs = []
            for v in value:
                rs.append(self._get_node_value(v))
            return rs
        else:
            return value

    def _dumps(self, indent=None):
        return json.dumps(self, indent=indent, default=lambda obj: obj.data)

    def _touch_all_fields(self):
        for field in self.fields:
            value = getattr(self, field)
            if isinstance(value, DNode):
                value._touch_all_fields()

    def pprint(self):
        self._touch_all_fields()
        pprint.pprint(self.data)

    def load_data(self, data):
        if not isinstance(data, dict):
            data = json.loads(data)
        self.data = data

    def clear(self):
        for key, value in self.data.iteritems():
            if isinstance(value, DNode):
                value.clear()
                continue

            if isinstance(value, str):
                null_value = ''
            elif isinstance(value, int):
                null_value = 0
            elif isinstance(value, list):
                null_value = []
            elif isinstance(value, dict):
                null_value = {}
            else:
                null_value = None

            self.data[key] = null_value


if __name__ == '__main__':

    data = {
        'a': 1,
        'b': {'b1': 3},
        'c': {'c1': 1, 'c2': {'c22': 22}},
        'd': ['d1', 'd2', 'd3'],
        'e': [{'ee': 1}, {'ee': 2}, {'ee': 3}],
        'f': [['f11', 'f12'], ['f21', 'f22']],
        'g': [[{'gg': 11}, {'gg': 12}], [{'gg': 21}, {'gg': 22}]],
    }

    obj = DNode(data)

    print '=========== print object ==============='

    obj.pprint()

    print '============= print json ==============='

    print obj._dumps(4)

    print '=========== test getattr ==============='

    print obj.a
    print obj.b.b1
    print obj.c.c2
    print obj.d[1]
    print obj.e[1].ee
    print obj.f[0][0]
    print obj.g[0][0].gg

    print '=========== test setattr ==============='

    obj.a = 'change_a'
    print obj.a

    obj.b.b1 = 'change_b'
    print obj.b.b1

    obj.c.c2.c22 = 'change_c'
    print obj.c.c2.c22

    obj.d[1] = 'change_d'
    print obj.d[1]

    obj.e[1].ee = 'change_e'
    print obj.e[1].ee

    obj.f[0][0] = 'change_f'
    print obj.f[0][0]

    obj.g[0][0].gg = 'change_g'
    print obj.g[0][0].gg

    print '============== test clear ==============='

    obj.clear()

    obj.pprint()

    print '========================================='

