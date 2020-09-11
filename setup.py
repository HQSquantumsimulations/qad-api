# Copyright © 2020 HQS Quantum Simulations GmbH. All Rights Reserved.

from setuptools import setup
from qad_api.__version__ import __version__

setup(
    name='QAD API',
    version=__version__,
    packages=['qad_api'],
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
    install_requires=[r.strip() for r in open('requirements.txt').readlines()]
)
