import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 120000,
})

export const getHealth = async () => {
  const { data } = await api.get('/health')
  return data.data
}

export const uploadCsv = async (file, onUploadProgress) => {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress,
  })
  return data.data
}

export const detectColumns = async (columns, sampleRows) => {
  const { data } = await api.post('/detect', { columns, sample_rows: sampleRows })
  return data.data
}

export const runBias = async (payload) => {
  const { data } = await api.post('/bias', payload)
  return data.data
}

export const runCounterfactual = async (payload) => {
  const { data } = await api.post('/counterfactual', payload)
  return data.data
}

export const runProxy = async (payload) => {
  const { data } = await api.post('/proxy', payload)
  return data.data
}

export const runExplain = async (payload) => {
  const { data } = await api.post('/explain', payload)
  return data.data
}

export const getReport = async (sessionId) => {
  const response = await api.get(`/report?session_id=${encodeURIComponent(sessionId)}`, {
    responseType: 'blob',
  })
  return response.data
}

export const sendChat = async (payload) => {
  const { data } = await api.post('/chat', payload)
  return data.data
}

export default api
