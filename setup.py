# -*- coding: utf-8 -*-
"""
Setup file for eems.
"""


from setuptools import setup, find_packages
from eems import __project__, __version__, __author__


# run setup
setup(
    name=__project__,
    version=__version__,
    description='eems - easy energy monitoring system',
    long_description='An easy application to establish an energy monitoring '
                     'system for raspberry pi and ds18b20 temperature sensors.',
    url='https://github.com/enricoba/eems',
    author=__author__,
    author_email='henrik.baran@online.de, a.hoehn@mailbox.org',
    license='MIT',
    install_requires=[
        'flask',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Manufacturing',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='easy energy monitoring system raspberrry pi',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': ['eems = eems.scripts.script:main']
    },
    include_package_data=True,
)
