#!/usr/bin/env python3.4
# coding=utf-8

from setuptools import setup, find_packages


setup(
    name='catcher',
    version='0.0.1',
    description='RESTful app for ultimate frisbee tournament management',
    author='Marek Dostál',
    keywords='ultimate,frisbee,rest,api',
    packages=find_packages(),
    license='Other/Proprietary License',
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'License :: Other/Proprietary License'
    ],
    install_requires=[
        'colorlog',
        'sqlalchemy',
        'falcon',
        'iso3166',
        'ujson',
        'click',
        'uwsgi',
        'py'
    ],
    entry_points={
        'console_scripts': [
            'catcher = catcher.__main__:main',
        ],
    },
    package_data={
        'catcher': [
            '../conf/catcher.test.cfg'
        ]
    },
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'flexmock',
        'pymysql'
    ],
    zip_safe=False,
)
