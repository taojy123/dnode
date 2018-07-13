#coding=utf8

from setuptools import setup
import dnode


long_description = """
$ pip install dnode

from dnode import DNode
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

assert obj.a == 1
assert obj.d[1] == 'd2'

obj.b.b1 = 'change_b'
data = obj.serialize()
assert data['b']['b1'] == 'change_b'

"""

setup(
    name='dnode',
    version=dnode.VERSION,
    description='read/write json as a object | 像读写对象属性一样读写 json',
    long_description=long_description,
    author='tao.py',
    author_email='taojy123@163.com',
    maintainer='tao.py',
    maintainer_email='taojy123@163.com',
    license='MIT License',
    py_modules=['dnode'],
    platforms=["all"],
    url='https://github.com/taojy123/dnode',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
