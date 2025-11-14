from typing import List, Sequence
from collections import Counter
import numpy as np
from ase import Atoms
from ase.neighborlist import NeighborList, natural_cutoffs
from ase.io import read
from pathlib import Path

def identify_linkers(atoms: Atoms, metal_symbols: Sequence[str] = ("Zr",),
                     zr_o_cutoff: float = 2.5) -> List[List[int]]:
    """
    在含金属 MOF 中识别有机 linker（不含金属、也不含节点 O）的原子索引。
    返回值：list of linkers，每个 linker 是一组原始 atoms 索引。
    """
    symbols = np.array(atoms.get_chemical_symbols(), dtype=str)
    all_indices = np.arange(len(atoms))

    # 1. 找金属原子
    metal_mask = np.isin(symbols, metal_symbols)
    metal_indices = all_indices[metal_mask]

    # 2. 找所有 O 中，哪些是“节点 O”：靠近 Zr 的
    O_indices = all_indices[symbols == "O"]
    node_O_indices = []

    for oi in O_indices:
        dists = atoms.get_distances(oi, metal_indices, mic=True)
        if len(dists) > 0 and dists.min() < zr_o_cutoff:
            node_O_indices.append(oi)

    node_O_indices = np.array(node_O_indices, dtype=int)

    # 3. 非节点原子 = 非金属 且 非节点O
    node_set = set(metal_indices.tolist()) | set(node_O_indices.tolist())
    non_node_mask = np.array([i not in node_set for i in all_indices])
    non_node_indices = all_indices[non_node_mask]

    # 4. 在“去掉节点（Zr + 节点O）”后的结构上建邻居表
    atoms_org = atoms[non_node_indices]

    cutoffs = natural_cutoffs(atoms_org, mult=1.2)
    nl = NeighborList(cutoffs, self_interaction=False, bothways=True)
    nl.update(atoms_org)

    n = len(atoms_org)
    adj = [[] for _ in range(n)]
    for i in range(n):
        indices, offsets = nl.get_neighbors(i)
        for j in indices:
            adj[i].append(j)

    # 5. DFS 连通分量
    visited = [False] * n
    components_local: List[List[int]] = []

    for i in range(n):
        if not visited[i]:
            stack = [i]
            comp = []
            visited[i] = True
            while stack:
                v = stack.pop()
                comp.append(v)
                for nb in adj[v]:
                    if not visited[nb]:
                        visited[nb] = True
                        stack.append(nb)
            components_local.append(comp)

    # 6. 映射回原结构索引
    linkers_global: List[List[int]] = []
    for comp in components_local:
        global_idx = non_node_indices[comp]
        linkers_global.append(sorted(global_idx.tolist()))

    # 小小统计一下，方便你检查
    sizes = [len(c) for c in linkers_global]
    print(f"Found {len(linkers_global)} candidate linkers.")
    print(f"Linker sizes: {Counter(sizes)}")

    return linkers_global


def main():
    infile = Path(r"C:\Users\lishi\code\mof-application\legacy_scripts\NH2-UiO-66_desolvated.cif")  # 你自己改路径
    atoms = read(infile)
    linkers = identify_linkers(atoms, metal_symbols=("Zr",))

    print(f"Total atoms: {len(atoms)}")
    print(f"Found {len(linkers)} linkers.")
    for i, comp in enumerate(linkers[:5]):  # 前5个看看长度
        print(f"Linker {i}: {len(comp)} atoms, indices (first 10): {comp[:10]}")

if __name__ == "__main__":
    main()