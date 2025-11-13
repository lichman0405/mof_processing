"""
步骤3: 位点识别模块
识别特定类型的官能团位点（如NH2）
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
from ase import Atoms
from ase.neighborlist import NeighborList, natural_cutoffs
from utils.logger import JobLogger
from utils.exceptions import SiteFinderError
import config


class SiteFinder:
    """官能团位点识别器"""
    
    def __init__(self, logger: JobLogger):
        self.logger = logger
    
    def find_sites(
        self,
        atoms: Atoms,
        site_type: str = None,
        mult_factor: float = None,
        original_indices_map: Dict[int, int] = None
    ) -> Dict[str, Any]:
        """
        识别官能团位点
        
        Args:
            atoms: ASE Atoms对象
            site_type: 位点类型（NH2, OH等）
            mult_factor: 键长判断因子
            original_indices_map: 原始索引映射（新索引 -> 原始索引）
        
        Returns:
            位点识别结果
        
        Raises:
            SiteFinderError: 位点识别失败
        """
        if site_type is None:
            site_type = config.DEFAULT_SITE_TYPE
        if mult_factor is None:
            mult_factor = config.DEFAULT_MULT_FACTOR
        
        self.logger.info(f"开始识别 {site_type} 位点")
        
        try:
            if site_type.upper() == "NH2":
                return self._find_nh2_sites(atoms, mult_factor, original_indices_map)
            else:
                error_msg = f"不支持的位点类型: {site_type}"
                self.logger.error(error_msg)
                raise SiteFinderError(error_msg)
                
        except SiteFinderError:
            raise
        except Exception as e:
            error_msg = f"位点识别失败: {str(e)}"
            self.logger.error(error_msg)
            raise SiteFinderError(error_msg, details=str(e))
    
    def _find_nh2_sites(
        self, 
        atoms: Atoms, 
        mult_factor: float,
        original_indices_map: Optional[Dict[int, int]] = None
    ) -> Dict[str, Any]:
        """识别NH2位点"""
        symbols = np.array(atoms.get_chemical_symbols(), dtype=str)
        scaled_pos = atoms.get_scaled_positions()
        cart_pos = atoms.get_positions()
        
        # 建邻居列表
        cutoffs = natural_cutoffs(atoms, mult=mult_factor)
        nl = NeighborList(cutoffs, self_interaction=False, bothways=True)
        nl.update(atoms)
        
        nh2_sites = []
        n_indices = np.where(symbols == "N")[0]
        
        self.logger.info(f"总共有 {len(n_indices)} 个N原子")
        
        for i in n_indices:
            indices, offsets = nl.get_neighbors(i)
            neigh_syms = symbols[indices]
            
            # 统计邻居
            C_neighbors = [j for j, s in zip(indices, neigh_syms) if s == "C"]
            H_neighbors = [j for j, s in zip(indices, neigh_syms) if s == "H"]
            # 检查所有可能的金属邻居
            metal_neighbors = [j for j, s in zip(indices, neigh_syms) if s in config.COMMON_MOF_METALS]
            
            # 距离过滤
            C_bonded = []
            for j in C_neighbors:
                d = atoms.get_distance(i, j, mic=True)
                if d < config.BOND_THRESHOLDS["C-N"]:
                    C_bonded.append(j)
            
            H_bonded = []
            for j in H_neighbors:
                d = atoms.get_distance(i, j, mic=True)
                if d < config.BOND_THRESHOLDS["N-H"]:
                    H_bonded.append(j)
            
            metal_bonded = []
            for j in metal_neighbors:
                d = atoms.get_distance(i, j, mic=True)
                if d < config.BOND_THRESHOLDS["N-Metal"]:
                    metal_bonded.append(j)
            
            # NH2判据：至少1个C-N键，无N-金属配位
            if len(C_bonded) >= 1 and len(metal_bonded) == 0:
                # 使用原始索引（如果提供了映射）
                original_index = original_indices_map[i] if original_indices_map else i
                original_C_bonded = [original_indices_map[j] if original_indices_map else j for j in C_bonded]
                original_H_bonded = [original_indices_map[j] if original_indices_map else j for j in H_bonded]
                
                site_info = {
                    "index": int(original_index),  # 使用原始索引
                    "framework_index": int(i),  # 去溶剂后的索引（供参考）
                    "element": "N",
                    "fractional": [round(x, 6) for x in scaled_pos[i].tolist()],
                    "cartesian": [round(x, 6) for x in cart_pos[i].tolist()],
                    "bonded_C": [int(x) for x in original_C_bonded],
                    "bonded_H": [int(x) for x in original_H_bonded]
                }
                nh2_sites.append(site_info)
                
                self.logger.info(
                    f"位点 {len(nh2_sites)-1}: N[原始:{original_index}] 分数坐标={site_info['fractional']}, "
                    f"C邻居={len(C_bonded)}, H邻居={len(H_bonded)}"
                )
        
        self.logger.info(f"共识别出 {len(nh2_sites)} 个NH2位点")
        
        result = {
            "status": "success",
            "site_type": "NH2",
            "site_count": len(nh2_sites),
            "sites": nh2_sites,
            "logs": self.logger.get_logs()
        }
        
        return result
