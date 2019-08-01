

import sys

from simtk.openmm import app, XmlSerializer, LangevinIntegrator, Platform
from simtk import unit

if __name__ == "__main__":

    prmtop = app.AmberPrmtopFile('input.prmtop')
    # NOTE we already have the coords from linear_pdb
    #inpcrd = app.AmberInpcrdFile('input.inpcrd')

    system = prmtop.createSystem(nonbondedMethod=app.NoCutoff)
    with open("system-noadds.xml", "w") as f:
        f.write(XmlSerializer.serialize(system))

    integrator = LangevinIntegrator(100*unit.kelvin, 1/unit.picosecond, 0.001*unit.picoseconds)

    platform = Platform.getPlatformByName("OpenCL")
    simulation = app.Simulation(prmtop.topology, system, integrator, platform)
    simulation.context.setPositions(linear_pdb.positions)
    simulation.minimizeEnergy()

    simulation.reporters.append(app.StateDataReporter(
        sys.stdout, 1000, separator=" | ", step=True,
        time=True, potentialEnergy=True, kineticEnergy=True,
        totalEnergy=True, temperature=True, speed=True
    ))

    simulation.reporters.append(app.PDBReporter("simulation.pdb", 10000))
    simulation.step(50000)


