"""
文件处理工具
"""
import uuid
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta
import config


class FileHandler:
    """文件管理器"""
    
    @staticmethod
    def generate_file_id(prefix: str = "") -> str:
        """
        生成唯一文件ID
        
        Args:
            prefix: 文件ID前缀
        
        Returns:
            唯一文件ID
        """
        unique_id = str(uuid.uuid4())[:8]
        if prefix:
            return f"{prefix}_{unique_id}"
        return unique_id
    
    @staticmethod
    def save_uploaded_file(file_content: bytes, original_filename: str) -> tuple[Path, str]:
        """
        保存上传的文件
        
        Args:
            file_content: 文件内容
            original_filename: 原始文件名
        
        Returns:
            (保存路径, 文件ID)
        """
        file_id = FileHandler.generate_file_id("upload")
        suffix = Path(original_filename).suffix
        filename = f"{file_id}{suffix}"
        filepath = config.UPLOAD_DIR / filename
        
        with open(filepath, 'wb') as f:
            f.write(file_content)
        
        return filepath, file_id
    
    @staticmethod
    def save_output_file(source_path: Path, prefix: str, job_id: str) -> tuple[Path, str]:
        """
        保存输出文件
        
        Args:
            source_path: 源文件路径
            prefix: 文件前缀（如desolvated, supercell）
            job_id: 作业ID
        
        Returns:
            (保存路径, 文件ID)
        """
        suffix = source_path.suffix
        file_id = f"{prefix}_{job_id[:8]}{suffix}"
        output_path = config.OUTPUT_DIR / file_id
        
        shutil.copy(source_path, output_path)
        
        return output_path, file_id
    
    @staticmethod
    def get_file_path(file_id: str, directory: Path = None) -> Optional[Path]:
        """
        获取文件路径
        
        Args:
            file_id: 文件ID
            directory: 搜索目录，默认为outputs
        
        Returns:
            文件路径，如果不存在返回None
        """
        if directory is None:
            directory = config.OUTPUT_DIR
        
        # 如果file_id已经包含扩展名
        filepath = directory / file_id
        if filepath.exists():
            return filepath
        
        # 尝试查找匹配的文件
        for file in directory.glob(f"{file_id}*"):
            return file
        
        return None
    
    @staticmethod
    def cleanup_old_files(hours: int = None):
        """
        清理过期文件
        
        Args:
            hours: 保留时间（小时），默认使用配置值
        """
        if hours is None:
            hours = config.FILE_RETENTION_HOURS
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for directory in [config.UPLOAD_DIR, config.OUTPUT_DIR]:
            for file in directory.iterdir():
                if file.is_file():
                    file_time = datetime.fromtimestamp(file.stat().st_mtime)
                    if file_time < cutoff_time:
                        file.unlink()
    
    @staticmethod
    def validate_cif_extension(filename: str) -> bool:
        """
        验证文件扩展名
        
        Args:
            filename: 文件名
        
        Returns:
            是否为有效的CIF文件
        """
        suffix = Path(filename).suffix
        return suffix in config.ALLOWED_EXTENSIONS
