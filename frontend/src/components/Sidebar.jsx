const items = [
  { id: 'overview', label: 'Overview' },
  { id: 'audit', label: 'Audit Dashboard' },
  { id: 'report', label: 'Download Report' },
]

function Sidebar({ activeView, setActiveView, hasAudit, onDownloadReport, sessionId }) {
  return (
    <aside className="sticky top-20 h-fit w-60 rounded-xl border border-border bg-white p-3 shadow-sm">
      <nav className="space-y-1">
        {items.map((item) => (
          <button
            key={item.id}
            className={`w-full rounded-lg px-3 py-2 text-left text-sm ${activeView === item.id ? 'bg-primary text-white' : 'text-slate-700 hover:bg-slate-100'}`}
            onClick={() => setActiveView(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>
      <button
        className="mt-4 w-full rounded-lg border border-border px-3 py-2 text-sm font-semibold text-slate-700 disabled:opacity-40"
        disabled={!hasAudit || !sessionId}
        onClick={() => onDownloadReport(sessionId)}
      >
        Download PDF
      </button>
    </aside>
  )
}

export default Sidebar
