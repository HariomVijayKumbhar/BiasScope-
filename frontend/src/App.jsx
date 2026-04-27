import { useEffect, useMemo, useState } from 'react'
import HomePage from './pages/HomePage'
import AuditPage from './pages/AuditPage'
import ReportPage from './pages/ReportPage'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import Toast from './components/Toast'
import { useUpload } from './hooks/useUpload'
import { useBiasAudit } from './hooks/useBiasAudit'
import { getHealth } from './services/api'

function App() {
  const [activeView, setActiveView] = useState('overview')
  const [toast, setToast] = useState(null)
  const [health, setHealth] = useState({ loading: true, ok: false, message: 'Checking API...' })

  const uploadState = useUpload()
  const auditState = useBiasAudit()

  const canRunAudit = useMemo(() => {
    return Boolean(uploadState.confirmedDetection && uploadState.uploadResult?.preview)
  }, [uploadState.confirmedDetection, uploadState.uploadResult])

  useEffect(() => {
    const runHealthCheck = async () => {
      try {
        const result = await getHealth()
        setHealth({ loading: false, ok: true, message: result.status })
      } catch (_error) {
        setHealth({ loading: false, ok: false, message: 'Backend unreachable' })
      }
    }
    runHealthCheck()
  }, [])

  const startAudit = async () => {
    try {
      await auditState.runAudit({
        sessionId: uploadState.uploadResult.session_id,
        dataset: uploadState.fullDataset,
        target: uploadState.detectResult.target_variable,
        protectedAttrs: uploadState.detectResult.protected_attributes,
        domain: uploadState.detectResult.domain,
      })
      setActiveView('audit')
      setToast({ type: 'success', message: 'Audit completed successfully.' })
    } catch (error) {
      setToast({ type: 'error', message: error.message || 'Audit failed.' })
    }
  }

  const resetAll = () => {
    uploadState.reset()
    auditState.reset()
    setActiveView('overview')
  }

  return (
    <div className="min-h-screen bg-bg text-slate-800">
      <Navbar
        datasetName={uploadState.fileMeta?.name || 'No dataset selected'}
        status={auditState.biasResult?.overall_passed ? 'Passed' : auditState.biasResult ? 'Bias Detected' : 'Pending'}
        health={health}
        onNewAudit={resetAll}
      />
      <div className="mx-auto flex max-w-[1400px] gap-4 p-4">
        <Sidebar
          activeView={activeView}
          setActiveView={setActiveView}
          hasAudit={Boolean(auditState.biasResult)}
          onDownloadReport={auditState.downloadReport}
          sessionId={uploadState.uploadResult?.session_id}
        />
        <main className="flex-1 space-y-6">
          {activeView === 'overview' && (
            <HomePage
              uploadState={uploadState}
              canRunAudit={canRunAudit}
              onRunAudit={startAudit}
            />
          )}
          {activeView === 'audit' && (
            <AuditPage
              uploadState={uploadState}
              auditState={auditState}
            />
          )}
          {activeView === 'report' && (
            <ReportPage
              sessionId={uploadState.uploadResult?.session_id}
              onDownloadReport={auditState.downloadReport}
            />
          )}
        </main>
      </div>
      {toast && <Toast type={toast.type} message={toast.message} onClose={() => setToast(null)} />}
    </div>
  )
}

export default App
