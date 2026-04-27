function ReportPage({ sessionId, onDownloadReport }) {
  return (
    <section className="card">
      <h2 className="mb-2 text-xl font-semibold">Compliance Report</h2>
      <p className="mb-4 text-sm text-slate-600">
        Generate and download a multi-section audit report suitable for compliance workflows.
      </p>
      <button
        className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white disabled:opacity-40"
        disabled={!sessionId}
        onClick={() => onDownloadReport(sessionId)}
      >
        Download Report
      </button>
    </section>
  )
}

export default ReportPage
