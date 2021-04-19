# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in iac_activity_logger/__init__.py
from iac_activity_logger import __version__ as version

setup(
	name='iac_activity_logger',
	version=version,
	description='Farm Operations Management app for IAC',
	author='Eco Data & IAC',
	author_email='rk@whitehatglobal.org',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
