import { useState } from 'react'
import { getReport, runBias, runCounterfactual, runExplain, runProxy } from '../services/api'

export function useBiasAudit() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [biasResult, setBiasResult] = useState(null)
  const [counterfactualResult, setCounterfactualResult] = useState(null)
  const [proxyResult, setProxyResult] = useState(null)
  const [explainResult, setExplainResult] = useState(null)

  const runAudit = async ({ sessionId, dataset, target, protectedAttrs, domain }) => {
    setLoading(true)
    setError('')
    try {
      const commonPayload = { session_id: sessionId, dataset, target, protected_attrs: protectedAttrs }
      const bias = await runBias(commonPayload)
      const counterfactual = await runCounterfactual(commonPayload)
      const proxy = await runProxy({ session_id: sessionId, dataset, protected_attrs: protectedAttrs })
      const explain = await runExplain({
        session_id: sessionId,
        bias_results: bias,
        counterfactual_results: counterfactual,
        proxy_results: proxy,
        domain,
        protected_attribute: protectedAttrs[0] || '',
      })

      setBiasResult(bias)
      setCounterfactualResult(counterfactual)
      setProxyResult(proxy)
      setExplainResult(explain)
      return { bias, counterfactual, proxy, explain }
    } catch (apiError) {
      const message = apiError?.response?.data?.error || apiError.message || 'Audit failed'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }

  const downloadReport = async (sessionId) => {
    if (!sessionId) {
      throw new Error('No active session found.')
    }
    const blob = await getReport(sessionId)
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `biasscope-report-${sessionId}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const reset = () => {
    setLoading(false)
    setError('')
    setBiasResult(null)
    setCounterfactualResult(null)
    setProxyResult(null)
    setExplainResult(null)
  }

  return {
    loading,
    error,
    biasResult,
    counterfactualResult,
    proxyResult,
    explainResult,
    runAudit,
    downloadReport,
    reset,
  }
}
