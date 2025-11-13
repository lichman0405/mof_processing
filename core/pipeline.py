"""
MOF处理Pipeline - 一体化工作流
按顺序执行: 检查结构 → 去溶剂 → 识别位点 → 构建超胞
"""
import uuid
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from .structure_analyzer import StructureAnalyzer
from .desolvator import Desolvator
from .site_finder import SiteFinder
from .supercell_builder import SupercellBuilder
from utils.logger import JobLogger
from utils.file_handler import FileHandler
from utils.exceptions import MOFProcessingError


class MOFPipeline:
    """MOF处理管道 - 统一管理整个处理流程"""
    
    def __init__(self, job_id: str = None):
        """
        初始化Pipeline
        
        Args:
            job_id: 作业ID，不提供则自动生成
        """
        self.job_id = job_id or str(uuid.uuid4())
        self.logger = JobLogger(self.job_id)
        
        # 初始化各个处理模块
        self.analyzer = StructureAnalyzer(self.logger)
        self.desolvator = Desolvator(self.logger)
        self.site_finder = SiteFinder(self.logger)
        self.supercell_builder = SupercellBuilder(self.logger)
    
    def process(
        self,
        cif_path: Path,
        supercell_repeat: List[int] = None,
        site_type: str = None,
        mult_factor: float = None,
        output_dir: Path = None
    ) -> Dict[str, Any]:
        """
        执行完整的MOF处理流程
        
        Args:
            cif_path: 输入CIF文件路径
            supercell_repeat: 超胞重复次数 [nx, ny, nz]
            site_type: 要识别的位点类型
            mult_factor: 键长判断因子
            output_dir: 输出目录
        
        Returns:
            完整的处理结果
        
        Raises:
            MOFProcessingError: 处理过程中的任何错误
        """
        start_time = time.time()
        
        self.logger.info("="*60)
        self.logger.info(f"开始MOF处理流程 - 作业ID: {self.job_id}")
        self.logger.info(f"输入文件: {cif_path.name}")
        self.logger.info("="*60)
        
        result = {
            "success": False,
            "data": {
                "job_id": self.job_id,
                "original_file": cif_path.name,
                "processing_time": 0,
                "steps": {},
                "output_files": {}
            },
            "message": "",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        try:
            # ============ 步骤1: 检查结构 ============
            self.logger.info("\n[步骤1/4] 检查结构...")
            step1_result = self.analyzer.analyze(cif_path)
            result["data"]["steps"]["step1_check"] = self._format_step_result(step1_result)
            
            atoms = step1_result["atoms_object"]
            
            # ============ 步骤2: 去溶剂 ============
            self.logger.info("\n[步骤2/4] 去除溶剂...")
            desolvated_path = self._get_temp_path("desolvated.cif")
            step2_result = self.desolvator.desolvate(
                atoms=atoms,
                output_path=desolvated_path,
                mult_factor=mult_factor
            )
            result["data"]["steps"]["step2_desolvate"] = self._format_step_result(step2_result)
            
            # 保存去溶剂文件到输出目录
            if output_dir:
                saved_path, file_id = FileHandler.save_output_file(
                    desolvated_path,
                    "desolvated",
                    self.job_id
                )
                result["data"]["output_files"]["desolvated"] = {
                    "file_id": file_id,
                    "download_url": f"/api/download/{file_id}"
                }
            
            framework = step2_result["framework_object"]
            
            # ============ 步骤3: 识别位点 ============
            self.logger.info("\n[步骤3/4] 识别NH2位点...")
            step3_result = self.site_finder.find_sites(
                atoms=framework,
                site_type=site_type,
                mult_factor=mult_factor
            )
            result["data"]["steps"]["step3_find_sites"] = self._format_step_result(step3_result)
            
            # ============ 步骤4: 构建超胞 ============
            self.logger.info("\n[步骤4/4] 构建超胞...")
            supercell_path = self._get_temp_path("supercell.cif")
            step4_result = self.supercell_builder.build_supercell(
                atoms=framework,
                output_path=supercell_path,
                repeat=supercell_repeat
            )
            result["data"]["steps"]["step4_supercell"] = self._format_step_result(step4_result)
            
            # 保存超胞文件到输出目录
            if output_dir:
                saved_path, file_id = FileHandler.save_output_file(
                    supercell_path,
                    "supercell",
                    self.job_id
                )
                result["data"]["output_files"]["supercell"] = {
                    "file_id": file_id,
                    "download_url": f"/api/download/{file_id}"
                }
            
            # ============ 完成 ============
            processing_time = time.time() - start_time
            result["data"]["processing_time"] = round(processing_time, 3)
            result["success"] = True
            result["message"] = "MOF处理流程成功完成"
            
            self.logger.info("="*60)
            self.logger.info(f"处理完成! 总用时: {processing_time:.2f}秒")
            self.logger.info("="*60)
            
            return result
            
        except MOFProcessingError as e:
            # 已知的处理错误
            processing_time = time.time() - start_time
            result["data"]["processing_time"] = round(processing_time, 3)
            result["error"] = {
                "code": e.__class__.__name__.replace("Error", "").upper() + "_FAILED",
                "step": e.step,
                "message": e.message,
                "details": e.details
            }
            result["message"] = f"处理失败: {e.message}"
            
            self.logger.error(f"处理失败: {e.message}")
            
            return result
            
        except Exception as e:
            # 未预期的错误
            processing_time = time.time() - start_time
            result["data"]["processing_time"] = round(processing_time, 3)
            result["error"] = {
                "code": "INTERNAL_ERROR",
                "step": "unknown",
                "message": str(e),
                "details": str(type(e).__name__)
            }
            result["message"] = f"内部错误: {str(e)}"
            
            self.logger.error(f"未预期的错误: {str(e)}")
            
            return result
    
    def _format_step_result(self, step_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化步骤结果，移除内部对象
        
        Args:
            step_result: 步骤原始结果
        
        Returns:
            格式化后的结果
        """
        # 复制结果并移除ASE对象
        formatted = step_result.copy()
        formatted.pop("atoms_object", None)
        formatted.pop("framework_object", None)
        formatted.pop("output_path", None)
        
        return formatted
    
    def _get_temp_path(self, filename: str) -> Path:
        """
        获取临时文件路径
        
        Args:
            filename: 文件名
        
        Returns:
            临时文件路径
        """
        from config import OUTPUT_DIR
        return OUTPUT_DIR / f"temp_{self.job_id[:8]}_{filename}"
