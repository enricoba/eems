from setuptools import setup

setup(
    name='eems',
    version='0.0.4.0a1',
    description='An easy application to establish an energy monitoring system.',
    long_description='test',
    url='https://github.com/enricoba/eems',
    author='Henrik Baran, Aurofree Hoehn',
    author_email='henrik.baran@online.de, a.hoehn@mailbox.org',
    license='MIT',
    platforms='',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Manufacturing',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='easy energy monitoring system',
    packages='eems',
    package_data={
        'eems': ['data/*.txt']
    },
    entry_points={
        'console_scripts': ['eems = eems.scripts:main']
    }
)
