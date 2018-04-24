#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup,find_packages
def calculate_version():
    initpy = open('DHCdatacleaner/_version.py').read().split('\n')
    version = list(filter(lambda x: '__version__' in x, initpy))[0].split('\'')[1]
    return version

package_version = calculate_version()

setup(
    name='DHCdatacleaner',
    version=package_version,
    author='Eddie Huang',
    author_email='huangyi@dhcc.com.cn',
    packages=find_packages(),
    url='',
    license='',
    entry_points={'console_scripts': ['DHCdatacleaner=DHCdatacleaner:main', ]},
    description=('DHC Python tool that automatically cleans data sets and readies them for analysis.'),
    long_description='''
A Python tool that automatically cleans data sets and readies them for analysis.
''',
    zip_safe=True,
    install_requires=['pandas', 'scikit-learn', 'numpy'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ],
    keywords=['data cleaning', 'csv', 'machine learning', 'data analysis', 'data engineering'],
)
