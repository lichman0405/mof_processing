#!/bin/bash
# MOF Processing Platform - 一键部署脚本 (Linux/Mac)

set -e

echo "======================================"
echo "  MOF Processing Platform 部署工具  "
echo "======================================"
echo ""

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查Docker
echo -e "${YELLOW}[1/5] 检查Docker环境...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: 未安装Docker${NC}"
    echo "请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: 未安装Docker Compose${NC}"
    echo "请先安装Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker环境正常${NC}"
echo ""

# 停止旧容器
echo -e "${YELLOW}[2/5] 停止旧容器...${NC}"
docker-compose down 2>/dev/null || true
echo -e "${GREEN}✓ 清理完成${NC}"
echo ""

# 构建镜像
echo -e "${YELLOW}[3/5] 构建Docker镜像...${NC}"
docker-compose build --no-cache
echo -e "${GREEN}✓ 构建完成${NC}"
echo ""

# 启动服务
echo -e "${YELLOW}[4/5] 启动服务...${NC}"
docker-compose up -d
echo -e "${GREEN}✓ 服务已启动${NC}"
echo ""

# 等待服务就绪
echo -e "${YELLOW}[5/5] 等待服务就绪...${NC}"
sleep 5

# 健康检查
if curl -s http://localhost/health > /dev/null; then
    echo -e "${GREEN}✓ 前端服务正常${NC}"
else
    echo -e "${RED}✗ 前端服务异常${NC}"
fi

if curl -s http://localhost/api/health > /dev/null; then
    echo -e "${GREEN}✓ 后端服务正常${NC}"
else
    echo -e "${RED}✗ 后端服务异常${NC}"
fi

echo ""
echo "======================================"
echo -e "${GREEN}🎉 部署成功!${NC}"
echo "======================================"
echo ""
echo "访问地址:"
echo "  • 前端界面: http://localhost"
echo "  • API文档:  http://localhost/docs"
echo "  • ReDoc:    http://localhost/redoc"
echo ""
echo "管理命令:"
echo "  • 查看日志: docker-compose logs -f"
echo "  • 停止服务: docker-compose down"
echo "  • 重启服务: docker-compose restart"
echo ""
