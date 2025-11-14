<template>
  <div class="params-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon :size="24"><Setting /></el-icon>
          <span>处理参数</span>
        </div>
      </template>

      <el-form :model="localParams" label-width="120px" label-position="left">
        <el-form-item label="超胞重复">
          <el-space>
            <el-input-number
              v-model="localParams.supercell_repeat[0]"
              :min="1"
              :max="10"
              :disabled="isProcessing"
              @change="updateParams"
            />
            <el-input-number
              v-model="localParams.supercell_repeat[1]"
              :min="1"
              :max="10"
              :disabled="isProcessing"
              @change="updateParams"
            />
            <el-input-number
              v-model="localParams.supercell_repeat[2]"
              :min="1"
              :max="10"
              :disabled="isProcessing"
              @change="updateParams"
            />
          </el-space>
          <div class="form-tip">沿a, b, c轴的重复次数</div>
        </el-form-item>

        <el-form-item label="位点类型">
          <el-input
            v-model="localParams.site_type"
            placeholder="NH2"
            :disabled="isProcessing"
            @change="updateParams"
          />
          <div class="form-tip">要识别的官能团类型</div>
        </el-form-item>

        <el-form-item label="键长因子">
          <el-slider
            v-model="localParams.mult_factor"
            :min="1.0"
            :max="2.0"
            :step="0.1"
            :disabled="isProcessing"
            :show-tooltip="true"
            :format-tooltip="formatFactor"
            @change="updateParams"
          />
          <div class="form-tip">键长判断的放大因子 ({{ localParams.mult_factor }})</div>
        </el-form-item>
      </el-form>

      <el-divider />

      <div class="action-buttons">
        <el-button
          type="primary"
          size="large"
          :icon="Promotion"
          :loading="isProcessing"
          :disabled="!canProcess"
          @click="handleProcess"
          style="width: 100%"
        >
          {{ isProcessing ? '处理中...' : '开始处理' }}
        </el-button>

        <el-button
          v-if="hasResult"
          size="large"
          :icon="RefreshLeft"
          @click="handleReset"
          style="width: 100%; margin-top: 12px"
        >
          重新开始
        </el-button>
      </div>

      <!-- 处理进度 -->
      <div v-if="isProcessing || hasResult" class="progress-section">
        <el-divider />
        <div class="progress-header">
          <span>处理进度</span>
          <el-tag :type="progressTagType">{{ progressPercent }}%</el-tag>
        </div>
        <el-progress
          :percentage="progressPercent"
          :status="progressStatus"
          :stroke-width="12"
        />
        <div class="steps-info">
          <el-steps :active="currentStep" align-center>
            <el-step title="检查结构" :icon="stepsCompleted.step1 ? Check : Loading" />
            <el-step title="去除溶剂" :icon="stepsCompleted.step2 ? Check : Loading" />
            <el-step title="识别位点" :icon="stepsCompleted.step3 ? Check : Loading" />
            <el-step title="构建超胞" :icon="stepsCompleted.step4 ? Check : Loading" />
          </el-steps>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Setting, Promotion, RefreshLeft, Check, Loading } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useMofStore } from '@/stores/mof'

const mofStore = useMofStore()

const localParams = ref({
  supercell_repeat: [...mofStore.params.supercell_repeat] as [number, number, number],
  site_type: mofStore.params.site_type,
  mult_factor: mofStore.params.mult_factor
})

// 同步store的参数变化
watch(
  () => mofStore.params,
  (newParams) => {
    localParams.value = {
      supercell_repeat: [...newParams.supercell_repeat] as [number, number, number],
      site_type: newParams.site_type,
      mult_factor: newParams.mult_factor
    }
  },
  { deep: true }
)

const isProcessing = computed(() => mofStore.isProcessing)
const hasResult = computed(() => mofStore.hasResult)
const currentStep = computed(() => mofStore.currentStep)
const progressPercent = computed(() => mofStore.progressPercent)
const stepsCompleted = computed(() => mofStore.stepsCompleted)

const canProcess = computed(() => {
  return mofStore.uploadedFile !== null && !isProcessing.value
})

const progressTagType = computed(() => {
  if (progressPercent.value === 100) return 'success'
  if (progressPercent.value > 0) return 'warning'
  return 'info'
})

const progressStatus = computed(() => {
  if (mofStore.error) return 'exception'
  if (progressPercent.value === 100) return 'success'
  return undefined
})

const updateParams = () => {
  mofStore.updateParams(localParams.value)
}

const formatFactor = (val: number) => {
  return val.toFixed(1)
}

const handleProcess = async () => {
  if (!mofStore.uploadedFile) {
    ElMessage.warning('请先上传CIF文件')
    return
  }

  try {
    await mofStore.processFile(mofStore.uploadedFile)
    
    if (mofStore.isSuccess) {
      ElMessage.success('处理完成！')
    } else {
      ElMessage.error(mofStore.error || '处理失败')
    }
  } catch (error: any) {
    ElMessage.error('处理失败: ' + (error.message || '未知错误'))
  }
}

const handleReset = async () => {
  try {
    await ElMessageBox.confirm('确定要重新开始吗？当前结果将被清除。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    mofStore.resetState()
    ElMessage.success('已重置')
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.params-container {
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

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.action-buttons {
  margin-top: 20px;
}

.progress-section {
  margin-top: 20px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-weight: 600;
}

.steps-info {
  margin-top: 24px;
}

:deep(.el-step__title) {
  font-size: 12px;
}
</style>
