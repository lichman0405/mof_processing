from ase.io import read, write
from ase.neighborlist import NeighborList, natural_cutoffs
from collections import Counter
import numpy as np

infile = "1405751.cif"  # 原始 NH2-UiO-66（带溶剂）
outfile = "NH2-UiO-66_desolvated.cif"

# 1. 读入原始结构
atoms = read(infile)
print("Original atoms:", len(atoms))
print("Cell (Å):")
print(atoms.get_cell())

symbols = np.array([a.symbol for a in atoms])
print("Element counts (original):", Counter(symbols))

# 2. 构建邻居列表（近似“成键”关系）
cutoffs = natural_cutoffs(atoms, mult=1.2)  # mult 可以之后微调
nl = NeighborList(cutoffs, self_interaction=False, bothways=True)
nl.update(atoms)

# 3. 建立邻接表
n = len(atoms)
adj = [[] for _ in range(n)]
for i in range(n):
    indices, offsets = nl.get_neighbors(i)
    for j in indices:
        adj[i].append(j)

# 4. 用 DFS/BFS 找所有连通分量
components = []
visited = [False] * n

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
        components.append(comp)

print(f"\nFound {len(components)} connected components.\n")

# 打印每个分量的元素统计，帮你判断哪个是框架
for idx, comp in enumerate(components):
    comp_syms = symbols[comp]
    counts = Counter(comp_syms)
    print(f"Component {idx}: size={len(comp)}  elements={dict(counts)}")

# 5. 找出包含 Zr 的所有分量，把它们当作框架的一部分
framework_indices = set()
for idx, comp in enumerate(components):
    comp_syms = symbols[comp]
    if "Zr" in comp_syms:
        framework_indices.update(comp)

framework_indices = sorted(framework_indices)
guest_indices = sorted(set(range(n)) - set(framework_indices))

print("\nFramework atoms:", len(framework_indices))
print("Guest/solvent atoms:", len(guest_indices))

print("Element counts (framework):", Counter(symbols[framework_indices]))
print("Element counts (guests):", Counter(symbols[guest_indices]))

# 6. 生成只包含框架的结构
framework = atoms[framework_indices]
framework.set_cell(atoms.get_cell())
framework.set_pbc(atoms.get_pbc())

write(outfile, framework)
print("\nWrote desolvated structure to:", outfile)
