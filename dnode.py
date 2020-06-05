#coding=utf8

import json
import pprint
import copy
import six
import logging


VERSION = '0.2.5'


class CompatibleWithDict(object):
    """ 兼容 dict 方式处理数据
    """

    def clear(self, *args, **kwargs):
        """ D.clear() -> None.  Remove all items from D. """
        return self._data.clear(*args, **kwargs)

    def copy(self, *args, **kwargs):
        """ D.copy() -> a shallow copy of D """
        return self._data.copy(*args, **kwargs)

    @staticmethod # known case
    def fromkeys(*args, **kwargs): # real signature unknown
        """ Returns a new dict with keys from iterable and values equal to value. """
        return self._data.fromkeys(*args, **kwargs)

    def get(self, *args, **kwargs):
        """ D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None. """
        return self._data.get(*args, **kwargs)

    def items(self, *args, **kwargs):
        """ D.items() -> a set-like object providing a view on D's items """
        return self._data.items(*args, **kwargs)

    def keys(self, *args, **kwargs):
        """ D.keys() -> a set-like object providing a view on D's keys """
        return self._data.keys(*args, **kwargs)

    def pop(self, *args, **kwargs):
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        return self._data.pop(*args, **kwargs)

    def popitem(self, *args, **kwargs):
        """
        D.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if D is empty.
        """
        return self._data.popitem(*args, **kwargs)

    def setdefault(self, *args, **kwargs):
        """ D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D """
        return self._data.setdefault(*args, **kwargs)

    def update(self, *args, **kwargs):
        """
        D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
        In either case, this is followed by: for k in F:  D[k] = F[k]
        """
        return self._data.update(*args, **kwargs)

    def values(self, *args, **kwargs):
        """ D.values() -> an object providing a view on D's values """
        return self._data.values(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        """ True if D has a key k, else False. """
        return self._data.__contains__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        """ Delete self[key]. """
        return self._data.__delitem__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        """ Return self==value. """
        return self._data.__eq__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        """ x.__getitem__(y) <==> x[y] """
        return self._data.__getitem__(*args, **kwargs)

    def __ge__(self, *args, **kwargs):
        """ Return self>=value. """
        return self._data.__ge__(*args, **kwargs)

    def __gt__(self, *args, **kwargs):
        """ Return self>value. """
        return self._data.__gt__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return self._data.__iter__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self._data.__len__(*args, **kwargs)

    def __le__(self, *args, **kwargs):
        """ Return self<=value. """
        return self._data.__le__(*args, **kwargs)

    def __lt__(self, *args, **kwargs):
        """ Return self<value. """
        return self._data.__lt__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        """ Return self!=value. """
        return self._data.__ne__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        """ Set self[key] to value. """
        return self._data.__setitem__(*args, **kwargs)

    def __sizeof__(self, *args, **kwargs):
        """ D.__sizeof__() -> size of D in memory, in bytes """
        return self._data.__sizeof__(*args, **kwargs)

    __hash__ = None


class DNode(CompatibleWithDict):
    """ read and write json as a object
    """

    _data = {}

    def __new__(cls, data):
        data = cls._prepare_data(data)
        if isinstance(data, list):
            return [cls(item) for item in data]
        return object.__new__(cls)

    def __init__(self, data):
        data = self._prepare_data(data)
        assert isinstance(data, dict)
        self._data = data

    def __repr__(self):
        return '<DNode: %s>' % self.dumps()

    def __str__(self):
        return '<DNode: %s>' % self.dumps()

    def __eq__(self, other):
        if isinstance(other, DNode):
            return self._data == other._data
        if isinstance(other, dict):
            return self._data == other
        return False

    def __getattr__(self, item):

        assert item != '_data', 'DNode object must have `_data` property!'

        if item not in self.fields:
            # raise AttributeError('%s field not in DNode' % item)
            return None

        value = self._data[item]

        val = self._get_node_value(value)

        self._data[item] = val

        return val

    def __setattr__(self, key, value):

        if key == '_data' or key not in self.fields:
            return super(DNode, self).__setattr__(key, value)

        self._data[key] = value

    @staticmethod
    def _prepare_data(data):
        if isinstance(data, six.string_types):
            try:
                data = json.loads(data)
            except Exception as e:
                logging.error('Load data failed! %s' % data)
                raise e
        return data

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

    def _touch_all_fields(self):
        for field in self.fields:
            value = getattr(self, field)
            if isinstance(value, DNode):
                value._touch_all_fields()

    def dumps(self, *args, **kwargs):
        if 'default' in kwargs:
            logging.warning('The default param of dumps will be replaced!')
        kwargs['default'] = lambda obj: obj._data if hasattr(obj, '_data') else None
        return json.dumps(self, *args, **kwargs)

    def to_dict(self):
        return json.loads(self.json)

    def pprint(self):
        self._touch_all_fields()
        pprint.pprint(self._data)

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
    """ This class of node is designed for SM
    1. add `STRUCT_FIELDS` into class, only fields in STRUCT_FIELDS can be changed
    2. use deepcopy
    """

    STRUCT_FIELDS = set([])

    def __setattr__(self, key, value):

        if key in SMNode.STRUCT_FIELDS:
            self._data[key] = value
            return

        super(SMNode, self).__setattr__(key, value)

    def __copy__(self):
        return copy.deepcopy(self)


if __name__ == '__main__':

    # pip install dnode
    # from dnode import *

    print('==============================================================================')
    print('========================== DNode Run For Test ================================')
    print('==============================================================================')

    print('============== load data ===============')

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

    print(obj.to_dict())
    assert obj.to_dict() == data

    print('=========== print object ===============')

    print(obj)
    obj.pprint()

    print('============= print json ===============')

    print(obj.json)  
    # or print(obj.dumps(indent=4))

    print('=========== test getattr ===============')

    assert obj.a == 1
    assert obj.b.b1 == 3
    assert obj.c.c2 == {'c22': 22} == DNode({'c22': 22})
    assert obj.d[1] == 'd2'
    assert obj.e[1].ee == 2
    assert obj.f[0][0] == 'f11'
    assert obj.g[0][0].gg == 11
    assert obj.h == None

    print('=========== test setattr ===============')

    obj.a = 'change_a'
    obj.b.b1 = 'change_b'
    obj.c.c2.c22 = 'change_c'
    obj.d[1] = 'change_d'
    obj.e[1].ee = 'change_e'
    obj.f[0][0] = 'change_f'
    obj.g[0][0].gg = 'change_g'

    data = obj.to_dict()
    assert data['a'] == 'change_a'
    assert data['b']['b1'] == 'change_b'
    assert data['c']['c2']['c22'] == 'change_c'
    assert data['d'][1] == 'change_d'
    assert data['e'][1]['ee'] == 'change_e'
    assert data['f'][0][0] == 'change_f'
    assert data['g'][0][0]['gg'] == 'change_g'

    print('======== test set non-json type =========')

    obj.a = {1, 2, 3}
    data = obj.to_dict()
    assert data['a'] == None

    print('============== test clear ===============')

    obj.clear()
    obj.pprint()

    print('============== list init ================')

    data = '[ {"a": 1}, [{"b": 2}, {"c": 3}] ]'
    rs = DNode(data)
    print(rs)
    assert isinstance(rs, list)
    assert rs[0].a == 1
    assert rs[1][0].b == 2
    assert rs[1][1].c == 3

    print('=========================================')

    print('\n\n-------------- test SMNode ---------------')

    print('========= test STRUCT_FIELDS ============')

    obj = SMNode({})
    SMNode.STRUCT_FIELDS = set(['aaa', 'bbb'])
    obj.aaa = 123
    obj.ccc = 456
    print(obj.json)  
    print('`ccc` should not in the output')

    print('=========================================')


