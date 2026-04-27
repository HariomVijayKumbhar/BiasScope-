import MetricCard from '../components/MetricCard'
import CounterfactualResult from '../components/CounterfactualResult'
import ProxyChart from '../components/ProxyChart'
import ExplainCard from '../components/ExplainCard'
import ChatPanel from '../components/ChatPanel'

function AuditPage({ uploadState, auditState }) {
  const auditContext = {
    dataset_name: uploadState.fileMeta?.name,
    domain: uploadState.detectResult?.domain,
    protected_attribute: uploadState.detectResult?.protected_attributes?.[0],
    bias_results: auditState.biasResult,
    counterfactual_score: auditState.counterfactualResult,
    proxy_features: auditState.proxyResult,
    explanation_summary: auditState.explainResult?.summary,
    severity: auditState.explainResult?.severity,
  }

  return (
    <section className="space-y-4">
      {auditState.error && <div className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{auditState.error}</div>}
      {auditState.loading && <div className="card">Running bias audit engines...</div>}

      {auditState.biasResult && (
        <div className={`card ${auditState.biasResult.overall_passed ? 'bg-green-50' : 'bg-red-50'}`}>
          <h2 className="text-xl font-bold">
            {auditState.biasResult.overall_passed ? 'No Significant Bias Detected' : 'Bias Detected - Action Required'}
          </h2>
        </div>
      )}

      {auditState.biasResult?.metrics && (
        <div className="grid gap-4 lg:grid-cols-3">
          {auditState.biasResult.metrics.map((metric) => (
            <MetricCard key={metric.name} metric={metric} />
          ))}
        </div>
      )}

      <CounterfactualResult result={auditState.counterfactualResult} />
      <ProxyChart result={auditState.proxyResult} />
      <ExplainCard explain={auditState.explainResult} />

      <ChatPanel auditContext={auditContext} />
    </section>
  )
}

export default AuditPage
