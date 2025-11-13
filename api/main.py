"""
FastAPI主应用
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional
import json

from core.pipeline import MOFPipeline
from utils.logger import setup_logger
from utils.file_handler import FileHandler
import config

# 初始化日志
logger = setup_logger()

# 创建FastAPI应用
app = FastAPI(
    title="MOF Processing API",
    description="MOF（金属有机框架）结构处理API - 提供结构分析、去溶剂、位点识别和超胞构建功能",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径 - API信息"""
    return {
        "name": "MOF Processing API",
        "version": "1.0.0",
        "description": "MOF结构处理服务",
        "endpoints": {
            "process": "POST /api/process - 处理CIF文件（完整流程）",
            "download": "GET /api/download/{file_id} - 下载生成的CIF文件",
            "health": "GET /api/health - 健康检查"
        }
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "mof-processing-api"
    }


@app.post("/api/process")
async def process_mof(
    file: UploadFile = File(..., description="CIF文件"),
    supercell_repeat: Optional[str] = Form(
        default="[2,2,2]",
        description="超胞重复次数，JSON格式的数组，如 [2,2,2]"
    ),
    site_type: Optional[str] = Form(
        default="NH2",
        description="要识别的位点类型"
    ),
    mult_factor: Optional[float] = Form(
        default=1.2,
        description="键长判断因子"
    )
):
    """
    处理MOF结构（完整流程）
    
    执行顺序：
    1. 检查结构
    2. 去除溶剂
    3. 识别NH2位点
    4. 构建超胞
    
    返回完整的处理结果和生成文件的下载链接
    """
    logger.info(f"收到处理请求: {file.filename}")
    
    try:
        # 验证文件类型
        if not FileHandler.validate_cif_extension(file.filename):
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_FILE_TYPE",
                    "message": f"不支持的文件类型，仅支持 {', '.join(config.ALLOWED_EXTENSIONS)} 文件"
                }
            )
        
        # 验证文件大小
        content = await file.read()
        if len(content) > config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail={
                    "code": "FILE_TOO_LARGE",
                    "message": f"文件过大，最大允许 {config.MAX_FILE_SIZE / 1024 / 1024:.1f} MB"
                }
            )
        
        # 保存上传的文件
        upload_path, file_id = FileHandler.save_uploaded_file(content, file.filename)
        logger.info(f"文件已保存: {upload_path}")
        
        # 解析参数
        try:
            repeat = json.loads(supercell_repeat)
            if not isinstance(repeat, list) or len(repeat) != 3:
                raise ValueError("supercell_repeat必须是包含3个整数的数组")
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_PARAMETERS",
                    "message": f"参数格式错误: {str(e)}"
                }
            )
        
        # 执行处理流程
        pipeline = MOFPipeline()
        result = pipeline.process(
            cif_path=upload_path,
            supercell_repeat=repeat,
            site_type=site_type,
            mult_factor=mult_factor,
            output_dir=config.OUTPUT_DIR
        )
        
        # 返回结果
        return JSONResponse(
            content=result,
            status_code=200 if result["success"] else 500
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": f"服务器内部错误: {str(e)}"
            }
        )


@app.get("/api/download/{file_id}")
async def download_file(file_id: str):
    """
    下载生成的CIF文件
    
    Args:
        file_id: 文件ID（从process接口返回）
    
    Returns:
        CIF文件
    """
    logger.info(f"下载请求: {file_id}")
    
    # 查找文件
    file_path = FileHandler.get_file_path(file_id, config.OUTPUT_DIR)
    
    if not file_path or not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail={
                "code": "FILE_NOT_FOUND",
                "message": f"文件不存在: {file_id}"
            }
        )
    
    return FileResponse(
        path=str(file_path),
        filename=file_id,
        media_type="chemical/x-cif"
    )


@app.delete("/api/cleanup")
async def cleanup_files(hours: Optional[int] = None):
    """
    清理过期文件
    
    Args:
        hours: 保留时间（小时），默认使用配置值
    
    Returns:
        清理结果
    """
    try:
        FileHandler.cleanup_old_files(hours)
        logger.info(f"已清理过期文件（保留时间: {hours or config.FILE_RETENTION_HOURS}小时）")
        return {
            "success": True,
            "message": f"已清理保留时间超过 {hours or config.FILE_RETENTION_HOURS} 小时的文件"
        }
    except Exception as e:
        logger.error(f"清理文件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "code": "CLEANUP_FAILED",
                "message": str(e)
            }
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
