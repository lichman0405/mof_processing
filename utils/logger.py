"""
日志配置模块
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler
import config


def setup_logger(
    name: str = "mof_api",
    log_file: Optional[Path] = None,
    level: str = None
) -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件路径
        level: 日志级别
    
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    log_level = getattr(logging, level or config.LOG_LEVEL)
    logger.setLevel(log_level)
    
    # 创建格式化器
    formatter = logging.Formatter(
        config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file is None:
        log_file = config.LOG_DIR / "mof_api.log"
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "mof_api") -> logging.Logger:
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
    
    Returns:
        日志记录器
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


class JobLogger:
    """
    作业日志收集器，用于收集单个处理作业的日志
    """
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.logs = []
        self.logger = get_logger()
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志消息"""
        log_entry = f"[{self.job_id}] {message}"
        self.logs.append(message)
        
        # 同时写入主日志
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(log_entry)
    
    def info(self, message: str):
        """INFO级别日志"""
        self.log(message, "INFO")
    
    def warning(self, message: str):
        """WARNING级别日志"""
        self.log(message, "WARNING")
    
    def error(self, message: str):
        """ERROR级别日志"""
        self.log(message, "ERROR")
    
    def get_logs(self) -> list:
        """获取所有收集的日志"""
        return self.logs.copy()
