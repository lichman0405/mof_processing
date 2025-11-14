<script setup lang="ts">
import { onMounted } from 'vue'
import { useMofStore } from '@/stores/mof'
import FileUpload from '@/components/FileUpload.vue'
import ProcessingPanel from '@/components/ProcessingPanel.vue'
import ResultsViewer from '@/components/ResultsViewer.vue'

const mofStore = useMofStore()

onMounted(() => {
  // 检查API连接
  mofStore.checkHealth()
})
</script>

<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="header-content">
        <div class="header-left">
          <el-icon :size="32" color="#409eff"><Histogram /></el-icon>
          <h1 class="app-title">MOF Processing Platform</h1>
        </div>
        <div class="header-right">
          <el-space :size="16">
            <el-tooltip content="API服务状态" placement="bottom">
              <el-badge :is-dot="true" :type="mofStore.isApiHealthy ? 'success' : 'danger'">
                <el-icon :size="24">
                  <Connection v-if="mofStore.isApiHealthy" />
                  <CircleClose v-else />
                </el-icon>
              </el-badge>
            </el-tooltip>
            <el-tooltip content="查看文档" placement="bottom">
              <el-button
                text
                circle
                :icon="Document"
                @click="() => window.open('http://localhost:8000/docs', '_blank')"
              />
            </el-tooltip>
          </el-space>
        </div>
      </div>
    </header>

    <!-- 主体内容 -->
    <main class="app-main">
      <el-container>
        <!-- 左侧控制面板 -->
        <el-aside width="450px" class="control-panel">
          <div class="panel-content">
            <FileUpload />
            <ProcessingPanel />
          </div>
        </el-aside>

        <!-- 右侧结果展示 -->
        <el-main class="results-panel">
          <ResultsViewer />
        </el-main>
      </el-container>
    </main>

    <!-- 底部状态栏 -->
    <footer class="app-footer">
      <div class="footer-content">
        <div class="footer-left">
          <el-text size="small" type="info">
            MOF Processing API v1.0.0 | Powered by Vue 3 + Element Plus
          </el-text>
        </div>
        <div class="footer-right" v-if="mofStore.jobId">
          <el-text size="small" type="info">
            Job ID: {{ mofStore.jobId.substring(0, 8) }}...
          </el-text>
          <el-divider direction="vertical" />
          <el-text size="small" type="info">
            Processing Time: {{ mofStore.processingTime.toFixed(2) }}s
          </el-text>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei',
    '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  height: 100vh;
}

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 顶部导航栏 */
.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 0 24px;
  z-index: 1000;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  max-width: 1920px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.app-title {
  font-size: 24px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 主体内容 */
.app-main {
  flex: 1;
  overflow: hidden;
  padding: 20px;
}

.el-container {
  height: 100%;
  max-width: 1920px;
  margin: 0 auto;
  gap: 20px;
}

.control-panel {
  width: 450px !important;
  overflow-y: auto;
  overflow-x: hidden;
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.results-panel {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 24px;
  overflow-y: auto;
  box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.1);
}

/* 底部状态栏 */
.app-footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 -2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 0 24px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 48px;
  max-width: 1920px;
  margin: 0 auto;
}

.footer-left,
.footer-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 滚动条样式 */
.control-panel::-webkit-scrollbar,
.results-panel::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.control-panel::-webkit-scrollbar-track,
.results-panel::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
}

.control-panel::-webkit-scrollbar-thumb,
.results-panel::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.control-panel::-webkit-scrollbar-thumb:hover,
.results-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .el-container {
    flex-direction: column;
  }

  .control-panel {
    width: 100% !important;
    max-height: 50vh;
  }

  .results-panel {
    flex: 1;
  }
}
</style>
