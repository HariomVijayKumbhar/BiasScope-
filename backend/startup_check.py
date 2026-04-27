import traceback
import uvicorn

print("uvicorn-import-ok")

try:
    import app.main as m
    print("app-import-ok", bool(m.app))
    uvicorn.run(m.app, host="127.0.0.1", port=8000, log_level="debug")
except Exception as exc:
    print("startup-error:", exc)
    traceback.print_exc()
