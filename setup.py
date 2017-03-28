#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pip.req import parse_requirements
from pip.download import PipSession
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()


def get_requirements(filepath):
    analysis = parse_requirements(filepath, session=PipSession())
    return [str(requirement.req) for requirement in analysis]


requirements = get_requirements('requirements.txt')
test_requirements = get_requirements('testing_requirements.txt')

setup(
    name='pyjkstra',
    version='0.1.0',
    description=("This is a Python implementation of Dijkstra's algorithm for "
                 "finding single-source shortest paths."),
    long_description=readme + '\n\n' + changelog,
    author="Robert Grant",
    author_email='rhgrant10@gmail.com',
    url='http://github.com/rhgrant10/pyjkstra',
    py_modules=['pyjkstra'],
    entry_points={
        'console_scripts': [
            'pyjkstra=pyjkstra:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords='pyjkstra',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
