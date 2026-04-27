import json
import traceback
from pathlib import Path

import requests

BASE = "http://127.0.0.1:8000"
CSV_PATH = Path(__file__).parent / "smoke_test.csv"
REPORT_PATH = Path(__file__).parent / "smoke_report.pdf"


def unwrap(resp: requests.Response):
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise RuntimeError(payload)
    return payload["data"]


try:
    summary = {}

    health = unwrap(requests.get(f"{BASE}/health", timeout=30))
    summary["health"] = health["status"]

    with CSV_PATH.open("rb") as f:
        upload = unwrap(requests.post(f"{BASE}/upload", files={"file": (CSV_PATH.name, f, "text/csv")}, timeout=120))

    summary["upload_rows"] = upload["row_count"]
    session_id = upload["session_id"]

    detect = unwrap(
        requests.post(
            f"{BASE}/detect",
            json={"columns": upload["columns"], "sample_rows": upload["preview"]},
            timeout=120,
        )
    )
    summary["detect_target"] = detect["target_variable"]
    summary["protected"] = detect["protected_attributes"]

    bias = unwrap(
        requests.post(
            f"{BASE}/bias",
            json={
                "session_id": session_id,
                "dataset": upload["dataset"],
                "target": detect["target_variable"],
                "protected_attrs": detect["protected_attributes"],
            },
            timeout=120,
        )
    )
    summary["overall_passed"] = bias["overall_passed"]

    cf = unwrap(
        requests.post(
            f"{BASE}/counterfactual",
            json={
                "session_id": session_id,
                "dataset": upload["dataset"],
                "target": detect["target_variable"],
                "protected_attrs": detect["protected_attributes"],
            },
            timeout=120,
        )
    )
    summary["cf_risk"] = cf["risk_label"]

    proxy = unwrap(
        requests.post(
            f"{BASE}/proxy",
            json={
                "session_id": session_id,
                "dataset": upload["dataset"],
                "protected_attrs": detect["protected_attributes"],
            },
            timeout=120,
        )
    )
    summary["proxy_count"] = len(proxy["proxy_features"])

    explain = unwrap(
        requests.post(
            f"{BASE}/explain",
            json={
                "session_id": session_id,
                "bias_results": bias,
                "counterfactual_results": cf,
                "proxy_results": proxy,
                "domain": detect["domain"],
                "protected_attribute": detect["protected_attributes"][0] if detect["protected_attributes"] else "",
            },
            timeout=120,
        )
    )
    summary["severity"] = explain["severity"]

    chat = unwrap(
        requests.post(
            f"{BASE}/chat",
            json={
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
            timeout=120,
        )
    )
    summary["chat_reply_len"] = len(chat["reply"])

    report_resp = requests.get(f"{BASE}/report", params={"session_id": session_id}, timeout=120)
    report_resp.raise_for_status()
    REPORT_PATH.write_bytes(report_resp.content)
    summary["report_size_bytes"] = REPORT_PATH.stat().st_size
    summary["session_id"] = session_id

    print(json.dumps(summary, indent=2))
except Exception as exc:
    print("smoke-test-error:", exc)
    traceback.print_exc()
    raise
