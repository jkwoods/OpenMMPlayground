#!/usr/bin/env python

import sys
from itertools import combinations
import numpy as np

from simtk.openmm import app


# TODO what units do we want?

#INPUT: 1. name of orig
#	2. name of linear (-pdb)
#	3. dist k
_default_force = 3.
_default_catom = "cb"
# distance in sequence space
_min_res_distance = 2
_extra_force_count = 0


# TODO not adequate for general case!
is_protein = lambda res: res.name.lower() not in {"hoh","h2o","tip3"}

if __name__ == "__main__" or len(sys.argv) == 1:
    # TODO use argparser
    dist_kforce = _default_force
    rcsb_pdbfile = "1ubq.pdb"
    linear_pdbfile = "linear.pdb"
    if len(sys.argv) > 1:
        rcsb_pdbfile = sys.argv[1]
        linear_pdbfile = sys.argv[2]
        if len(sys.argv) == 4:
            dist_kforce = float(sys.argv[3])

    # NOTE always use the actual class name
    #      to initialize data structures,
    #      with {} this might be dict or set
    # dict of {res #: (linear serial #, RCSB serial #)}
    serials_map = dict()
    rcsb_pdb = app.PDBFile(rcsb_pdbfile)
    linear_pdb = app.PDBFile(linear_pdbfile)

    # Because in case there are waters first, etc.
    #  - we are assuming the linear_pdb is ONLY protein
    #    AND every residue is present in the RCSB file
    custom_residue_index = -1
    for residue in linear_pdb.topology.residues():
        custom_residue_index += 1
        for atom in residue.atoms():
            if atom.name.lower() == _default_catom:
                serials_map.update(
                    {(residue.name, custom_residue_index): [atom.index]}
                )

    custom_residue_index = -1
    for residue in rcsb_pdb.topology.residues():
        if is_protein(residue):
            custom_residue_index += 1
            for atom in residue.atoms():
                if atom.name.lower() == _default_catom:
                    try:
                        serials_map[(residue.name, custom_residue_index)].append(atom.index)
                    except KeyError:
                        raise Exception("Mismatch detected between residue sequences")

    rcsb_positions = rcsb_pdb.positions
    linear_positions = linear_pdb.positions

    restraints = ""
    for (a1,i1), (a2,i2) in combinations(serials_map.items(), 2):

        # Skip if have 'close neighbors'
        if a2[1] - a1[1] <= _min_res_distance:
            continue

        r1 = rcsb_positions[i1[1]]
        r2 = rcsb_positions[i2[1]]
        d  = np.linalg.norm(r2 - r1)

        restraints += "{0:7d} {1:7d} {2:9.4f} {3:5.2f}\n".format(
            i1[0], i2[0], d._value, dist_kforce
        )

    with open("restraints.txt", "w") as f:
        f.write(restraints)

