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

"""Module for solving lattice problems.

The API of this module is divided into a main class (:class:`Lattice`)
and the sub-APIs for modeling input as well as accessing the solvers.

Main API
========

.. autosummary::
    :nosignatures:
    :toctree: generated/

    Lattice

Problem Input
=============

To model the input for lattice problem solvers, create a unit-cell definition
as well as a system description using the sub-APIs below.

.. autosummary::
    :nosignatures:
    :toctree: generated/

    UnitCells
    Systems

Solvers & Results
=================

Currently, the only solver available is SCCE. It is accessed via the
sub-API :class:`scce.Jobs`.

.. autosummary::
    :nosignatures:
    :toctree: generated/

    scce.Jobs

Handlers
========

The handlers used in this module are simply named the singular version of the
class names used for the API. For example, after creating a unit-cell, you
will get an instance of the class :class:`UnitCell`. When retrieving all
unit-cells of your user account using :meth:`UnitCells.get_all`, you will
receive a list of such instances.

Most importantly, you access the results of successfully completed jobs using
the members in the class :class:`scce.Job`, which is returned when creating
the job.

.. autosummary::
    :nosignatures:
    :toctree: generated/

    UnitCell
    System
    scce.Job
"""

from qad_api.lattice.lattice_api import Lattice
from qad_api.lattice.unit_cells import UnitCells
from qad_api.lattice.systems import Systems
from qad_api.lattice.models import UnitCell, System
