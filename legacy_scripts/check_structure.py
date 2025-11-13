# check_structure.py
from ase.io import read
from collections import Counter

atoms = read("1405751.cif")  # NH2-UiO-66 CCDC 1405751

print("Total atoms:", len(atoms))
print("Cell (Å):")
print(atoms.get_cell())

symbols = [a.symbol for a in atoms]
print("Element counts:", Counter(symbols))
