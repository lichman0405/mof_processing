<template>
  <div class="results-container">
    <el-alert
      v-if="error"
      type="error"
      :title="error"
      :closable="false"
      show-icon
      style="margin-bottom: 20px"
    />

    <el-empty v-if="!hasResult && !error" description="暂无处理结果" />

    <div v-if="hasResult" class="results-content">
      <!-- 概览信息 -->
      <el-card shadow="hover" class="result-card">
        <template #header>
          <div class="card-header">
            <el-icon :size="20"><DocumentChecked /></el-icon>
            <span>处理概览</span>
            <el-tag :type="isSuccess ? 'success' : 'danger'" style="margin-left: auto">
              {{ isSuccess ? '成功' : '失败' }}
            </el-tag>
          </div>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="作业ID">
            <el-text type="info" style="font-family: monospace">{{ jobId }}</el-text>
          </el-descriptions-item>
          <el-descriptions-item label="处理时间">
            {{ processingTime.toFixed(2) }} 秒
          </el-descriptions-item>
          <el-descriptions-item label="原始文件">
            {{ result?.data.original_file }}
          </el-descriptions-item>
          <el-descriptions-item label="时间戳">
            {{ formatTimestamp(result?.timestamp) }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 步骤1: 结构检查 -->
      <el-card v-if="steps.step1_check" shadow="hover" class="result-card">
        <template #header>
          <div class="card-header">
            <el-icon :size="20"><MagicStick /></el-icon>
            <span>步骤1: 结构检查</span>
            <el-tag
              type="success"
              size="small"
              style="margin-left: auto"
            >
              完成
            </el-tag>
          </div>
        </template>
        
        <div v-if="steps.step1_check.data" class="step-content">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="原子总数">
              {{ steps.step1_check.data.atom_count }}
            </el-descriptions-item>
            <el-descriptions-item label="化学组成">
              <el-space wrap>
                <el-tag
                  v-for="(count, element) in steps.step1_check.data.composition"
                  :key="element"
                  size="small"
                >
                  {{ element }}<sub>{{ count }}</sub>
                </el-tag>
              </el-space>
            </el-descriptions-item>
          </el-descriptions>

          <el-divider content-position="left">晶格参数</el-divider>
          <el-table
            :data="formatCellParams(steps.step1_check.data.cell_params)"
            stripe
            border
            size="small"
          >
            <el-table-column prop="param" label="参数" width="100" />
            <el-table-column prop="value" label="数值" />
            <el-table-column prop="unit" label="单位" width="100" />
          </el-table>

          <!-- 调试信息 -->
          <el-alert v-if="!steps.step1_check.logs || steps.step1_check.logs.length === 0" 
            type="warning" 
            :closable="false"
            style="margin-top: 16px">
            后端返回的日志数据为空
          </el-alert>

          <LogViewer 
            v-if="steps.step1_check.logs && steps.step1_check.logs.length > 0"
            :logs="steps.step1_check.logs" 
            title="步骤1 详细日志" 
          />
        </div>
      </el-card>

      <!-- 步骤2: 去溶剂 -->
      <el-card v-if="steps.step2_desolvate" shadow="hover" class="result-card">
        <template #header>
          <div class="card-header">
            <el-icon :size="20"><Filter /></el-icon>
            <span>步骤2: 去除溶剂</span>
            <el-tag
              type="success"
              size="small"
              style="margin-left: auto"
            >
              完成
            </el-tag>
          </div>
        </template>

        <div v-if="steps.step2_desolvate.data" class="step-content">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="框架原子数">
              <el-text type="success" :size="'large'">
                {{ steps.step2_desolvate.data.framework_atom_count }}
              </el-text>
            </el-descriptions-item>
            <el-descriptions-item label="移除原子数">
              <el-text type="warning" :size="'large'">
                {{ steps.step2_desolvate.data.removed_atoms }}
              </el-text>
            </el-descriptions-item>
            <el-descriptions-item label="框架组成" :span="2">
              <el-space wrap>
                <el-tag
                  v-for="(count, element) in steps.step2_desolvate.data.framework_composition"
                  :key="element"
                  type="success"
                  size="small"
                >
                  {{ element }}<sub>{{ count }}</sub>
                </el-tag>
              </el-space>
            </el-descriptions-item>
          </el-descriptions>

          <!-- 调试信息 -->
          <el-alert v-if="!steps.step2_desolvate.logs || steps.step2_desolvate.logs.length === 0" 
            type="warning" 
            :closable="false"
            style="margin-top: 16px">
            后端返回的日志数据为空
          </el-alert>

          <LogViewer 
            v-if="steps.step2_desolvate.logs && steps.step2_desolvate.logs.length > 0"
            :logs="steps.step2_desolvate.logs" 
            title="步骤2 详细日志" 
          />
        </div>
      </el-card>

      <!-- 步骤3: 识别位点 -->
      <el-card v-if="steps.step3_find_sites" shadow="hover" class="result-card">
        <template #header>
          <div class="card-header">
            <el-icon :size="20"><Location /></el-icon>
            <span>步骤3: 识别位点</span>
            <el-tag
              type="success"
              size="small"
              style="margin-left: auto"
            >
              完成
            </el-tag>
          </div>
        </template>

        <div v-if="steps.step3_find_sites.data" class="step-content">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="位点类型">
              <el-tag type="primary">{{ steps.step3_find_sites.data.site_type }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="位点数量">
              <el-text type="success" :size="'large'">
                {{ steps.step3_find_sites.data.site_count }}
              </el-text>
            </el-descriptions-item>
          </el-descriptions>

          <el-divider content-position="left">位点坐标</el-divider>
          <el-table
            :data="steps.step3_find_sites.data.sites"
            stripe
            border
            size="small"
            max-height="300"
          >
            <el-table-column prop="index" label="原始索引" width="100" />
            <el-table-column prop="framework_index" label="框架索引" width="100" />
            <el-table-column prop="element" label="元素" width="80" />
            <el-table-column label="坐标 (x, y, z)">
              <template #default="{ row }">
                {{ row.position.map((v: number) => v.toFixed(4)).join(', ') }}
              </template>
            </el-table-column>
          </el-table>

          <!-- 调试信息 -->
          <el-alert v-if="!steps.step3_find_sites.logs || steps.step3_find_sites.logs.length === 0" 
            type="warning" 
            :closable="false"
            style="margin-top: 16px">
            后端返回的日志数据为空
          </el-alert>

          <LogViewer 
            v-if="steps.step3_find_sites.logs && steps.step3_find_sites.logs.length > 0"
            :logs="steps.step3_find_sites.logs" 
            title="步骤3 详细日志" 
          />
        </div>
      </el-card>

      <!-- 步骤4: 构建超胞 -->
      <el-card v-if="steps.step4_supercell" shadow="hover" class="result-card">
        <template #header>
          <div class="card-header">
            <el-icon :size="20"><Grid /></el-icon>
            <span>步骤4: 构建超胞</span>
            <el-tag
              type="success"
              size="small"
              style="margin-left: auto"
            >
              完成
            </el-tag>
          </div>
        </template>

        <div v-if="steps.step4_supercell.data" class="step-content">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="重复倍数">
              <el-tag>{{ steps.step4_supercell.data.repeat.join(' × ') }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="原子数">
              {{ steps.step4_supercell.data.original_atoms }} →
              <el-text type="success">{{ steps.step4_supercell.data.supercell_atoms }}</el-text>
            </el-descriptions-item>
          </el-descriptions>

          <el-divider content-position="left">超胞晶格参数</el-divider>
          <el-table
            :data="formatCellParams(steps.step4_supercell.data.cell_params)"
            stripe
            border
            size="small"
          >
            <el-table-column prop="param" label="参数" width="100" />
            <el-table-column prop="value" label="数值" />
            <el-table-column prop="unit" label="单位" width="100" />
          </el-table>

          <!-- 调试信息 -->
          <el-alert v-if="!steps.step4_supercell.logs || steps.step4_supercell.logs.length === 0" 
            type="warning" 
            :closable="false"
            style="margin-top: 16px">
            后端返回的日志数据为空
          </el-alert>

          <LogViewer 
            v-if="steps.step4_supercell.logs && steps.step4_supercell.logs.length > 0"
            :logs="steps.step4_supercell.logs" 
            title="步骤4 详细日志" 
          />
        </div>
      </el-card>

      <!-- 文件下载 -->
      <el-card v-if="Object.keys(outputFiles).length > 0" shadow="hover" class="result-card">
        <template #header>
          <div class="card-header">
            <el-icon :size="20"><Download /></el-icon>
            <span>输出文件</span>
          </div>
        </template>

        <el-space direction="vertical" :size="12" style="width: 100%">
          <el-button
            v-if="outputFiles.desolvated"
            type="success"
            :icon="Download"
            @click="handleDownload(outputFiles.desolvated.file_id, 'desolvated')"
            style="width: 100%"
          >
            下载去溶剂结构文件
          </el-button>

          <el-button
            v-if="outputFiles.supercell"
            type="primary"
            :icon="Download"
            @click="handleDownload(outputFiles.supercell.file_id, 'supercell')"
            style="width: 100%"
          >
            下载超胞结构文件
          </el-button>
        </el-space>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  DocumentChecked,
  MagicStick,
  Filter,
  Location,
  Grid,
  Download
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useMofStore } from '@/stores/mof'
import LogViewer from './LogViewer.vue'

const mofStore = useMofStore()

const hasResult = computed(() => mofStore.hasResult)
const isSuccess = computed(() => mofStore.isSuccess)
const error = computed(() => mofStore.error)
const result = computed(() => mofStore.result)
const jobId = computed(() => mofStore.jobId)
const processingTime = computed(() => mofStore.processingTime)
const steps = computed(() => mofStore.steps)
const outputFiles = computed(() => mofStore.outputFiles)

const formatTimestamp = (timestamp?: string) => {
  if (!timestamp) return '-'
  return new Date(timestamp).toLocaleString('zh-CN')
}

const formatCellParams = (params: any) => {
  if (!params) return []
  return [
    { param: 'a', value: params.a.toFixed(4), unit: 'Å' },
    { param: 'b', value: params.b.toFixed(4), unit: 'Å' },
    { param: 'c', value: params.c.toFixed(4), unit: 'Å' },
    { param: 'α', value: params.alpha.toFixed(2), unit: '°' },
    { param: 'β', value: params.beta.toFixed(2), unit: '°' },
    { param: 'γ', value: params.gamma.toFixed(2), unit: '°' },
    { param: 'V', value: params.volume.toFixed(2), unit: 'Å³' }
  ]
}

const handleDownload = async (fileId: string, type: string) => {
  try {
    const filename = `${type}_${jobId.value.substring(0, 8)}.cif`
    await mofStore.downloadFile(fileId, filename)
    ElMessage.success('文件下载成功')
  } catch (error: any) {
    ElMessage.error('下载失败: ' + (error.message || '未知错误'))
  }
}
</script>

<style scoped>
.results-container {
  width: 100%;
}

.results-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-card {
  transition: all 0.3s;
}

.result-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
}

.step-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

:deep(.el-descriptions__label) {
  font-weight: 600;
}

:deep(sub) {
  font-size: 0.8em;
}
</style>
