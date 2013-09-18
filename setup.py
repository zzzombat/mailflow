# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
sys.path.insert(0, 'src')
import mailflow

requires = [
    'flask',
    'flask-security',
    'sqlalchemy>=0.8',
    'flask-sqlalchemy==0.16',
    'sqlalchemy-migrate',
    'flask-whooshalchemy==0.54a',
    'flask-wtf',
    'pytz==2013b',
    'flask-babel==0.8',
    'flup',
    'flask-admin',
    'psycopg2',
    'fs',
    'pyzmail',
    'kombu==2.5.14',
    'librabbitmq==1.0.1',
    'flask-restful',
    'blinker==1.2',
    'Flask-Cache',
    'python-memcached',
    'gevent',
    'psycogreen',
    'Flask-Script',
]

setup(
    name='mailflow',
    url='',
    license='GPLv3',
    version=mailflow.__version__,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'mailflow = mailflow.manage:manager.run',
        ]
    },
)
