# find_nh2_sites.py
from ase.io import read
from ase.neighborlist import NeighborList, natural_cutoffs
import numpy as np

infile = "NH2-UiO-66_desolvated.cif"  # 就是刚才写出的那个

atoms = read(infile)
print("Atoms in desolvated structure:", len(atoms))

symbols = np.array(atoms.get_chemical_symbols(), dtype=str)
scaled_pos = atoms.get_scaled_positions()
cart_pos = atoms.get_positions()

# 建邻居列表
cutoffs = natural_cutoffs(atoms, mult=1.2)
nl = NeighborList(cutoffs, self_interaction=False, bothways=True)
nl.update(atoms)

nh_like_indices = []

for i, sym in enumerate(symbols):
    if sym != "N":
        continue

    indices, offsets = nl.get_neighbors(i)
    neigh_syms = symbols[indices]

    # 统计不同元素邻居
    C_neighbors = [j for j, s in zip(indices, neigh_syms) if s == "C"]
    H_neighbors = [j for j, s in zip(indices, neigh_syms) if s == "H"]
    Zr_neighbors = [j for j, s in zip(indices, neigh_syms) if s == "Zr"]

    # 进一步用距离过滤一下（防止隔着周期近但不成键）
    C_bonded = []
    H_bonded = []

    for j in C_neighbors:
        d = atoms.get_distance(i, j, mic=True)
        if d < 1.6:  # 典型 C-N 键长 ~1.3-1.5 Å
            C_bonded.append(j)

    for j in H_neighbors:
        d = atoms.get_distance(i, j, mic=True)
        if d < 1.2:  # N-H ~1.0 Å 左右
            H_bonded.append(j)

    Zr_bonded = []
    for j in Zr_neighbors:
        d = atoms.get_distance(i, j, mic=True)
        if d < 2.5:  # N→Zr 如果有配位，多半在这个范围；我们反而要排除这种怪物
            Zr_bonded.append(j)

    # 判据：
    #  1) 至少有一个 C-N 键
    #  2) 没有明显的 N-Zr 配位
    if len(C_bonded) == 1 and len(Zr_bonded) == 0:
        nh_like_indices.append(i)
        print("=" * 50)
        print(f"N atom index: {i}")
        print(f"  bonded C neighbors: {C_bonded}")
        print(f"  bonded H neighbors: {H_bonded}")
        print(f"  (C count = {len(C_bonded)}, H count = {len(H_bonded)})")

        x, y, z = scaled_pos[i]
        print("  Fractional coordinates:")
        print(f"    {x:.4f}  {y:.4f}  {z:.4f}")
        X, Y, Z = cart_pos[i]
        print("  Cartesian coordinates (Å):")
        print(f"    {X:.4f}  {Y:.4f}  {Z:.4f}")

print("\nTotal N atoms:", (symbols == "N").sum())
print("N identified as linker NHx:", len(nh_like_indices))
print("Indices:", nh_like_indices)
