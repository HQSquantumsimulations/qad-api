# The QAD-API Python library

QAD-API is a Python library for accessing the (REST) API of
[QAD Cloud](https://qad.quantumsimulations.de/).

## Note

As this library servers just as a Python frontend to QAD Cloud, you first need
an account on that platform before using this Python library.

## Installation

We do not yet provide a PyPi package. The recommended way to install QAD-API
is to clone this repository, and pip install it from the local folder:

```shell
git clone https://github.com/HQSquantumsimulations/qad_api.git
pip install -e qad_api/
```

## Usage

Use QAD-API by importing the class `QAD_API` from the root package `qad_api`.
Create an instance of this class and use the members to access the API.

To find out more about the API functionality, see the 
[documentation of QAD API](https://qad_api.readthedocs.io/en/latest/).

## Example

One simple example is listed below to get you started quickly.

Here you see how we create an instance of `QAD_API`, which will authenticate
the user with the backend. The first time the user does this, they are asked
to open a link with their browser and use their credentials to authenticate
with the backend (OAuth2). 

After that, we use that instance to access API functionality. Using this, we
create a unit-cell and a system for the lattice-based problem solver "SCCE".
We also create a job for that solver by passing the just-created handlers,
and wait for the job to be finished. This will take some time, after which we
download the result file to the local file system.

```python
from qad_api import QAD_API

# Creating an QAD_API instance will authenticate the user with the backend
qad = QAD_API()

# Create a unit-cell
unit_cell = qad.lattice.unit_cells.create('1D XXZ', {
    "unitcell": {
        "atoms": [
            ['0', 'X', [0, 0, 0], 0.0, 0.0]
        ],
        "lattice_vectors": [
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ],
        "bonds": [
            ['0', '0', [1, 0, 0], -1.0, 0]
        ]
    }
})
print(f"Unit cell created: {unit_cell.id}")

# Create a system
system = qad.lattice.systems.create('1D XXZ', {
    "system": {
        "cluster_size": [42, 1, 1],
        "system_size": [1, 1, 1],
        "spinful": False,
        "N": 21,
        "system_boundary_condition": 'periodic'
    },
    "run": {
        "states": 1
    }
})
print(f"System created: {system.id}")

# Create a job (will start to run it automatically)
job = qad.lattice.scce.jobs.create('1D XXZ Test', unit_cell, system)
print(f"Job created: {job.id}")

# Wait for the job to be done (you might want to use co-routines: await job.wait())
job.wait_blocking()

# Download the result to a local file
job.download_result(f"./{job.id}.h5")
print(f"Downloaded result")
```
