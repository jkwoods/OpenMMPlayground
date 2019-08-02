
import sys

from simtk import unit
from simtk.openmm import app, LangevinIntegrator

statedata_freq   = 1000
structure_freq   = 10000
simulation_steps = 50000

simulation_file  = "simulation-{}.pdb"


def setup_run_simulation(topology, positions, system, platform, tag=""):

    integrator = LangevinIntegrator(
        100*unit.kelvin, 1/unit.picosecond, 0.002*unit.picoseconds
    )

    simulation = app.Simulation(
        topology, system, integrator, platform
    )

    simulation.context.setPositions(positions)
    simulation.minimizeEnergy()

    simulation.reporters.append(app.StateDataReporter(
        sys.stdout, statedata_freq, separator=" | ", step=True,
        time=True, potentialEnergy=True, kineticEnergy=True,
        totalEnergy=True, temperature=True, speed=True
    ))

    simulation.reporters.append(app.PDBReporter(
        simulation_file.format(tag), structure_freq
    ))

    simulation.step(simulation_steps)

    del simulation
