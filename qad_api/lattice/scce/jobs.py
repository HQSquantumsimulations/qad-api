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

from qad_api.core.internal import Module, Pagination
from qad_api.core.exceptions import ConsistencyError
from qad_api.lattice import System, UnitCell
from qad_api.lattice.scce import Job

from typing import List, Union
from requests import HTTPError


class Jobs(Module):
    """Sub-API for accessing the SCCE jobs of the current user.
    """

    def get_all(self) -> List[Job]:
        """Get all jobs of the current user.
        
        Returns
        -------
        jobs : List[Job]
            All jobs of the current user as a list of :class:`Job` objects.
        """
        pagination = self._get('', Pagination[Job])
        return pagination.data

    def get(self, id: str) -> Job:
        """Get a specific job of the current user.
        
        Parameters
        ----------
        id : str
            The ID of the job to be queried.

        Returns
        -------
        job : Job
            The queried job as a :class:`Job` object.

        Raises
        ------
        
        """
        return self._get(id, Job)

    def add(self, obj: Job) -> Job:
        try:
            return self._post('', obj, Job)
        except HTTPError as error:
            if error.response.status_code == 400:
                raise ConsistencyError(error.response.json()['message'], error.response) from None
            else:
                raise

    def remove(self, id: str) -> None:
        self._delete(id)

    # Convenience function
    def create(self, name: str, unit_cell: Union[UnitCell, str], system: Union[System, str]) -> Job:
        unit_cell_id = unit_cell if type(unit_cell) == str else unit_cell.id
        system_id = system if type(system) == str else system.id
        return self.add(Job(name, unit_cell_id, system_id))
