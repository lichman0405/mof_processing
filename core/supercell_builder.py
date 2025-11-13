"""
步骤4: 超胞构建模块
构建MOF结构的超胞
"""
from pathlib import Path
from typing import Dict, Any, List
from ase import Atoms
from ase.io import write
from utils.logger import JobLogger
from utils.exceptions import SupercellError
import config


class SupercellBuilder:
    """超胞构建器"""
    
    def __init__(self, logger: JobLogger):
        self.logger = logger
    
    def build_supercell(
        self,
        atoms: Atoms,
        output_path: Path,
        repeat: List[int] = None
    ) -> Dict[str, Any]:
        """
        构建超胞
        
        Args:
            atoms: ASE Atoms对象
            output_path: 输出文件路径
            repeat: 重复次数 [nx, ny, nz]
        
        Returns:
            超胞构建结果
        
        Raises:
            SupercellError: 超胞构建失败
        """
        if repeat is None:
            repeat = config.DEFAULT_SUPERCELL_REPEAT
        
        self.logger.info(f"开始构建超胞: {repeat[0]}x{repeat[1]}x{repeat[2]}")
        
        try:
            original_atom_count = len(atoms)
            original_cell = atoms.get_cell()
            original_cell_params = original_cell.cellpar()
            
            self.logger.info(f"原始结构原子数: {original_atom_count}")
            self.logger.info(
                f"原始晶胞: a={original_cell_params[0]:.3f}, "
                f"b={original_cell_params[1]:.3f}, "
                f"c={original_cell_params[2]:.3f} Å"
            )
            
            # 构建超胞
            super_atoms = atoms.repeat(tuple(repeat))
            
            supercell_atom_count = len(super_atoms)
            supercell_cell = super_atoms.get_cell()
            supercell_cell_params = supercell_cell.cellpar()
            
            self.logger.info(f"超胞原子数: {supercell_atom_count}")
            self.logger.info(
                f"超胞晶胞: a={supercell_cell_params[0]:.3f}, "
                f"b={supercell_cell_params[1]:.3f}, "
                f"c={supercell_cell_params[2]:.3f} Å"
            )
            
            # 保存文件
            write(str(output_path), super_atoms)
            self.logger.info(f"超胞结构已保存: {output_path.name}")
            
            result = {
                "status": "success",
                "repeat": repeat,
                "original_atoms": original_atom_count,
                "supercell_atoms": supercell_atom_count,
                "original_cell": [round(p, 4) for p in original_cell_params],
                "supercell_cell": [round(p, 4) for p in supercell_cell_params],
                "output_path": output_path,
                "logs": self.logger.get_logs()
            }
            
            return result
            
        except Exception as e:
            error_msg = f"超胞构建失败: {str(e)}"
            self.logger.error(error_msg)
            raise SupercellError(error_msg, details=str(e))
