from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='easy_ems',
    version='0.0.0.dev1',
    description='An easy application to establish an energy monitoring system.',
    long_description=long_description,
    url='https://github.com/enricoba/easy-ems',
    author='Henrik Baran, Aurofree Hoehn',
    author_email='henrik.baran@online.de, a.hoehn@mailbox.org',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Manufacturing',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='easy energy monitoring system',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['']
)
