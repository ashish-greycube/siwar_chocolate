# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in siwar_chocolate/__init__.py
from siwar_chocolate import __version__ as version

setup(
	name='siwar_chocolate',
	version=version,
	description='Customization for Siwar Chocolate',
	author='GreyCube Technologies',
	author_email='admin@greycube.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
