function Navbar({ datasetName, status, health, onNewAudit }) {
  const dotClass = health.loading ? 'bg-yellow-400' : health.ok ? 'bg-green-500' : 'bg-red-500'

  return (
    <header className="sticky top-0 z-20 border-b border-border bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-[1400px] items-center justify-between px-4 py-3">
        <div>
          <h1 className="text-xl font-bold text-slate-800">BiasScope</h1>
          <p className="text-sm text-slate-500">{datasetName}</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="inline-flex items-center gap-2 rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-700">
            <span className={`h-2.5 w-2.5 rounded-full ${dotClass}`} />
            {health.message}
          </span>
          <span className="badge bg-slate-100 text-slate-700">{status}</span>
          <button className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white" onClick={onNewAudit}>
            New Audit
          </button>
        </div>
      </div>
    </header>
  )
}

export default Navbar
