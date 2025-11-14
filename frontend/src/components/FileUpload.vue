<template>
  <div class="upload-container">
    <el-card shadow="hover" :body-style="{ padding: '40px' }">
      <template #header>
        <div class="card-header">
          <el-icon :size="24"><Upload /></el-icon>
          <span>上传CIF文件</span>
        </div>
      </template>

      <el-upload
        ref="uploadRef"
        class="upload-dragger"
        drag
        :auto-upload="false"
        :show-file-list="true"
        :limit="1"
        accept=".cif,.CIF"
        :on-change="handleFileChange"
        :on-remove="handleFileRemove"
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          拖拽CIF文件到此处，或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">支持 .cif 格式，文件大小不超过 50MB</div>
        </template>
      </el-upload>

      <div v-if="uploadedFile" class="file-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="文件名">
            {{ uploadedFile.name }}
          </el-descriptions-item>
          <el-descriptions-item label="大小">
            {{ formatFileSize(uploadedFile.size) }}
          </el-descriptions-item>
          <el-descriptions-item label="类型">
            {{ uploadedFile.type || 'chemical/x-cif' }}
          </el-descriptions-item>
          <el-descriptions-item label="最后修改">
            {{ formatDate(uploadedFile.lastModified) }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Upload, UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { UploadFile, UploadInstance } from 'element-plus'
import { useMofStore } from '@/stores/mof'

const mofStore = useMofStore()
const uploadRef = ref<UploadInstance>()

const uploadedFile = computed(() => mofStore.uploadedFile)

const handleFileChange = (file: UploadFile) => {
  // 验证文件类型
  const validExtensions = ['.cif', '.CIF']
  const fileName = file.name
  const isValidType = validExtensions.some((ext) => fileName.endsWith(ext))

  if (!isValidType) {
    ElMessage.error('只支持 .cif 格式的文件')
    uploadRef.value?.clearFiles()
    return
  }

  // 验证文件大小 (50MB)
  const maxSize = 50 * 1024 * 1024
  if (file.size && file.size > maxSize) {
    ElMessage.error('文件大小不能超过 50MB')
    uploadRef.value?.clearFiles()
    return
  }

  // 保存文件到store
  if (file.raw) {
    mofStore.uploadedFile = file.raw
    ElMessage.success('文件上传成功')
  }
}

const handleFileRemove = () => {
  mofStore.uploadedFile = null
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (timestamp: number): string => {
  return new Date(timestamp).toLocaleString('zh-CN')
}
</script>

<style scoped>
.upload-container {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: #409eff;
}

.upload-dragger {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
  padding: 40px;
}

.el-icon--upload {
  font-size: 67px;
  color: #409eff;
  margin-bottom: 16px;
}

.file-info {
  margin-top: 24px;
}
</style>
