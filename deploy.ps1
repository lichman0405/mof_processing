# MOF Processing Platform - 一键部署脚本 (Windows PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  MOF Processing Platform 部署工具  " -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 检查Docker
Write-Host "[1/5] 检查Docker环境..." -ForegroundColor Yellow
try {
    docker --version | Out-Null
    docker-compose --version | Out-Null
    Write-Host "✓ Docker环境正常" -ForegroundColor Green
} catch {
    Write-Host "错误: 未安装Docker或Docker Compose" -ForegroundColor Red
    Write-Host "请先安装Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 停止旧容器
Write-Host "[2/5] 停止旧容器..." -ForegroundColor Yellow
docker-compose down 2>$null
Write-Host "✓ 清理完成" -ForegroundColor Green
Write-Host ""

# 构建镜像
Write-Host "[3/5] 构建Docker镜像..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟时间，请耐心等待..." -ForegroundColor Gray
docker-compose build --no-cache
Write-Host "✓ 构建完成" -ForegroundColor Green
Write-Host ""

# 启动服务
Write-Host "[4/5] 启动服务..." -ForegroundColor Yellow
docker-compose up -d
Write-Host "✓ 服务已启动" -ForegroundColor Green
Write-Host ""

# 等待服务就绪
Write-Host "[5/5] 等待服务就绪..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 健康检查
try {
    Invoke-WebRequest -Uri "http://localhost/health" -UseBasicParsing -TimeoutSec 5 | Out-Null
    Write-Host "✓ 前端服务正常" -ForegroundColor Green
} catch {
    Write-Host "✗ 前端服务异常" -ForegroundColor Red
}

try {
    Invoke-WebRequest -Uri "http://localhost/api/health" -UseBasicParsing -TimeoutSec 5 | Out-Null
    Write-Host "✓ 后端服务正常" -ForegroundColor Green
} catch {
    Write-Host "✗ 后端服务异常" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "🎉 部署成功!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "访问地址:" -ForegroundColor White
Write-Host "  • 前端界面: " -NoNewline; Write-Host "http://localhost" -ForegroundColor Cyan
Write-Host "  • API文档:  " -NoNewline; Write-Host "http://localhost/docs" -ForegroundColor Cyan
Write-Host "  • ReDoc:    " -NoNewline; Write-Host "http://localhost/redoc" -ForegroundColor Cyan
Write-Host ""
Write-Host "管理命令:" -ForegroundColor White
Write-Host "  • 查看日志: " -NoNewline; Write-Host "docker-compose logs -f" -ForegroundColor Yellow
Write-Host "  • 停止服务: " -NoNewline; Write-Host "docker-compose down" -ForegroundColor Yellow
Write-Host "  • 重启服务: " -NoNewline; Write-Host "docker-compose restart" -ForegroundColor Yellow
Write-Host ""
