from qad_api import QAD_API

qad = QAD_API()


unit_cell_config = {
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
}

system_config = {
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
}


unit_cell = qad.lattice.unit_cells.create('1D XXZ', unit_cell_config)
print(f"Unit cell created: {unit_cell.id}")

system = qad.lattice.systems.create('1D XXZ', system_config)
print(f"System created: {system.id}")

job = qad.lattice.scce.jobs.create('1D XXZ Test', unit_cell, system)
print(f"Job created: {job.id}")

job.wait_blocking()

job.download_result(f"./{job.id}.h5")
print(f"Downloaded result")
