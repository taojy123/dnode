#coding=utf8

from setuptools import setup
import dnode


try:
    long_description = open('README.md').read()
except Exception as e:
    long_description = ''


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
