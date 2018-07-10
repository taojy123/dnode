from setuptools import setup
import dnode


setup(
    name='dnode',
    version=dnode.VERSION,
    description='read/write json as a object',
    long_description=open('README.md').read(),
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
