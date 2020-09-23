# The QAD-API Python library

The QAD-API Python library is a library for accessing the (REST) API of
[QAD Cloud](https://qad.quantumsimulations.de/).

## Note

As this library serves simply as a Python front-end to the QAD Cloud,
you will first need an account on this platform, before using the library.

## Installation

We do not yet provide a PyPi package. The recommended method for installing
QAD-API is to clone the following repository, and then "pip install" it
from the appropriate local folder:

```shell
git clone https://github.com/HQSquantumsimulations/qad-api.git
cd qad-api
pip install -e qad_api/
```

## Usage

The QAD-API is utilized by importing the class `QAD_API` from the root package
`qad_api`. In order access the API, one must create an instance of this class.

To learn more about the API functionality, please refer to the 
[documentation of QAD_API](https://qad_api.readthedocs.io/en/latest/).

## Example

To get started with the QAD_API, we provide a quick and simple example here.

We will create an instance of `QAD_API`, which will authenticate the user
with the back-end. The first time this is done, the user will be asked
to open a link in a browser and use their credentials to authenticate
with the back-end (OAuth2).

After this, we use the instance of `QAD_API` to access the API functionality.
We create a unit-cell and a system for the lattice-based problem solver "SCCE,"
and also create a job for that solver by passing the recently created handlers,
then wait for the job to finish. This will take some time, after which we
download the results file to the local file system.

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
            [1, 0, 0]
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
