"""
步骤1: 结构分析模块
检查CIF文件的基本信息
"""
from pathlib import Path
from typing import Dict, Any
from collections import Counter
from ase.io import read
from ase import Atoms
from utils.logger import JobLogger
from utils.exceptions import InvalidCIFError


class StructureAnalyzer:
    """CIF结构分析器"""
    
    def __init__(self, logger: JobLogger):
        self.logger = logger
    
    def analyze(self, cif_path: Path) -> Dict[str, Any]:
        """
        分析CIF文件结构
        
        Args:
            cif_path: CIF文件路径
        
        Returns:
            结构分析结果
        
        Raises:
            InvalidCIFError: CIF文件解析失败
        """
        self.logger.info(f"开始分析结构: {cif_path.name}")
        
        try:
            # 读取CIF文件
            atoms = read(str(cif_path))
            
            # 获取基本信息
            atom_count = len(atoms)
            cell = atoms.get_cell()
            cell_params = list(cell.cellpar())
            
            # 统计元素组成
            symbols = [atom.symbol for atom in atoms]
            composition = dict(Counter(symbols))
            
            self.logger.info(f"总原子数: {atom_count}")
            self.logger.info(f"晶胞参数: a={cell_params[0]:.3f}, b={cell_params[1]:.3f}, c={cell_params[2]:.3f} Å")
            self.logger.info(f"晶胞角度: α={cell_params[3]:.2f}°, β={cell_params[4]:.2f}°, γ={cell_params[5]:.2f}°")
            self.logger.info(f"元素组成: {composition}")
            
            result = {
                "status": "success",
                "atom_count": atom_count,
                "cell_parameters": [round(p, 4) for p in cell_params],
                "element_composition": composition,
                "atoms_object": atoms,  # 传递给下一步
                "logs": self.logger.get_logs()
            }
            
            return result
            
        except Exception as e:
            error_msg = f"无法解析CIF文件: {str(e)}"
            self.logger.error(error_msg)
            raise InvalidCIFError(error_msg, details=str(e))
