# dnode

[![PyPI Downloads](https://pypistats.com/badge/dnode.png)](https://pypistats.com/package/dnode)


`$ pip install dnode`

```python

from dnode import *


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

print(obj.serialize())
assert obj.serialize() == data

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

print('=========== test setattr ===============')

obj.a = 'change_a'
obj.b.b1 = 'change_b'
obj.c.c2.c22 = 'change_c'
obj.d[1] = 'change_d'
obj.e[1].ee = 'change_e'
obj.f[0][0] = 'change_f'
obj.g[0][0].gg = 'change_g'

data = obj.serialize()
assert data['a'] == 'change_a'
assert data['b']['b1'] == 'change_b'
assert data['c']['c2']['c22'] == 'change_c'
assert data['d'][1] == 'change_d'
assert data['e'][1]['ee'] == 'change_e'
assert data['f'][0][0] == 'change_f'
assert data['g'][0][0]['gg'] == 'change_g'

print('======== test set non-json type =========')

obj.a = {1, 2, 3}
data = obj.serialize()
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


```
