import { useMemo, useState } from 'react'

function DetectionResult({ columns = [], detectResult, loading, onConfirm }) {
  const [targetVariable, setTargetVariable] = useState(detectResult?.target_variable || '')
  const [protectedAttributes, setProtectedAttributes] = useState(detectResult?.protected_attributes || [])
  const [domain, setDomain] = useState(detectResult?.domain || 'other')

  const confidenceColor = useMemo(() => {
    if (detectResult?.confidence === 'high') return 'bg-green-100 text-green-700'
    if (detectResult?.confidence === 'medium') return 'bg-yellow-100 text-yellow-700'
    return 'bg-red-100 text-red-700'
  }, [detectResult])

  if (loading) {
    return <div className="card">BiasScope is analyzing your dataset...</div>
  }

  if (!detectResult) {
    return null
  }

  const toggleAttr = (attr) => {
    setProtectedAttributes((prev) =>
      prev.includes(attr) ? prev.filter((item) => item !== attr) : [...prev, attr],
    )
  }

  return (
    <section className="card space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">AI Column Detection</h3>
        <span className={`badge ${confidenceColor}`}>{detectResult.confidence}</span>
      </div>
      <p className="italic text-slate-500">{detectResult.reasoning}</p>
      <div className="grid gap-4 md:grid-cols-2">
        <label className="text-sm">
          <span className="mb-1 block font-semibold text-slate-700">Target Variable</span>
          <select className="w-full rounded border border-border p-2" value={targetVariable} onChange={(e) => setTargetVariable(e.target.value)}>
            {columns.map((col) => (
              <option key={col} value={col}>{col}</option>
            ))}
          </select>
        </label>
        <label className="text-sm">
          <span className="mb-1 block font-semibold text-slate-700">Domain</span>
          <select className="w-full rounded border border-border p-2" value={domain} onChange={(e) => setDomain(e.target.value)}>
            <option value="hiring">hiring</option>
            <option value="loan">loan</option>
            <option value="medical">medical</option>
            <option value="other">other</option>
          </select>
        </label>
      </div>
      <div>
        <p className="mb-2 text-sm font-semibold text-slate-700">Protected Attributes</p>
        <div className="grid gap-2 sm:grid-cols-2">
          {columns.map((col) => (
            <label key={col} className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={protectedAttributes.includes(col)} onChange={() => toggleAttr(col)} />
              {col}
            </label>
          ))}
        </div>
      </div>
      <button
        className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white"
        onClick={() => onConfirm({ ...detectResult, target_variable: targetVariable, protected_attributes: protectedAttributes, domain })}
      >
        Confirm and Continue
      </button>
    </section>
  )
}

export default DetectionResult
