"""
步骤2: 去溶剂模块
移除客体分子，保留MOF框架
"""
from pathlib import Path
from typing import Dict, Any
from collections import Counter
import numpy as np
from ase import Atoms
from ase.io import write
from ase.neighborlist import NeighborList, natural_cutoffs
from utils.logger import JobLogger
from utils.exceptions import DesolvationError
import config


class Desolvator:
    """去溶剂处理器"""
    
    def __init__(self, logger: JobLogger):
        self.logger = logger
    
    def desolvate(
        self,
        atoms: Atoms,
        output_path: Path,
        mult_factor: float = None
    ) -> Dict[str, Any]:
        """
        去除溶剂分子，保留框架
        
        Args:
            atoms: ASE Atoms对象
            output_path: 输出文件路径
            mult_factor: 键长判断因子
        
        Returns:
            去溶剂结果
        
        Raises:
            DesolvationError: 去溶剂失败
        """
        if mult_factor is None:
            mult_factor = config.DEFAULT_MULT_FACTOR
        
        self.logger.info("开始去溶剂处理")
        self.logger.info(f"使用键长因子: {mult_factor}")
        
        try:
            n = len(atoms)
            symbols = np.array([atom.symbol for atom in atoms])
            
            # 构建邻居列表
            self.logger.info("构建邻居列表...")
            cutoffs = natural_cutoffs(atoms, mult=mult_factor)
            nl = NeighborList(cutoffs, self_interaction=False, bothways=True)
            nl.update(atoms)
            
            # 构建邻接表
            adj = [[] for _ in range(n)]
            for i in range(n):
                indices, offsets = nl.get_neighbors(i)
                for j in indices:
                    adj[i].append(j)
            
            # 查找连通分量
            self.logger.info("分析连通分量...")
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
            
            self.logger.info(f"发现 {len(components)} 个连通分量")
            
            # 识别框架：策略1 - 尝试查找金属节点，策略2 - 选择最大分量
            framework_indices = set()
            framework_components = []
            
            # 使用配置的MOF金属元素列表
            common_metals = config.COMMON_MOF_METALS
            
            # 先尝试找包含金属的分量
            metal_components = []
            for idx, comp in enumerate(components):
                comp_syms = symbols[comp]
                comp_counts = Counter(comp_syms)
                metals_in_comp = set(comp_syms) & common_metals
                
                if metals_in_comp:
                    metal_components.append((idx, len(comp), metals_in_comp))
                    self.logger.info(
                        f"分量 {idx}: 包含金属 {metals_in_comp} (大小={len(comp)}, 组成={dict(comp_counts)})"
                    )
            
            if metal_components:
                # 如果找到金属分量，选择最大的那个
                largest_metal_comp = max(metal_components, key=lambda x: x[1])
                framework_idx = largest_metal_comp[0]
                framework_indices.update(components[framework_idx])
                self.logger.info(f"选择分量 {framework_idx} 作为框架 (包含金属: {largest_metal_comp[2]})")
            else:
                # 如果没有金属，选择最大的分量作为框架
                largest_comp_idx = max(range(len(components)), key=lambda i: len(components[i]))
                framework_indices.update(components[largest_comp_idx])
                comp_syms = symbols[components[largest_comp_idx]]
                comp_counts = Counter(comp_syms)
                self.logger.info(
                    f"未检测到金属元素，选择最大分量 {largest_comp_idx} 作为框架 "
                    f"(大小={len(components[largest_comp_idx])}, 组成={dict(comp_counts)})"
                )
            
            framework_indices = sorted(framework_indices)
            guest_indices = sorted(set(range(n)) - set(framework_indices))
            
            # 创建索引映射：新索引 -> 原始索引
            framework_indices_map = {new_idx: old_idx for new_idx, old_idx in enumerate(framework_indices)}
            
            # 统计信息
            framework_composition = Counter(symbols[framework_indices])
            guest_composition = Counter(symbols[guest_indices])
            
            self.logger.info(f"框架原子数: {len(framework_indices)}")
            self.logger.info(f"客体原子数: {len(guest_indices)}")
            self.logger.info(f"框架组成: {dict(framework_composition)}")
            if guest_indices:
                self.logger.info(f"客体组成: {dict(guest_composition)}")
            
            # 生成去溶剂结构
            framework = atoms[framework_indices]
            framework.set_cell(atoms.get_cell())
            framework.set_pbc(atoms.get_pbc())
            
            # 保存文件
            write(str(output_path), framework)
            self.logger.info(f"去溶剂结构已保存: {output_path.name}")
            
            result = {
                "status": "success",
                "framework_atoms": len(framework_indices),
                "guest_atoms": len(guest_indices),
                "components_found": len(components),
                "framework_composition": dict(framework_composition),
                "guest_composition": dict(guest_composition) if guest_indices else {},
                "framework_object": framework,  # 传递给下一步
                "framework_indices_map": framework_indices_map,  # 索引映射
                "output_path": output_path,
                "logs": self.logger.get_logs()
            }
            
            return result
            
        except DesolvationError:
            raise
        except Exception as e:
            error_msg = f"去溶剂处理失败: {str(e)}"
            self.logger.error(error_msg)
            raise DesolvationError(error_msg, details=str(e))
