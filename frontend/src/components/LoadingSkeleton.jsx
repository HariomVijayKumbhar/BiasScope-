function LoadingSkeleton({ lines = 3 }) {
  return (
    <div className="card animate-pulse space-y-3">
      {Array.from({ length: lines }).map((_, idx) => (
        <div key={idx} className="h-4 w-full rounded bg-slate-200" />
      ))}
    </div>
  )
}

export default LoadingSkeleton
