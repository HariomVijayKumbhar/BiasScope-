function DataPreview({ columns = [], rows = [], rowCount = 0, columnCount = 0 }) {
  if (!columns.length) return null

  return (
    <section className="card">
      <h3 className="text-lg font-semibold">Dataset Preview</h3>
      <p className="mb-3 text-sm text-slate-500">
        {rowCount} rows • {columnCount} columns
      </p>
      <div className="overflow-auto rounded-lg border border-border">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-50">
            <tr>
              {columns.map((column) => (
                <th key={column} className="px-3 py-2 text-left font-semibold text-slate-700">
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, rowIndex) => (
              <tr key={rowIndex} className="border-t border-border">
                {columns.map((column) => (
                  <td key={`${rowIndex}-${column}`} className="px-3 py-2 text-slate-700">
                    {String(row[column] ?? '')}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default DataPreview
