/**
 * API服务 - 封装所有后端接口调用
 */
import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import type {
  ApiResponse,
  ProcessingData,
  ProcessingParams,
  HealthResponse,
  ApiInfo
} from '@/types'

class ApiService {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
      timeout: 300000, // 5分钟超时
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // 响应拦截器
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error)
        return Promise.reject(error)
      }
    )
  }

  /**
   * 获取API信息
   */
  async getApiInfo(): Promise<ApiInfo> {
    const response: AxiosResponse<ApiInfo> = await this.client.get('/')
    return response.data
  }

  /**
   * 健康检查
   */
  async healthCheck(): Promise<HealthResponse> {
    const response: AxiosResponse<HealthResponse> = await this.client.get('/api/health')
    return response.data
  }

  /**
   * 处理MOF文件 - 核心接口
   */
  async processMOF(params: ProcessingParams): Promise<ApiResponse<ProcessingData>> {
    const formData = new FormData()
    formData.append('file', params.file)
    formData.append('supercell_repeat', JSON.stringify(params.supercell_repeat))
    formData.append('site_type', params.site_type)
    formData.append('mult_factor', params.mult_factor.toString())

    const response: AxiosResponse<ApiResponse<ProcessingData>> = await this.client.post(
      '/api/process',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            console.log('Upload progress:', percentCompleted + '%')
          }
        }
      }
    )

    return response.data
  }

  /**
   * 下载文件
   */
  async downloadFile(fileId: string): Promise<Blob> {
    const response: AxiosResponse<Blob> = await this.client.get(`/api/download/${fileId}`, {
      responseType: 'blob'
    })
    return response.data
  }

  /**
   * 触发下载
   */
  triggerDownload(blob: Blob, filename: string) {
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  }
}

export const apiService = new ApiService()
