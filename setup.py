from setuptools import setup, find_packages

setup(
    name='eems',
    version='0.0.0.dev1',
    description='An easy application to establish an energy monitoring system.',
    long_description='test',
    url='https://github.com/enricoba/eems',
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
        'Programming Language :: Python :: 2.7'
    ],
    keywords='easy energy monitoring system',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['']
)
