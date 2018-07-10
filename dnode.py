# dnode

import json
import pprint
import copy


VERSION = '0.15'


class DNode(object):
    _data = {}

    def __init__(self, data):
        self.load_data(data)

    def __repr__(self):
        return '<DNode: %s>' % self.json

    def __str__(self):
        return '<DNode: %s>' % self.json

    def __getattr__(self, item):
        if item == '_data':
            raise AttributeError

        if item not in self.fields:
            raise AttributeError

        value = self._data[item]

        val = self._get_node_value(value)

        self._data[item] = val

        return val

    def __setattr__(self, key, value):

        if key == '_data' or key not in self.fields:
            return super(DNode, self).__setattr__(key, value)

        self._data[key] = value

    @property
    def fields(self):
        return self._data.keys()

    @property
    def json(self):
        return self.dumps(indent=4)

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

    def dumps(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = lambda obj: obj._data if hasattr(obj, '_data') else None
        return json.dumps(self, *args, **kwargs)

    def _touch_all_fields(self):
        for field in self.fields:
            value = getattr(self, field)
            if isinstance(value, DNode):
                value._touch_all_fields()

    def pprint(self):
        self._touch_all_fields()
        pprint.pprint(self._data)

    def load_data(self, data):
        if not isinstance(data, dict):
            data = json.loads(data)
        self._data = data

    def clear(self):
        for key, value in self._data.items():
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

            self._data[key] = null_value


class SMNode(DNode):

    STRUCT_FIELDS = set([])

    def __setattr__(self, key, value):

        if key in SMNode.STRUCT_FIELDS:
            self._data[key] = value
            return

        super(SMNode, self).__setattr__(key, value)

    def __copy__(self):
        return copy.deepcopy(self)


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

    print('=========== print object ===============')

    obj.pprint()

    print('============= print json ===============')

    print(obj.dumps(indent=4))

    print('=========== test getattr ===============')

    print(obj.a)
    print(obj.b.b1)
    print(obj.c.c2)
    print(obj.d[1])
    print(obj.e[1].ee)
    print(obj.f[0][0])
    print(obj.g[0][0].gg)

    print('=========== test setattr ===============')

    obj.a = 'change_a'
    print(obj.a)

    obj.b.b1 = 'change_b'
    print(obj.b.b1)

    obj.c.c2.c22 = 'change_c'
    print(obj.c.c2.c22)

    obj.d[1] = 'change_d'
    print(obj.d[1])

    obj.e[1].ee = 'change_e'
    print(obj.e[1].ee)

    obj.f[0][0] = 'change_f'
    print(obj.f[0][0])

    obj.g[0][0].gg = 'change_g'
    print(obj.g[0][0].gg)

    print('======== test set non-json type =========')

    obj.a = {1, 2, 3}
    print(obj.json)

    print('============== test clear ===============')

    obj.clear()
    obj.pprint()

    print('--------------- test SM -----------------')

    print('========= test STRUCT_FIELDS ============')

    obj = SMNode({})
    SMNode.STRUCT_FIELDS = set(['aaa', 'bbb'])
    obj.aaa = 123
    print(obj.json)

    print('=========================================')


