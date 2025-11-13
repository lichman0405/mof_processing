"""
Pydantic数据模型
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ProcessRequest(BaseModel):
    """处理请求参数"""
    supercell_repeat: List[int] = Field(
        default=[2, 2, 2],
        description="超胞重复次数 [nx, ny, nz]",
        example=[2, 2, 2]
    )
    site_type: str = Field(
        default="NH2",
        description="要识别的位点类型",
        example="NH2"
    )
    mult_factor: float = Field(
        default=1.2,
        description="键长判断因子",
        example=1.2
    )


class StepResult(BaseModel):
    """单个步骤的结果"""
    status: str
    logs: List[str]


class CheckResult(StepResult):
    """步骤1: 结构检查结果"""
    atom_count: int
    cell_parameters: List[float]
    element_composition: Dict[str, int]


class DesolvateResult(StepResult):
    """步骤2: 去溶剂结果"""
    framework_atoms: int
    guest_atoms: int
    components_found: int
    framework_composition: Dict[str, int]
    guest_composition: Dict[str, int]


class SiteInfo(BaseModel):
    """位点信息"""
    index: int
    element: str
    fractional: List[float]
    cartesian: List[float]
    bonded_C: List[int]
    bonded_H: List[int]


class FindSitesResult(StepResult):
    """步骤3: 位点识别结果"""
    site_type: str
    site_count: int
    sites: List[SiteInfo]


class SupercellResult(StepResult):
    """步骤4: 超胞构建结果"""
    repeat: List[int]
    original_atoms: int
    supercell_atoms: int
    original_cell: List[float]
    supercell_cell: List[float]


class FileInfo(BaseModel):
    """文件信息"""
    file_id: str
    download_url: str


class ProcessData(BaseModel):
    """处理结果数据"""
    job_id: str
    original_file: str
    processing_time: float
    steps: Dict[str, Any]
    output_files: Dict[str, FileInfo]


class ProcessResponse(BaseModel):
    """处理响应"""
    success: bool
    data: ProcessData
    message: str
    timestamp: str


class ErrorDetail(BaseModel):
    """错误详情"""
    code: str
    step: Optional[str] = None
    message: str
    details: Optional[str] = None


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = False
    error: ErrorDetail
    message: str
    timestamp: str
    data: Optional[Dict[str, Any]] = None
