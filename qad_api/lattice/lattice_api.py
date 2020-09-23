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

from qad_api.core.internal.module import Module


class Lattice(Module):
    """API for solving lattice problems."""

    @property
    def unit_cells(self):
        """Sub-API for accessing the unit-cells of the current user.
        
        This attribute is an instance of the :class:`.UnitCells` class.
        For the list of available sub-functionalities of this API
        see the attribute's documentation of :class:`.UnitCells`.
        """

        from qad_api.lattice.unit_cells import UnitCells
        return self._submodule(UnitCells, 'unit-cells/')


    @property
    def systems(self):
        """Sub-API for accessing the systems of the current user.

        This attribute is an instance of the :class:`.Systems` class.
        For the list of available sub-functionalities of this API
        see the attribute's documentation of :class:`.Systems`.
        """

        from qad_api.lattice.systems import Systems
        return self._submodule(Systems, 'systems/')


    @property
    def scce(self):
        """Sub-API for accessing the SCCE solver.

        This attribute is an instance of the :class:`.SCCE` class.
        For the list of available sub-functionalities of this API
        see the attribute's documentation of :class:`.SCCE`.
        """

        from qad_api.lattice.scce.scce import SCCE
        return self._submodule(SCCE, 'scce/')