# Copyright © 2020 HQS Quantum Simulations GmbH. All Rights Reserved.

from setuptools import setup
import os

path = os.path.dirname(os.path.abspath(__file__))

# Read version
__version__ = None
with open(os.path.join(path, 'qad_api/__version__.py')) as file:
    exec(file.read())

# Read readme
readme = None
with open(os.path.join(path, 'README.md')) as file:
    readme = file.read()

# Read license
license = None
with open(os.path.join(path, 'LICENSE')) as file:
    license = file.read()

# Read required packages
install_requires = []
with open(os.path.join(path, 'requirements.txt')) as file:
    install_requires = [r.strip() for r in file.readlines()]


setup(
    name='QAD API',
    version=__version__,
    packages=['qad_api'],
    license=license,
    long_description=readme,
    install_requires=install_requires
)
