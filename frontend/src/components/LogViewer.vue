<template>
  <div class="log-viewer">
    <div class="log-header" @click="toggleLogs">
      <div class="header-left">
        <el-icon :class="['expand-icon', { expanded: isExpanded }]">
          <ArrowRight />
        </el-icon>
        <el-icon class="log-icon"><Document /></el-icon>
        <span class="log-title">{{ title }}</span>
        <el-tag size="small" type="info" style="margin-left: 8px">
          {{ logs.length }} 条
        </el-tag>
      </div>
    </div>
    
    <el-collapse-transition>
      <div v-show="isExpanded" class="log-content-wrapper">
        <div class="log-content">
          <div v-if="logs.length === 0" class="empty-logs">
            <el-icon :size="48" color="#909399"><DocumentDelete /></el-icon>
            <el-text type="info" style="margin-top: 12px">暂无日志</el-text>
          </div>
          <div v-else class="log-lines">
            <div 
              v-for="(log, index) in logs" 
              :key="index" 
              class="log-line"
              :class="getLogClass(log)"
            >
              <span class="log-index">{{ String(index + 1).padStart(3, '0') }}</span>
              <el-icon class="log-type-icon">
                <component :is="getLogIcon(log)" />
              </el-icon>
              <span class="log-text">{{ log }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-collapse-transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { 
  ArrowRight, 
  Document, 
  DocumentDelete,
  SuccessFilled,
  WarningFilled,
  CircleCloseFilled,
  InfoFilled
} from '@element-plus/icons-vue'

interface Props {
  logs: string[]
  title?: string
}

withDefaults(defineProps<Props>(), {
  title: '详细日志'
})

const isExpanded = ref(true)  // 默认展开日志

const toggleLogs = () => {
  isExpanded.value = !isExpanded.value
}

const getLogClass = (log: string): string => {
  const lowerLog = log.toLowerCase()
  if (lowerLog.includes('error') || lowerLog.includes('失败') || lowerLog.includes('错误')) {
    return 'log-error'
  }
  if (lowerLog.includes('warning') || lowerLog.includes('警告')) {
    return 'log-warning'
  }
  if (lowerLog.includes('success') || lowerLog.includes('成功') || lowerLog.includes('完成')) {
    return 'log-success'
  }
  return 'log-normal'
}

const getLogIcon = (log: string) => {
  const lowerLog = log.toLowerCase()
  if (lowerLog.includes('error') || lowerLog.includes('失败') || lowerLog.includes('错误')) {
    return CircleCloseFilled
  }
  if (lowerLog.includes('warning') || lowerLog.includes('警告')) {
    return WarningFilled
  }
  if (lowerLog.includes('success') || lowerLog.includes('成功') || lowerLog.includes('完成')) {
    return SuccessFilled
  }
  return InfoFilled
}
</script>

<style scoped>
.log-viewer {
  margin-top: 16px;
  border-radius: 8px;
  overflow: hidden;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.log-viewer:hover {
  border-color: rgba(102, 126, 234, 0.3);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.log-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  cursor: pointer;
  user-select: none;
  transition: all 0.3s ease;
}

.log-header:hover {
  background: rgba(102, 126, 234, 0.08);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.expand-icon {
  transition: transform 0.3s ease;
  color: #667eea;
  font-size: 16px;
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.log-icon {
  color: #667eea;
  font-size: 18px;
}

.log-title {
  font-weight: 500;
  color: #303133;
  font-size: 14px;
}

.log-content-wrapper {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.log-content {
  background: linear-gradient(to bottom, #1e1e2e, #181825);
  padding: 16px;
  max-height: 400px;
  overflow-y: auto;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
}

.empty-logs {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #909399;
}

.log-lines {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.log-line {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.log-line::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: transparent;
  transition: all 0.2s ease;
}

.log-line:hover {
  background: rgba(255, 255, 255, 0.05);
}

.log-line.log-error::before {
  background: #f56c6c;
}

.log-line.log-warning::before {
  background: #e6a23c;
}

.log-line.log-success::before {
  background: #67c23a;
}

.log-line.log-normal::before {
  background: #409eff;
}

.log-index {
  color: #6272a4;
  min-width: 36px;
  text-align: right;
  user-select: none;
  flex-shrink: 0;
  font-weight: 500;
  opacity: 0.6;
}

.log-type-icon {
  flex-shrink: 0;
  margin-top: 2px;
  font-size: 14px;
}

.log-error .log-type-icon {
  color: #f56c6c;
}

.log-warning .log-type-icon {
  color: #e6a23c;
}

.log-success .log-type-icon {
  color: #67c23a;
}

.log-normal .log-type-icon {
  color: #409eff;
}

.log-text {
  flex: 1;
  word-break: break-word;
  line-height: 1.6;
}

.log-error .log-text {
  color: #ff7b7b;
}

.log-warning .log-text {
  color: #f4bd5c;
}

.log-success .log-text {
  color: #85d96e;
}

.log-normal .log-text {
  color: #b4c7dc;
}

.log-content::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

.log-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 5px;
}

.log-content::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #667eea, #764ba2);
  border-radius: 5px;
  transition: all 0.3s ease;
}

.log-content::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #7c8eeb, #8b5fc4);
}
</style>
