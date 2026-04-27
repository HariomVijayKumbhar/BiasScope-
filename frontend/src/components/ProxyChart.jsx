import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { formatNumber } from '../utils/formatters'

const barColor = {
  High: '#EF4444',
  Moderate: '#F59E0B',
  Low: '#22C55E',
}

function ProxyChart({ result }) {
  if (!result?.proxy_features?.length) return null

  return (
    <section className="card">
      <h3 className="mb-3 text-lg font-semibold">Proxy Bias Detection</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={result.proxy_features} layout="vertical" margin={{ left: 20, right: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" domain={[0, 1]} />
            <YAxis type="category" dataKey="feature" width={150} />
            <Tooltip formatter={(value, _, props) => `${formatNumber(value, 2)} with ${props?.payload?.correlated_attribute}`} />
            <Bar dataKey="correlation" fill="#3B82F6">
              {result.proxy_features.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={barColor[entry.risk_level] || '#3B82F6'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <ul className="mt-4 space-y-2 text-sm text-slate-700">
        {result.proxy_features.slice(0, 5).map((item) => (
          <li key={item.feature}>
            {item.feature}: {formatNumber(item.correlation, 2)} ({item.risk_level} risk)
          </li>
        ))}
      </ul>
    </section>
  )
}

export default ProxyChart
