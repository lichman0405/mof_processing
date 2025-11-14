/**
 * 后端API类型定义
 */

// API响应基础结构
export interface ApiResponse<T = any> {
  success: boolean
  data: T
  message: string
  timestamp: string
  error?: ApiError
}

// API错误
export interface ApiError {
  code: string
  step?: string
  message: string
  details?: string
}

// 处理结果数据
export interface ProcessingData {
  job_id: string
  original_file: string
  processing_time: number
  steps: ProcessingSteps
  output_files: OutputFiles
}

// 各步骤结果
export interface ProcessingSteps {
  step1_check?: StepResult
  step2_desolvate?: StepResult
  step3_find_sites?: StepResult
  step4_supercell?: StepResult
}

// 单个步骤结果
export interface StepResult {
  success: boolean
  data: any
  logs: string[]
  error?: string
}

// 步骤1: 结构检查
export interface CheckData {
  atom_count: number
  composition: Record<string, number>
  cell_params: {
    a: number
    b: number
    c: number
    alpha: number
    beta: number
    gamma: number
    volume: number
  }
}

// 步骤2: 去溶剂
export interface DesolvateData {
  framework_atom_count: number
  removed_atoms: number
  framework_composition: Record<string, number>
}

// 步骤3: 位点识别
export interface SiteData {
  site_type: string
  site_count: number
  sites: Site[]
}

export interface Site {
  index: number
  framework_index: number
  position: [number, number, number]
  element: string
}

// 步骤4: 超胞构建
export interface SupercellData {
  repeat: [number, number, number]
  original_atoms: number
  supercell_atoms: number
  cell_params: {
    a: number
    b: number
    c: number
    alpha: number
    beta: number
    gamma: number
    volume: number
  }
}

// 输出文件
export interface OutputFiles {
  desolvated?: FileInfo
  supercell?: FileInfo
}

export interface FileInfo {
  file_id: string
  download_url: string
}

// 处理参数
export interface ProcessingParams {
  file: File
  supercell_repeat: [number, number, number]
  site_type: string
  mult_factor: number
}

// 健康检查响应
export interface HealthResponse {
  status: string
  service: string
}

// API信息响应
export interface ApiInfo {
  name: string
  version: string
  description: string
  endpoints: Record<string, string>
}
