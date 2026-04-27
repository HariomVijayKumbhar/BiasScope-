import UploadZone from '../components/UploadZone'
import DataPreview from '../components/DataPreview'
import DetectionResult from '../components/DetectionResult'
import LoadingSkeleton from '../components/LoadingSkeleton'

function HomePage({ uploadState, canRunAudit, onRunAudit }) {
  return (
    <section className="space-y-4">
      <UploadZone
        onFileSelect={uploadState.handleUpload}
        loading={uploadState.loading}
        progress={uploadState.uploadProgress}
        fileMeta={uploadState.fileMeta}
      />
      {uploadState.error && <div className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{uploadState.error}</div>}
      {uploadState.loading && <LoadingSkeleton lines={4} />}
      {uploadState.uploadResult && (
        <DataPreview
          columns={uploadState.uploadResult.columns}
          rows={uploadState.uploadResult.preview}
          rowCount={uploadState.uploadResult.row_count}
          columnCount={uploadState.uploadResult.column_count}
        />
      )}
      {(uploadState.detectLoading || uploadState.detectResult) && (
        <DetectionResult
          columns={uploadState.uploadResult?.columns || []}
          detectResult={uploadState.detectResult}
          loading={uploadState.detectLoading}
          onConfirm={uploadState.confirmDetection}
        />
      )}
      <button
        className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white disabled:opacity-40"
        disabled={!canRunAudit}
        onClick={onRunAudit}
      >
        Run Full Audit
      </button>
    </section>
  )
}

export default HomePage
