import { severityClasses } from '../utils/formatters'

function ExplainCard({ explain }) {
  if (!explain) return null

  return (
    <section className="card space-y-4">
      <div className={`rounded-lg px-4 py-3 ${severityClasses[explain.severity] || 'bg-slate-100 text-slate-700'}`}>
        Severity: {explain.severity}
      </div>
      <div>
        <h3 className="text-lg font-semibold">Summary</h3>
        <p className="text-slate-700">{explain.summary}</p>
      </div>
      <div>
        <h4 className="font-semibold">Issues</h4>
        <ul className="mt-2 space-y-2">
          {explain.issues.map((issue, idx) => (
            <li key={idx} className="rounded border border-border p-3 text-sm">
              <p className="font-semibold">{issue.title}</p>
              <p>{issue.description}</p>
              <p className="text-slate-500">Metric: {issue.metric}</p>
            </li>
          ))}
        </ul>
      </div>
      <div>
        <h4 className="font-semibold">Recommendations</h4>
        <ul className="mt-2 space-y-2">
          {explain.recommendations.map((item, idx) => (
            <li key={idx} className="rounded border border-border p-3 text-sm">
              <div className="mb-2 flex items-center justify-between">
                <p className="font-semibold">{item.title}</p>
                <span className="badge bg-blue-100 text-blue-700">{item.priority}</span>
              </div>
              <p>{item.description}</p>
              <pre className="mt-2 overflow-x-auto rounded bg-slate-900 p-3 text-xs text-slate-100">{item.code}</pre>
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}

export default ExplainCard
