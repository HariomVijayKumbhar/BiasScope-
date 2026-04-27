import { formatNumber } from '../utils/formatters'

function MetricCard({ metric }) {
  return (
    <article className="card">
      <div className="mb-2 flex items-center justify-between">
        <h4 className="font-semibold text-slate-800">{metric.name}</h4>
        <span className={`badge ${metric.passed ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {metric.passed ? 'PASS' : 'FAIL'}
        </span>
      </div>
      <p className="text-2xl font-bold text-slate-800">{formatNumber(metric.value)}</p>
      <p className="mt-2 text-sm text-slate-500">Threshold: {metric.threshold}</p>
      <p className="mt-2 text-sm text-slate-600">{metric.description}</p>
      <p className="mt-1 text-sm text-slate-700">{metric.interpretation}</p>
    </article>
  )
}

export default MetricCard
