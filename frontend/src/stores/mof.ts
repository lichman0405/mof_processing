/**
 * Pinia Store - MOF处理状态管理
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type {
  ProcessingParams,
  ApiResponse,
  ProcessingData,
  ProcessingSteps
} from '@/types'
import { apiService } from '@/services/api'

export const useMofStore = defineStore('mof', () => {
  // 状态
  const isProcessing = ref(false)
  const currentStep = ref(0) // 0-4: 未开始、步骤1-4
  const uploadProgress = ref(0)
  const result = ref<ApiResponse<ProcessingData> | null>(null)
  const error = ref<string | null>(null)

  // 参数状态
  const params = ref<Omit<ProcessingParams, 'file'>>({
    supercell_repeat: [2, 2, 2],
    site_type: 'NH2',
    mult_factor: 1.2
  })

  // 上传的文件
  const uploadedFile = ref<File | null>(null)

  // API连接状态
  const isApiHealthy = ref(false)

  // 计算属性
  const hasResult = computed(() => result.value !== null)
  const isSuccess = computed(() => result.value?.success || false)
  const processingTime = computed(() => result.value?.data?.processing_time || 0)
  const jobId = computed(() => result.value?.data?.job_id || '')
  const steps = computed<ProcessingSteps>(() => result.value?.data?.steps || {})
  const outputFiles = computed(() => result.value?.data?.output_files || {})

  // 步骤完成状态
  const stepsCompleted = computed(() => {
    const s = steps.value
    return {
      step1: !!s.step1_check,
      step2: !!s.step2_desolvate,
      step3: !!s.step3_find_sites,
      step4: !!s.step4_supercell
    }
  })

  // 进度百分比
  const progressPercent = computed(() => {
    if (!isProcessing.value && !hasResult.value) return 0
    const completed = Object.values(stepsCompleted.value).filter(Boolean).length
    return Math.round((completed / 4) * 100)
  })

  // Actions
  async function checkHealth() {
    try {
      const health = await apiService.healthCheck()
      isApiHealthy.value = health.status === 'healthy'
      return true
    } catch (err) {
      isApiHealthy.value = false
      return false
    }
  }

  async function processFile(file: File) {
    isProcessing.value = true
    currentStep.value = 0
    error.value = null
    result.value = null
    uploadedFile.value = file

    try {
      const processingParams: ProcessingParams = {
        file,
        ...params.value
      }

      // 模拟步骤进度（实际应通过WebSocket或轮询获取）
      const progressInterval = setInterval(() => {
        if (currentStep.value < 4) {
          currentStep.value++
        }
      }, 2000)

      const response = await apiService.processMOF(processingParams)
      
      clearInterval(progressInterval)
      currentStep.value = 4
      
      result.value = response

      if (!response.success) {
        error.value = response.message || '处理失败'
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail?.message || err.message || '处理请求失败'
      console.error('Processing error:', err)
    } finally {
      isProcessing.value = false
    }
  }

  async function downloadFile(fileId: string, filename: string) {
    try {
      const blob = await apiService.downloadFile(fileId)
      apiService.triggerDownload(blob, filename)
    } catch (err: any) {
      error.value = '文件下载失败: ' + (err.message || '未知错误')
      throw err
    }
  }

  function resetState() {
    isProcessing.value = false
    currentStep.value = 0
    uploadProgress.value = 0
    result.value = null
    error.value = null
    uploadedFile.value = null
  }

  function updateParams(newParams: Partial<Omit<ProcessingParams, 'file'>>) {
    params.value = { ...params.value, ...newParams }
  }

  return {
    // State
    isProcessing,
    currentStep,
    uploadProgress,
    result,
    error,
    params,
    uploadedFile,
    isApiHealthy,

    // Computed
    hasResult,
    isSuccess,
    processingTime,
    jobId,
    steps,
    outputFiles,
    stepsCompleted,
    progressPercent,

    // Actions
    checkHealth,
    processFile,
    downloadFile,
    resetState,
    updateParams
  }
})
