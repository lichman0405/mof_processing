# build_supercell.py
from ase.io import read, write

infile = "NH2-UiO-66_desolvated.cif"
outfile = "NH2-UiO-66_2x2x2.cif"

atoms = read(infile)
print("Original cell:")
print("  Atoms:", len(atoms))
print("  Cell (Å):")
print(atoms.get_cell())

# 2x2x2 超胞
super_atoms = atoms.repeat((2, 2, 2))

print("\nSupercell (2x2x2):")
print("  Atoms:", len(super_atoms))
print("  Cell (Å):")
print(super_atoms.get_cell())

write(outfile, super_atoms)
print("\nWrote supercell to:", outfile)
