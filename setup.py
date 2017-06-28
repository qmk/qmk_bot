#!/usr/bin/env python
# Special thanks to Hynek Schlawack for providing excellent documentation:
#
# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
import os
from setuptools import setup, find_packages


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='qmk_bot',
    version='0.0.1',
    description='Github bot to manage the QMK project',
    long_description='\n\n'.join((read('README.rst'), read('AUTHORS.rst'))),
    url='http://qmk.fm/',
    license='MIT',
    author='Zach White',
    author_email='skullydazed@gmail.com',
    install_requires=['flask', 'flask-mysqldb', 'github-webhook'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: MIT',
        'Topic :: System :: Systems Administration',
    ],
)
