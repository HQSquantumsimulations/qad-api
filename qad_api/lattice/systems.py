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
from qad_api.lattice.models.system import System
from qad_api.core.internal.models.pagination import Pagination
from qad_api.core.exceptions import ConsistencyError

from typing import List, Union, cast
from requests import HTTPError
import yaml


class Systems(Module):
    """Sub-API for accessing the systems of the current user.
    """

    def get_all(self) -> List[System]:
        """Retrieve a list of all systems of the current user."""
        pagination = self._get('', Pagination[System])
        return pagination.data

    def get(self, id: str) -> System:
        """Retrieve a specific system by its id."""
        return self._get(id, System)

    def add(self, obj: System) -> System:
        """Adds a system, given a :class:`System` handler object."""
        try:
            return self._post('', obj, System)
        except HTTPError as error:
            if error.response.status_code == 400:
                raise ConsistencyError(error.response.json()['message'], error.response) from None
            else:
                raise

    def update(self, obj: System) -> System:
        """Updates an existing system, given an (updated) handler object."""
        try:
            return self._put(obj.id, obj, System)
        except HTTPError as error:
            if error.response.status_code == 400:
                raise ConsistencyError(error.response.json()['message'], error.response) from None
            else:
                raise

    def remove(self, id: str) -> None:
        """Removes a system entirely (cannot be undone!)."""
        self._delete(id)

    # Convenience function
    def create(self, name: str, configuration: Union[str, dict]) -> System:
        """Creates and adds a system, given its configuration.
        
        This is a short-hand version of first creating an instance of
        :class:`System` and then passing that instance to
        :meth:`Systems.add`.
        """
        if type(configuration) == str:
            configuration_str = cast(str, configuration)
        else:
            configuration_str = yaml.safe_dump(configuration)

        return self.add(System(
            name=name,
            configuration=configuration_str
        ))
