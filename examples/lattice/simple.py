from qad_api import QAD_API

# Creating an QAD_API instance will authenticate the user with the backend
qad = QAD_API()

# Create a unit-cell
unit_cell = qad.lattice.unit_cells.create('Helo world', {
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
system = qad.lattice.systems.create('Helo world', {
    "system": {
        "cluster_size": [8, 1, 1],
        "system_size": [1, 1, 1],
        "spinful": False,
        "N": 2,
        "system_boundary_condition": 'periodic'
    },
    "run": {
        "states": 1
    }
})
print(f"System created: {system.id}")

# Create a job (will start to run it automatically)
job = qad.lattice.scce.jobs.create('Helo world', unit_cell, system)
print(f"Job created: {job.id}")

# Wait for the job to be done (when using co-routines: await job.wait())
job.wait_blocking()

# Download the result to a local file
job.download_result(f"./{job.id}.h5")
print("Downloaded result")