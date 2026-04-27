import { useState } from 'react'
import { detectColumns, uploadCsv } from '../services/api'

export function useUpload() {
  const [loading, setLoading] = useState(false)
  const [detectLoading, setDetectLoading] = useState(false)
  const [error, setError] = useState('')
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadResult, setUploadResult] = useState(null)
  const [fullDataset, setFullDataset] = useState([])
  const [detectResult, setDetectResult] = useState(null)
  const [fileMeta, setFileMeta] = useState(null)
  const [confirmedDetection, setConfirmedDetection] = useState(false)

  const handleUpload = async (file) => {
    setLoading(true)
    setError('')
    setUploadProgress(0)
    setConfirmedDetection(false)

    try {
      const result = await uploadCsv(file, (progressEvent) => {
        const total = progressEvent.total || file.size
        setUploadProgress(Math.round((progressEvent.loaded * 100) / total))
      })

      setUploadResult(result)
      setFullDataset(result.dataset || result.preview)
      setFileMeta({ name: file.name, size: file.size })

      setDetectLoading(true)
      const detection = await detectColumns(result.columns, result.preview)
      setDetectResult(detection)
    } catch (apiError) {
      setError(apiError?.response?.data?.error || apiError.message || 'Upload failed')
    } finally {
      setDetectLoading(false)
      setLoading(false)
    }
  }

  const confirmDetection = (payload) => {
    setDetectResult(payload)
    setConfirmedDetection(true)
  }

  const reset = () => {
    setLoading(false)
    setDetectLoading(false)
    setError('')
    setUploadProgress(0)
    setUploadResult(null)
    setFullDataset([])
    setDetectResult(null)
    setFileMeta(null)
    setConfirmedDetection(false)
  }

  return {
    loading,
    detectLoading,
    error,
    uploadProgress,
    uploadResult,
    fullDataset,
    detectResult,
    fileMeta,
    confirmedDetection,
    handleUpload,
    confirmDetection,
    reset,
  }
}
