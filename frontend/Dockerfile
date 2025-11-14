# 阶段1: 构建前端
FROM node:20-alpine AS builder

LABEL maintainer="MOF Processing Frontend"
LABEL description="MOF前端构建阶段"

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖 (使用国内镜像加速)
RUN npm config set registry https://registry.npmmirror.com && \
    npm ci --only=production

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# 阶段2: 使用Nginx提供静态文件
FROM nginx:alpine

LABEL maintainer="MOF Processing Frontend"
LABEL description="MOF前端生产镜像"

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从构建阶段复制打包文件
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]
