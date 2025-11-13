# MOF Processing API

MOF（金属有机框架）结构处理服务 - 提供结构分析、去溶剂、位点识别和超胞构建功能。

## 📋 功能特性

- ✅ **结构分析**: 检查CIF文件的基本信息（原子数、晶胞参数、元素组成）
- ✅ **去溶剂**: 自动识别并移除客体分子，保留MOF框架（支持多种金属节点）
- ✅ **位点识别**: 识别特定官能团位点（如NH₂）
- ✅ **超胞构建**: 构建指定大小的超胞结构
- ✅ **通用性强**: 支持多种MOF类型（Zr-MOF, Cu-MOF, Zn-MOF等）
- ✅ **完整日志**: 每个步骤都有详细的日志记录
- ✅ **RESTful API**: 基于FastAPI的现代Web服务
- ✅ **Docker支持**: 容器化部署，开箱即用

## 🏗️ 项目结构

```
mof-application/
├── api/                      # API层
│   ├── main.py              # FastAPI主应用
│   └── models.py            # Pydantic数据模型
├── core/                     # 核心业务逻辑
│   ├── pipeline.py          # 工作流管道
│   ├── structure_analyzer.py # 结构分析
│   ├── desolvator.py        # 去溶剂
│   ├── site_finder.py       # 位点识别
│   └── supercell_builder.py # 超胞构建
├── utils/                    # 工具函数
│   ├── logger.py            # 日志系统
│   ├── file_handler.py      # 文件管理
│   └── exceptions.py        # 自定义异常
├── uploads/                  # 上传文件目录
├── outputs/                  # 输出文件目录
├── logs/                     # 日志目录
├── config.py                 # 配置文件
├── requirements.txt          # Python依赖
├── Dockerfile               # Docker配置
├── docker-compose.yml       # Docker Compose配置
└── README.md                # 本文件
```

## 🚀 快速开始

### 方式1: Docker部署（推荐）

```bash
# 1. 构建镜像
docker-compose build

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

服务将在 `http://localhost:8000` 启动。

### 方式2: 传统部署

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python api/main.py

# 或使用uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📡 API使用说明

### 1. 处理MOF结构（完整流程）

**端点**: `POST /api/process`

**请求参数**:
- `file`: CIF文件（必需）
- `supercell_repeat`: 超胞重复次数，JSON数组格式，如 `[2,2,2]`（可选，默认 `[2,2,2]`）
- `site_type`: 位点类型（可选，默认 `NH2`）
- `mult_factor`: 键长判断因子（可选，默认 `1.2`）

**使用curl示例**:

```bash
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@NH2-UiO-66_desolvated.cif" \
  -F "supercell_repeat=[2,2,2]" \
  -F "site_type=NH2" \
  -F "mult_factor=1.2"
```

**使用Python示例**:

```python
import requests

url = "http://localhost:8000/api/process"

with open("NH2-UiO-66_desolvated.cif", "rb") as f:
    files = {"file": f}
    data = {
        "supercell_repeat": "[2,2,2]",
        "site_type": "NH2",
        "mult_factor": 1.2
    }
    response = requests.post(url, files=files, data=data)
    result = response.json()
    
    if result["success"]:
        print(f"处理成功! 作业ID: {result['data']['job_id']}")
        print(f"用时: {result['data']['processing_time']}秒")
        
        # 下载生成的文件
        for file_type, file_info in result["data"]["output_files"].items():
            print(f"{file_type}: {file_info['download_url']}")
    else:
        print(f"处理失败: {result['message']}")
```

**成功响应示例**:

```json
{
  "success": true,
  "data": {
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "original_file": "NH2-UiO-66.cif",
    "processing_time": 2.34,
    "steps": {
      "step1_check": {
        "status": "success",
        "atom_count": 240,
        "cell_parameters": [20.7, 20.7, 20.7, 90.0, 90.0, 90.0],
        "element_composition": {"Zr": 24, "C": 144, "O": 96, "N": 8, "H": 48},
        "logs": ["开始分析结构...", "总原子数: 240"]
      },
      "step2_desolvate": {
        "status": "success",
        "framework_atoms": 240,
        "guest_atoms": 0,
        "logs": ["开始去溶剂处理...", "框架原子数: 240"]
      },
      "step3_find_sites": {
        "status": "success",
        "site_type": "NH2",
        "site_count": 8,
        "sites": [
          {
            "index": 42,
            "element": "N",
            "fractional": [0.25, 0.25, 0.25],
            "cartesian": [5.175, 5.175, 5.175],
            "bonded_C": [45],
            "bonded_H": [210, 211]
          }
        ],
        "logs": ["开始识别 NH2 位点...", "共识别出 8 个NH2位点"]
      },
      "step4_supercell": {
        "status": "success",
        "repeat": [2, 2, 2],
        "original_atoms": 240,
        "supercell_atoms": 1920,
        "logs": ["开始构建超胞: 2x2x2...", "超胞原子数: 1920"]
      }
    },
    "output_files": {
      "desolvated": {
        "file_id": "desolvated_550e8400.cif",
        "download_url": "/api/download/desolvated_550e8400.cif"
      },
      "supercell": {
        "file_id": "supercell_550e8400.cif",
        "download_url": "/api/download/supercell_550e8400.cif"
      }
    }
  },
  "message": "MOF处理流程成功完成",
  "timestamp": "2025-11-13T10:30:00Z"
}
```

### 2. 下载生成的CIF文件

**端点**: `GET /api/download/{file_id}`

**示例**:

```bash
curl -O "http://localhost:8000/api/download/supercell_550e8400.cif"
```

### 3. 健康检查

**端点**: `GET /api/health`

```bash
curl http://localhost:8000/api/health
```

### 4. 清理过期文件

**端点**: `DELETE /api/cleanup?hours=24`

```bash
curl -X DELETE "http://localhost:8000/api/cleanup?hours=24"
```

## 📚 API文档

启动服务后，访问以下地址查看交互式API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## ⚙️ 配置说明

编辑 `config.py` 文件可以修改以下配置：

```python
# 文件大小限制
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# 文件保留时间
FILE_RETENTION_HOURS = 24

# 默认处理参数
DEFAULT_SUPERCELL_REPEAT = [2, 2, 2]
DEFAULT_MULT_FACTOR = 1.2
DEFAULT_SITE_TYPE = "NH2"

# 键长阈值
BOND_THRESHOLDS = {
    "C-N": 1.6,
    "N-H": 1.2,
    "N-Metal": 2.5  # N与金属的配位距离
}

# 支持的MOF金属元素
COMMON_MOF_METALS = {
    'Zr', 'Cu', 'Zn', 'Fe', 'Al', 'Cr', 'Ni', 'Co', 'Mn', 
    'Mg', 'Ca', 'Ti', 'V', 'Mo', 'W', 'Cd', 'Hf', 'In'
}
```

### **去溶剂策略**

系统采用智能策略识别MOF框架：

1. **优先策略**: 查找包含金属节点的连通分量（支持18种常见MOF金属）
2. **备用策略**: 如果没有检测到金属，选择最大的连通分量作为框架
3. **通用性**: 适用于Zr-MOF, Cu-MOF, Zn-MOF等多种类型

环境变量：
- `LOG_LEVEL`: 日志级别（DEBUG, INFO, WARNING, ERROR）
- `FILE_RETENTION_HOURS`: 文件保留时间（小时）

## 🔧 开发说明

### 运行测试

```bash
# 使用现有的CIF文件测试
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@1405751.cif"
```

### 查看日志

```bash
# 应用日志
tail -f logs/mof_api.log

# Docker日志
docker-compose logs -f
```

## 📝 错误处理

API使用标准的HTTP状态码：

- `200`: 成功
- `400`: 请求参数错误
- `404`: 文件不存在
- `413`: 文件过大
- `500`: 服务器内部错误

错误响应格式：

```json
{
  "success": false,
  "error": {
    "code": "DESOLVATION_FAILED",
    "step": "step2_desolvate",
    "message": "未找到包含Zr的框架结构",
    "details": "..."
  },
  "message": "处理失败: 未找到包含Zr的框架结构",
  "timestamp": "2025-11-13T10:30:00Z"
}
```

## 🐛 故障排查

### 问题1: 端口被占用

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### 问题2: Docker容器无法启动

```bash
# 查看详细日志
docker-compose logs

# 重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 问题3: ASE无法解析CIF文件

确保CIF文件格式正确，可以使用其他工具（如VESTA）先验证文件。

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题请提交Issue或联系开发者。
