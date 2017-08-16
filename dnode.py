
import json


class DNode(object):
    data = {}
    parent = None
    name = None
    position = None

    def __init__(self, data, parent=None, name=None, position=None):

        self.data = data
        self.parent = parent
        self.name = name
        self.position = position

    def __repr__(self):
        return '<DNode: %s>' % self.dumps()

    def __str__(self):
        return '<DNode: %s>' % self.dumps()

    def __getattr__(self, item):
        data = self.data.get(item)

        val = self._get_node_value(data, item)

        return val

    def __setattr__(self, key, value):

        if key not in self.data:
            return super(DNode, self).__setattr__(key, value)

        if isinstance(value, DNode):
            value = value.data
        self.data[key] = value

        if not self.parent:
            return

        if self.position is None:
            self.parent.data[self.name] = self.data
        else:
            self.parent.data[self.name][self.position] = self.data

    def _get_node_value(self, data, name, position=None):

        if isinstance(data, dict):
            return DNode(data, self, name, position)
        elif isinstance(data, list):
            dl = DNodeList()
            dl.parent = self
            dl.name = name
            position = 0
            for d in data:
                dl.append(self._get_node_value(d, name, position))
                position += 1
            return dl
        else:
            return data

    def dumps(self):
        return json.dumps(self.data, default=lambda obj: obj.data)

    @property
    def fields(self):
        return self.data.keys()


class DNodeList(list):

    parent = None
    name = None
    position = None

    def __init__(self, value=None):
        value = value or []
        super(DNodeList, self).__init__(value)

    def __repr__(self):
        return '<DNodeList: %s>' % self.dumps()

    def __str__(self):
        return '<DNodeList: %s>' % self.dumps()

    def __setitem__(self, key, value):
        assert isinstance(key, int)
        super(DNodeList, self).__setitem__(key, value)
        if isinstance(value, DNode):
            value = value.data
        self.parent.data[self.name][key] = value

    def dumps(self):
        return json.dumps(self.data, default=lambda obj: obj.data)

    @property
    def items(self):
        return list(self)

    @property
    def data(self):
        return self



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

    obj = DNode(data, None)

    import pprint
    pprint.pprint(obj.data)

    print '=========== test getattr ==============='

    print obj.a
    print obj.b.b1
    print obj.c.c2.c22
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
    print obj.d[1]              # failed!

    obj.e[1].ee = 'change_e'
    print obj.e[1].ee

    obj.f[0][0] = 'change_f'
    print obj.f                 # failed!

    obj.g[0][0].gg = 'change_g'
    print obj.g                 # failed!

    print '========================================'

    # todo: solution make a DNodeList class


    e0 = obj.e[0]
    print e0
    print e0.dumps()

    a = DNodeList([2, 3, 4])
    json.dumps(a)


