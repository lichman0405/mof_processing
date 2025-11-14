# MOF Processing Platform

🚀 **完整的MOF（金属有机框架）结构处理平台** - 提供现代化的Web界面和强大的后端API服务

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/Vue-3.5+-brightgreen)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 平台特性

### 🎯 核心功能
- ✅ **结构分析**: 自动检查CIF文件的基本信息（原子数、晶胞参数、元素组成）
- ✅ **智能去溶剂**: 自动识别并移除客体分子，保留MOF框架（支持18种金属节点）
- ✅ **位点识别**: 精确识别特定官能团位点（如NH₂、COOH等）
- ✅ **超胞构建**: 快速构建任意大小的超胞结构
- ✅ **批量处理**: 支持多文件并发处理
- ✅ **实时日志**: 完整的处理日志和进度跟踪

### 🎨 前端特性
- 💎 **现代化UI**: 基于Vue 3 + Element Plus的精美界面
- 🎭 **拖拽上传**: 支持文件拖拽上传，即时预览
- 📊 **数据可视化**: 处理结果表格展示，清晰直观
- 📋 **日志查看**: 美观的日志面板，支持语法高亮
- 📱 **响应式设计**: 完美适配各种屏幕尺寸
- ⚡ **性能优化**: Vite构建，秒级热更新

### 🔧 技术特性
- 🐳 **容器化部署**: Docker一键部署，开箱即用
- 🌐 **反向代理**: Nginx统一入口，避免CORS
- 📡 **RESTful API**: 标准化的API接口设计
- 🔒 **类型安全**: TypeScript + Pydantic全栈类型检查
- 📝 **自动文档**: Swagger/ReDoc交互式API文档
- 🩺 **健康检查**: 完善的服务监控和健康检查

## 🏗️ 系统架构

```
┌─────────────────────────────────────────┐
│          用户浏览器 (Browser)            │
└──────────────┬──────────────────────────┘
               │ http://localhost
               ↓
┌─────────────────────────────────────────┐
│      Nginx 反向代理 (Port 80)           │
│  ┌─────────────────────────────────┐   │
│  │  /        → 前端静态文件         │   │
│  │  /api/*   → 后端API代理          │   │
│  │  /docs    → API文档代理          │   │
│  └─────────────────────────────────┘   │
└──────────┬─────────────────┬────────────┘
           │                 │
           ↓                 ↓
┌──────────────────┐ ┌──────────────────┐
│  Frontend        │ │  Backend         │
│  (Vue 3)         │ │  (FastAPI)       │
│  - Element Plus  │ │  - ASE           │
│  - TypeScript    │ │  - Pipeline      │
│  - Pinia         │ │  - JobLogger     │
└──────────────────┘ └──────────────────┘
```

## 📁 项目结构

```
mof-application/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/      # Vue组件
│   │   │   ├── FileUpload.vue
│   │   │   ├── ProcessingPanel.vue
│   │   │   ├── ResultsViewer.vue
│   │   │   └── LogViewer.vue
│   │   ├── stores/          # Pinia状态管理
│   │   ├── services/        # API服务
│   │   └── types/           # TypeScript类型
│   ├── Dockerfile           # 前端容器配置
│   └── nginx.conf           # Nginx配置
├── api/                      # API层
│   └── main.py              # FastAPI主应用
├── core/                     # 核心业务逻辑
│   ├── pipeline.py          # 工作流管道
│   ├── structure_analyzer.py
│   ├── desolvator.py
│   ├── site_finder.py
│   └── supercell_builder.py
├── utils/                    # 工具模块
├── docker-compose.yml       # 容器编排配置
├── deploy.sh / deploy.ps1   # 一键部署脚本
└── README.md

## 🚀 快速开始

### 📦 前置要求

- **Docker** >= 20.10
- **Docker Compose** >= 2.0

### ⚡ 一键部署（推荐）

**Windows 用户**:
```powershell
.\deploy.ps1
```

**Linux/Mac 用户**:
```bash
chmod +x deploy.sh
./deploy.sh
```

部署脚本会自动:
1. ✅ 检查Docker环境
2. ✅ 停止旧容器
3. ✅ 构建镜像（前端 + 后端）
4. ✅ 启动服务
5. ✅ 健康检查

### 🌐 访问服务

部署成功后，打开浏览器访问:

- **Web界面**: http://localhost
- **API文档**: http://localhost/docs
- **ReDoc**: http://localhost/redoc

### 🛠️ 手动部署

如果需要手动控制部署过程:

```bash
# 1. 构建镜像
docker-compose build

# 2. 启动服务（后台运行）
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

### 💻 开发模式

**前端开发**:
```bash
cd frontend
npm install
npm run dev  # 启动开发服务器 http://localhost:5173
```

**后端开发**:
```bash
pip install -r requirements.txt
python api/main.py  # 启动后端服务 http://localhost:8000
```

## 📖 使用指南

### 🎬 快速上手

1. **上传CIF文件**
   - 拖拽CIF文件到上传区域
   - 或点击选择文件
   - 支持最大50MB文件

2. **设置处理参数**
   - 超胞重复: 设置xyz三个方向的重复次数 (默认2×2×2)
   - 位点类型: 指定要识别的官能团 (如NH2)
   - 键长因子: 调整键长判断阈值 (默认1.2)

3. **开始处理**
   - 点击"开始处理"按钮
   - 实时查看处理进度（4个步骤）
   - 查看每步详细日志

4. **查看结果**
   - 处理概览: 作业ID、用时等信息
   - 步骤详情: 每步的数据表格展示
   - 日志查看: 展开日志面板查看详细信息

5. **下载文件**
   - 下载去溶剂结构文件 (.cif)
   - 下载超胞结构文件 (.cif)

### 🎯 处理流程

```
步骤1: 结构检查
  ↓ 读取CIF文件，分析原子数、晶胞参数、元素组成
  
步骤2: 去除溶剂
  ↓ 识别并移除客体分子，保留MOF框架
  
步骤3: 识别位点
  ↓ 定位特定官能团（如NH2）的位置和坐标
  
步骤4: 构建超胞
  ↓ 根据指定倍数构建超胞结构
  
✅ 生成去溶剂和超胞CIF文件
```

## 📡 API使用说明

### REST API 接口

完整的API文档请访问: http://localhost/docs

#### 核心接口

**1. 处理MOF结构** - `POST /api/process`

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

**2. 下载文件** - `GET /api/download/{file_id}`

**3. 健康检查** - `GET /api/health`

**4. 清理过期文件** - `DELETE /api/cleanup?hours=24`

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

## 🔧 运维管理

### 容器管理

```bash
# 查看运行状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f frontend
docker-compose logs -f backend

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 完全清理（包括卷）
docker-compose down -v
```

### 性能监控

```bash
# 查看资源使用
docker stats

# 查看容器详情
docker inspect mof-frontend
docker inspect mof-backend
```

### 数据备份

```bash
# 备份上传和输出文件
tar -czf backup_$(date +%Y%m%d).tar.gz uploads/ outputs/ logs/

# 恢复备份
tar -xzf backup_20251114.tar.gz
```

## 🐛 故障排查

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

### 常见问题

**1. 端口80被占用**
```powershell
# Windows
netstat -ano | findstr :80
Stop-Process -Id <PID> -Force

# Linux/Mac
sudo lsof -ti:80 | xargs kill -9
```

**2. 容器无法启动**
```bash
# 查看详细日志
docker-compose logs

# 重新构建（清除缓存）
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**3. 前端无法连接后端**
- 检查后端容器是否运行: `docker ps`
- 检查网络连接: `docker network inspect mof-application_mof-network`
- 查看Nginx日志: `docker-compose logs frontend`

**4. 文件上传失败**
- 检查文件大小是否超过50MB
- 确认CIF文件格式正确
- 查看后端日志: `docker-compose logs backend`

**5. 内存不足**
```bash
# 增加Docker内存限制（Docker Desktop设置）
# 或修改docker-compose.yml添加资源限制
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
```

## 📝 技术栈

### 后端
- **FastAPI** - 现代Python Web框架
- **ASE** (Atomic Simulation Environment) - 原子结构处理
- **NumPy** - 数值计算
- **Pydantic** - 数据验证
- **Uvicorn** - ASGI服务器

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全
- **Element Plus** - UI组件库
- **Pinia** - 状态管理
- **Axios** - HTTP客户端
- **Vite** - 构建工具

### 基础设施
- **Docker** - 容器化
- **Nginx** - 反向代理与静态文件服务
- **Docker Compose** - 容器编排

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👥 联系方式

- 提交Issue: https://github.com/lichman0405/mof_processing/issues
- 项目主页: https://github.com/lichman0405/mof_processing

## 🌟 致谢

感谢以下开源项目:
- [ASE](https://wiki.fysik.dtu.dk/ase/) - 原子模拟环境
- [FastAPI](https://fastapi.tiangolo.com/) - Web框架
- [Vue.js](https://vuejs.org/) - 前端框架
- [Element Plus](https://element-plus.org/) - UI组件库

---

**Made with ❤️ for MOF researchers**
