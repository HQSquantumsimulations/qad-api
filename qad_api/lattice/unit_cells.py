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
from qad_api.lattice.models.unit_cell import UnitCell
from qad_api.core.internal.models.pagination import Pagination
from qad_api.core.exceptions import ConsistencyError

from typing import List, Union, cast
from requests import HTTPError
import yaml


class UnitCells(Module):
    """Sub-API for accessing the unit-cells of the current user.
    """

    def get_all(self) -> List[UnitCell]:
        """Retrieve a list of all unit-cells of the current user."""
        pagination = self._get('', Pagination[UnitCell])
        return pagination.data

    def get(self, id: str) -> UnitCell:
        """Retrieve a specific unit-cell by its id."""
        return self._get(id, UnitCell)

    def add(self, obj: UnitCell) -> UnitCell:
        """Adds a unit-cell, given a :class:`UnitCell` handler object."""
        try:
            return self._post('', obj, UnitCell)
        except HTTPError as error:
            if error.response.status_code == 400:
                raise ConsistencyError(error.response.json()['message'], error.response) from None
            else:
                raise

    def update(self, obj: UnitCell) -> UnitCell:
        """Updates an existing unit-cell, given an (updated) handler object."""
        try:
            return self._put(obj.id, obj, UnitCell)
        except HTTPError as error:
            if error.response.status_code == 400:
                raise ConsistencyError(error.response.json()['message'], error.response) from None
            else:
                raise

    def remove(self, id: str) -> None:
        """Removes a unit-cell entirely (cannot be undone!)."""
        self._delete(id)

    # Convenience function
    def create(self, name: str, configuration: Union[str, dict]) -> UnitCell:
        """Creates and adds a unit-cell, given its configuration.
        
        This is a short-hand version of first creating an instance of
        :class:`UnitCell` and then passing that instance to
        :meth:`UnitCells.add`.
        """
        if type(configuration) == str:
            configuration_str = cast(str, configuration)
        else:
            configuration_str = yaml.safe_dump(configuration)

        return self.add(UnitCell(
            name=name,
            configuration=configuration_str
        ))
