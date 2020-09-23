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

"""Handler which represents an SCCE job."""

from dataclasses import dataclass
from qad_api.core.internal import JobBase, readonly_field


@dataclass
class Job(JobBase):
    """Handler which represents an SCCE job.

    For creating a new job, do not construct a new object of this class
    directly but rather use :meth:`scce.Jobs.create()`, like in this example:

    .. code-block:: python

        my_unit_cell = qad.lattice.unit_cells.create("My Unit-Cell", ...)
        my_system = qad.lattice.systems.create("My System", ...)
        my_job = qad.lattice.scce.jobs.create("My SCCE Job", my_unit_cell, my_system)

    More attributes, such as execution status, and methods to wait for and
    fetch the result of the job are found in :class:`JobBase`.

    .. code-block:: python

        await my_job.wait()
        my_job.download_result("my_job.hdf")
        

    Args:
        name: The name of the job.
        unit_cell_id: The ID of the unit-cell to use for the job.
        system_id: The ID of the system to use for the job.
    
    """

    unit_cell_id: str
    system_id: str

    original_system_name: str       = readonly_field()
    original_unit_cell_name: str    = readonly_field()
    configuration: str              = readonly_field()
