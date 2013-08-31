# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
sys.path.insert(0, 'src')
import mailflow

requires = [
    'flask==0.9',
    'flask-security',
    'sqlalchemy==0.7.9',
    'flask-sqlalchemy==0.16',
    'sqlalchemy-migrate',
    'flask-whooshalchemy==0.54a',
    'flask-wtf',
    'pytz==2013b',
    'flask-babel==0.8',
    'flup',
    'flask-admin',
    'psycopg2',
]

setup(
    name='mailflow',
    author_email='kubus@openpz.org',
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
            'mailflow-front = mailflow.front:main',
            'mailflow-deliver = mailflow.deliver:main',
        ]
    },
)
