# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in structure/__init__.py
from structure import __version__ as version

setup(
	name='structure',
	version=version,
	description='AFS',
	author='AFS',
	author_email='afsbo@afs.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
