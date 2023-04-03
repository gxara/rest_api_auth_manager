# -*- coding: utf-8 -*-
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='rest_api_auth_manager',
    version='1.0.1',
    description='Biblioteca para autenticar e autorizar requisições',
    url='https://github.com/gxara/rest_api_auth_manager',
    author='gxara',
    author_email='gabrielxara@gmail.com',
    license='Private',
    package_dir={"": "src"},
    packages=['rest_api_auth_manager'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'redis'
    ],
)
