from setuptools import setup, find_packages

setup(
    name='eems',
    version='0.1.0.0b1',
    description='eems - easy energy monitoring system',
    long_description='An easy application to establish an energy monitoring '
                     'system for raspberry pi and ds18b20 temperature sensors.',
    url='https://github.com/enricoba/eems',
    author='Henrik Baran, Aurofree Hoehn',
    author_email='henrik.baran@online.de, a.hoehn@mailbox.org',
    license='MIT',
    platforms='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Manufacturing',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='easy energy monitoring system',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_data={
        'eems': ['data/*.txt'],
    },
    entry_points={
        'console_scripts': ['eems = eems.scripts:main']
    }
)
