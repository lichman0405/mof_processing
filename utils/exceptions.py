"""
自定义异常类
"""

class MOFProcessingError(Exception):
    """MOF处理基础异常"""
    def __init__(self, message: str, step: str = None, details: str = None):
        self.message = message
        self.step = step
        self.details = details
        super().__init__(self.message)


class InvalidCIFError(MOFProcessingError):
    """CIF文件无效或解析失败"""
    def __init__(self, message: str, details: str = None):
        super().__init__(message, step="step1_check", details=details)


class DesolvationError(MOFProcessingError):
    """去溶剂过程失败"""
    def __init__(self, message: str, details: str = None):
        super().__init__(message, step="step2_desolvate", details=details)


class SiteFinderError(MOFProcessingError):
    """位点识别失败"""
    def __init__(self, message: str, details: str = None):
        super().__init__(message, step="step3_find_sites", details=details)


class SupercellError(MOFProcessingError):
    """超胞构建失败"""
    def __init__(self, message: str, details: str = None):
        super().__init__(message, step="step4_supercell", details=details)
