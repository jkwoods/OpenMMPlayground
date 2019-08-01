# None of this actually works
# just saving snippets that can be used for tests later

# Test for correct matching between atom indices
rcsbs=list(filter(lambda r: is_protein(r), rcsb_pdb.topology.residues()))[::10]
lines=list(filter(lambda r: is_protein(r), linear_pdb.topology.residues()))[::10]

# Currently don't have any verification these are the same atoms...
list(map(lambda l: list(filter(lambda a: a.name == "CB", l.atoms()))[0].index, lines))
>>> [4, 169, 328, 491, 640, 814, 963, 1132]
list(map(lambda l: list(filter(lambda a: a.name == "CB", l.atoms()))[0].index, rcsbs))
>>> [4, 82, 159, 237, 315, 397, 478, 559]
