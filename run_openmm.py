

import sys

from simtk import unit
from simtk.openmm import app, XmlSerializer, Platform, CustomBondForce

from openmm_tools import setup_run_simulation

if __name__ == "__main__":

    simpletag, mediumtag, complextag = "simple", "medium", "complex"
    system_file      = "system-{}.xml"

    platform = Platform.getPlatformByName("OpenCL")
    prmtop = app.AmberPrmtopFile("input.prmtop")
    linear_pdb = app.PDBFile("linear.pdb")
    system = prmtop.createSystem(nonbondedMethod=app.NoCutoff)

    with open(system_file.format(simpletag), "w") as f:
        f.write(XmlSerializer.serialize(system))

    setup_run_simulation(
        prmtop.topology, linear_pdb.positions,
        system, platform, simpletag
    )

    distance_restraints = CustomBondForce("-k*(r-r0)^2")
    distance_restraints.addPerBondParameter("k")
    distance_restraints.addPerBondParameter("r0")
    distance_restraints.addBond(10, 1050, [0.5*unit.nanometer, 100])
    system.addForce(distance_restraints)

    with open(system_file.format(mediumtag), "w") as f:
        f.write(XmlSerializer.serialize(system))

    setup_run_simulation(
        prmtop.topology, linear_pdb.positions,
        system, platform, mediumtag
    )
