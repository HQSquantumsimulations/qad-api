# Copyright 2020 HQS Quantum Simulations GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is the Python library for accessing the API of QAD Cloud by HQS Quantum Simulations GmbH.

The library is split into modules. In the **core** module, there is the
:class:`.QAD_API` class, which serves as the main entry point for all API
interactions.

The other modules are accessible as attributes of an instance of
:class:`.QAD_API` and contain corresponding sub-APIs.

Modules
=======

.. autosummary::
    :toctree: generated/

    qad_api.core
    qad_api.account
    qad_api.lattice
"""

from qad_api.core import *
from qad_api.account import *
from qad_api.lattice import *
