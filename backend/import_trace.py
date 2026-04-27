import importlib

modules = [
    "app.config",
    "app.utils.response_utils",
    "app.utils.file_utils",
    "app.utils.session_store",
    "app.models.upload_models",
    "app.models.detect_models",
    "app.models.bias_models",
    "app.models.counterfactual_models",
    "app.models.proxy_models",
    "app.models.explain_models",
    "app.models.chat_models",
    "app.services.gemini_service",
    "app.services.bias_service",
    "app.services.counterfactual_service",
    "app.services.proxy_service",
    "app.services.report_service",
    "app.routers.health",
    "app.routers.upload",
    "app.routers.detect",
    "app.routers.bias",
    "app.routers.counterfactual",
    "app.routers.proxy",
    "app.routers.explain",
    "app.routers.report",
    "app.routers.chat",
]

for name in modules:
    print("importing", name, flush=True)
    importlib.import_module(name)
    print("ok", name, flush=True)

print("all imports ok", flush=True)
