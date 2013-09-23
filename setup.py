# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
sys.path.insert(0, 'src')
import mailflow

requires = [
    'pytz==2013b',
    'flask-babel==0.8',
    'flup',
    'fs',
    'dexml',
    'pyzmail',
    'blinker==1.2',
    'python-memcached',
    'gevent',
    'psycopg2',
    'psycogreen',
    'flask',
    'flask-login',
    'flask-sqlalchemy',
    'flask-admin',
    'flask-whooshalchemy==0.54a',
    'flask-wtf',
    'flask-restful',
    'Flask-Cache',
    'Flask-Script',
    'celery'
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
