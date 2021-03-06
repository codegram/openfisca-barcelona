#! /usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name='OpenFisca-Barcelona',
    version='1.0.0',
    author='OpenFisca Team',
    author_email='contact@openfisca.fr',
    description=u'OpenFisca tax and benefit system for Barcelona',
    keywords='benefit microsimulation social tax',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://github.com/openfisca/openfisca-barcelona',
    include_package_data=True,  # Will read MANIFEST.in
    install_requires=[
        'OpenFisca-Core == 19.0.0',
        'PyYAML >= 3.10',
        'numpy >= 1.11, < 1.13',
        'requests >= 2.8',
        ],
    extras_require={
        'api': [
            'OpenFisca-Web-API == 7.1.0',
            ],
        'test': [
            'flake8',
            'flake8-print',
            'nose',
            ]
        },
    packages=find_packages(),
    test_suite='nose.collector',
    )
