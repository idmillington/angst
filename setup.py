# -*- coding: utf-8 -*-
"""Installs this package."""

from setuptools import setup, find_packages

setup(
    name='angst',
    version='0.5.0',

    description='Adds secret messages to source code.',
    long_description='',
    keywords='source-code augmentation',

    url='https://github.com/idmillington/angst',
    author='Ian Millington',
    author_email='idmillington@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    entry_points={
        'console_scripts': [
            'angst=angst:main'
        ],
    },
)