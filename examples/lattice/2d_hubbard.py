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

from qad_api import QAD_API

# Creating an QAD_API instance will authenticate the user with the backend
qad = QAD_API()

# Create a unit-cell
unit_cell = qad.lattice.unit_cells.create('2D Hubbard', { 
    "unitcell": {
        "atoms": [ #                    eps,   U 
            ['0', 'A', [  0,   0, 0],  0.01, 1.0 ],
            ['1', 'B', [  0, 0.5, 0], -0.01, 1.0 ],
            ['2', 'B', [0.5,   0, 0], -0.01, 1.0 ],
            ['3', 'A', [0.5, 0.5, 0],  0.01, 1.0 ]
        ],
        "bonds": [ #                 t    U
            ['0', '1', [0, 0, 0], -1.0, 0.0 ],
            ['0', '2', [0, 0, 0], -1.0, 0.0 ],
            ['1', '3', [0, 0, 0], -1.0, 0.0 ],
            ['2', '3', [0, 0, 0], -1.0, 0.0 ],
            ['2', '0', [1, 0, 0], -1.0, 0.0 ],
            ['3', '1', [1, 0, 0], -1.0, 0.0 ],
            ['1', '0', [0, 1, 0], -1.0, 0.0 ],
            ['3', '2', [0, 1, 0], -1.0, 0.0 ]
        ],
        "lattice_vectors": [
            [1, 0, 0],
            [0, 1, 0]
        ]
    }
})
print(f"Unit cell created: {unit_cell.id}")

# Create a system
system = qad.lattice.systems.create('2D Hubbard', {
    "system": {
        "cluster_size":    [1, 1, 1],   # measured in unit cells
        "system_size":     [2, 2, 1],    # measured in clusters
        "cluster_offset":  [0, 0, 0], # measured in clusters
        "system_boundary_condition": "periodic"
    }
})
print(f"System created: {system.id}")

# Create a job (will start to run it automatically)
job = qad.lattice.scce.jobs.create('2D Hubbard', unit_cell, system)
print(f"Job created: {job.id}")

# Wait for the job to be done (when using co-routines: await job.wait())
job.wait_blocking()

# Download the result to a local file
job.download_result(f"./{job.id}.h5")
print("Downloaded result")
