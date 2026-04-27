import { formatNumber } from '../utils/formatters'

function CounterfactualResult({ result }) {
  if (!result) return null

  return (
    <section className="card">
      <h3 className="mb-2 text-lg font-semibold">Counterfactual Fairness</h3>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-lg bg-slate-50 p-4">
          <p className="text-sm text-slate-500">Fairness Score</p>
          <p className="text-2xl font-bold text-slate-800">{formatNumber(result.fairness_score, 2)}%</p>
        </div>
        <div className="rounded-lg bg-slate-50 p-4">
          <p className="text-sm text-slate-500">Flip Rate</p>
          <p className="text-2xl font-bold text-slate-800">{formatNumber(result.flip_rate, 2)}%</p>
        </div>
        <div className="rounded-lg bg-slate-50 p-4">
          <p className="text-sm text-slate-500">Risk</p>
          <p className="text-lg font-bold text-slate-800">{result.risk_label}</p>
        </div>
      </div>
      <p className="mt-3 text-sm text-slate-600">
        {formatNumber(result.flip_rate, 2)}% of predictions changed when protected attributes were flipped.
      </p>
    </section>
  )
}

export default CounterfactualResult
