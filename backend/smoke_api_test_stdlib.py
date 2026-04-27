import json
import uuid
from pathlib import Path
from urllib import parse, request

BASE = "http://127.0.0.1:8000"
CSV_PATH = Path(__file__).parent / "smoke_test.csv"
REPORT_PATH = Path(__file__).parent / "smoke_report.pdf"


def http_json(method: str, path: str, payload: dict | None = None) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(f"{BASE}{path}", data=data, headers=headers, method=method)
    with request.urlopen(req, timeout=120) as resp:
        body = resp.read().decode("utf-8")
        parsed = json.loads(body)
        return parsed


def http_upload_csv(path: str, file_path: Path) -> dict:
    boundary = f"----BiasScopeBoundary{uuid.uuid4().hex}"
    file_bytes = file_path.read_bytes()
    lines = []
    lines.append(f"--{boundary}\r\n".encode())
    lines.append(
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{file_path.name}\"\r\n".encode()
    )
    lines.append(b"Content-Type: text/csv\r\n\r\n")
    lines.append(file_bytes)
    lines.append(b"\r\n")
    lines.append(f"--{boundary}--\r\n".encode())
    body = b"".join(lines)

    req = request.Request(
        f"{BASE}{path}",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_download(path: str, out_path: Path) -> int:
    with request.urlopen(f"{BASE}{path}", timeout=120) as resp:
        data = resp.read()
    out_path.write_bytes(data)
    return len(data)


def unwrap(payload: dict) -> dict:
    if not payload.get("success"):
        raise RuntimeError(payload)
    return payload["data"]


summary = {}

health = unwrap(http_json("GET", "/health"))
summary["health"] = health["status"]

upload = unwrap(http_upload_csv("/upload", CSV_PATH))
summary["upload_rows"] = upload["row_count"]
session_id = upload["session_id"]

detect = unwrap(
    http_json(
        "POST",
        "/detect",
        {"columns": upload["columns"], "sample_rows": upload["preview"]},
    )
)
summary["detect_target"] = detect["target_variable"]
summary["protected"] = detect["protected_attributes"]

bias = unwrap(
    http_json(
        "POST",
        "/bias",
        {
            "session_id": session_id,
            "dataset": upload["dataset"],
            "target": detect["target_variable"],
            "protected_attrs": detect["protected_attributes"],
        },
    )
)
summary["overall_passed"] = bias["overall_passed"]

cf = unwrap(
    http_json(
        "POST",
        "/counterfactual",
        {
            "session_id": session_id,
            "dataset": upload["dataset"],
            "target": detect["target_variable"],
            "protected_attrs": detect["protected_attributes"],
        },
    )
)
summary["cf_risk"] = cf["risk_label"]

proxy = unwrap(
    http_json(
        "POST",
        "/proxy",
        {
            "session_id": session_id,
            "dataset": upload["dataset"],
            "protected_attrs": detect["protected_attributes"],
        },
    )
)
summary["proxy_count"] = len(proxy["proxy_features"])

explain = unwrap(
    http_json(
        "POST",
        "/explain",
        {
            "session_id": session_id,
            "bias_results": bias,
            "counterfactual_results": cf,
            "proxy_results": proxy,
            "domain": detect["domain"],
            "protected_attribute": detect["protected_attributes"][0] if detect["protected_attributes"] else "",
        },
    )
)
summary["severity"] = explain["severity"]

chat = unwrap(
    http_json(
        "POST",
        "/chat",
        {
            "message": "What is the biggest risk in my dataset?",
            "audit_context": {
                "dataset_name": CSV_PATH.name,
                "domain": detect["domain"],
                "protected_attribute": detect["protected_attributes"][0] if detect["protected_attributes"] else "",
                "bias_results": bias,
                "counterfactual_score": cf,
                "proxy_features": proxy["proxy_features"],
                "explanation_summary": explain["summary"],
                "severity": explain["severity"],
            },
            "history": [],
        },
    )
)
summary["chat_reply_len"] = len(chat["reply"])

summary["report_size_bytes"] = http_download(f"/report?{parse.urlencode({'session_id': session_id})}", REPORT_PATH)
summary["session_id"] = session_id

print(json.dumps(summary, indent=2))
