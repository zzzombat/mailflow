# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
sys.path.insert(0, 'src')
import mailflow

requires = [
    'flask',
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
        ]
    },
)
