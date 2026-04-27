import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { bytesToMb } from '../utils/formatters'

function UploadZone({ onFileSelect, loading, progress, fileMeta }) {
  const onDrop = useCallback(
    (acceptedFiles) => {
      const file = acceptedFiles?.[0]
      if (file) {
        onFileSelect(file)
      }
    },
    [onFileSelect],
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/csv': ['.csv'] },
    maxSize: 50 * 1024 * 1024,
    multiple: false,
  })

  return (
    <section className="card">
      <h2 className="mb-2 text-lg font-semibold">Upload Dataset</h2>
      <div
        {...getRootProps()}
        className={`rounded-lg border-2 border-dashed p-8 text-center ${isDragActive ? 'border-primary bg-blue-50' : 'border-border'}`}
      >
        <input {...getInputProps()} />
        <p className="text-slate-600">Drag and drop a CSV file here, or click to browse.</p>
      </div>
      {loading && <p className="mt-3 text-sm text-slate-600">Uploading... {progress}%</p>}
      {fileMeta && (
        <p className="mt-3 text-sm text-slate-700">
          Selected: <span className="font-semibold">{fileMeta.name}</span> ({bytesToMb(fileMeta.size)})
        </p>
      )}
    </section>
  )
}

export default UploadZone
