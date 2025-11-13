"""
配置文件
"""
import os
from pathlib import Path

# 基础目录
BASE_DIR = Path(__file__).parent

# 目录配置
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
LOG_DIR = BASE_DIR / "logs"

# 确保目录存在
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# 文件限制
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = ['.cif', '.CIF']

# 文件保留时间（小时）
FILE_RETENTION_HOURS = 24

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 默认处理参数
DEFAULT_SUPERCELL_REPEAT = [2, 2, 2]
DEFAULT_MULT_FACTOR = 1.2
DEFAULT_SITE_TYPE = "NH2"

# 键长阈值（Å）
BOND_THRESHOLDS = {
    "C-N": 1.6,
    "N-H": 1.2,
    "N-Metal": 2.5  # N与金属的配位距离
}

# 常见MOF金属元素
COMMON_MOF_METALS = {
    'Zr', 'Cu', 'Zn', 'Fe', 'Al', 'Cr', 'Ni', 'Co', 'Mn', 
    'Mg', 'Ca', 'Ti', 'V', 'Mo', 'W', 'Cd', 'Hf', 'In'
}
