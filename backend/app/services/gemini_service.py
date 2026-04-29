import json
import re
from typing import Any

from app.config import settings


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    return json.loads(text)


def _generate_json(prompt: str) -> dict[str, Any]:
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")
    import google.generativeai as genai

    try:
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(settings.gemini_model)
        response = model.generate_content(prompt)
        # Handle cases where safety filters block the response
        try:
            raw_text = response.text or ""
        except Exception as e:
            print(f"Gemini response.text error: {e}")
            raise ValueError(f"Gemini blocked the response or failed: {e}")
            
        return _extract_json(raw_text)
    except Exception as e:
        print(f"Gemini generation error: {e}")
        raise


def _fallback_detection(columns: list[str], sample_rows: list[dict], reason: str) -> dict[str, Any]:
    target_candidates = [
        "prediction", "predicted", "target", "label", "approved", "outcome", "decision", "survived"
    ]
    protected_candidates = ["gender", "sex", "race", "ethnicity", "age", "zip", "zipcode"]

    lowered = {col.lower(): col for col in columns}
    target = next((lowered[name] for name in target_candidates if name in lowered), columns[-1] if columns else "")
    protected = [lowered[name] for name in protected_candidates if name in lowered]

    sample_text = str(sample_rows[:3]).lower()
    if any(k in sample_text for k in ["resume", "candidate", "hiring", "interview"]):
        domain = "hiring"
    elif any(k in sample_text for k in ["loan", "credit", "income", "default"]):
        domain = "loan"
    elif any(k in sample_text for k in ["patient", "diagnosis", "triage", "medical"]):
        domain = "medical"
    else:
        domain = "other"

    return {
        "target_variable": target,
        "protected_attributes": protected[:2],
        "domain": domain,
        "confidence": "low",
        "reasoning": f"Heuristic fallback: {reason}",
    }


def detect_columns(columns: list[str], sample_rows: list[dict]) -> dict[str, Any]:
    if not settings.gemini_api_key:
        return _fallback_detection(columns, sample_rows, "Gemini key not configured.")

    prompt = f"""
You are a data science expert specializing in AI fairness auditing.

Analyze this dataset sample:
Columns: {columns}
Sample rows (first 10): {sample_rows[:10]}

Return ONLY valid JSON with this exact structure - no explanation, no markdown:
{{
  \"target_variable\": \"column_name\",
  \"protected_attributes\": [\"col1\", \"col2\"],
  \"domain\": \"hiring | loan | medical | other\",
  \"confidence\": \"high | medium | low\",
  \"reasoning\": \"one sentence explaining your detection\"
}}

Rules:
- target_variable must be one of the provided column names
- protected_attributes must only contain columns from the provided list
- If unsure, set confidence to \"low\"
"""
    try:
        return _generate_json(prompt)
    except Exception as e:
        print(f"Falling back to heuristics due to AI error: {e}")
        return _fallback_detection(columns, sample_rows, str(e))


def explain_audit(audit_results: dict[str, Any]) -> dict[str, Any]:
    def _fallback_explanation(audit_results: dict[str, Any], reason: str) -> dict[str, Any]:
        metrics = audit_results.get("bias_results", {}).get("metrics", [])
        failed = [m for m in metrics if not m.get("passed")]
        severity = "high" if failed else "low"
        issues = [
            {
                "title": m.get("name", "Metric issue"),
                "description": m.get("interpretation", "This metric indicates a fairness gap."),
                "metric": m.get("name", "Unknown metric"),
            }
            for m in failed[:3]
        ]
        recommendations = [
            {
                "title": "Reweigh training samples",
                "description": "Adjust sample weights to reduce imbalance between protected groups.",
                "priority": "immediate",
                "code": "from aif360.algorithms.preprocessing import Reweighing\n# Apply reweighing before model training",
            },
            {
                "title": "Review proxy features",
                "description": "Remove or constrain highly correlated proxy features before retraining.",
                "priority": "short-term",
                "code": "high_risk = [f for f in proxy_features if f['correlation'] > 0.5]\n# Drop or regularize these features",
            },
        ]
        return {
            "summary": f"Heuristic fallback (AI error: {reason}). Review failed metrics and proxy signals before using this model in production.",
            "severity": severity,
            "issues": issues or [{"title": "No critical issue detected", "description": "All primary fairness checks passed.", "metric": "overall"}],
            "recommendations": recommendations,
        }

    if not settings.gemini_api_key:
        return _fallback_explanation(audit_results, "Gemini key not configured.")

    prompt = f"""
You are a bias auditing expert. Your audience is a compliance officer with no data science background.

Here are the full audit results:
{audit_results}

Return ONLY valid JSON with this exact structure:
{{
  \"summary\": \"2-3 sentence plain English overview of findings\",
  \"severity\": \"critical | high | medium | low\",
  \"issues\": [
    {{
      \"title\": \"Issue name\",
      \"description\": \"What this means in plain English\",
      \"metric\": \"which metric triggered this\"
    }}
  ],
  \"recommendations\": [
    {{
      \"title\": \"Fix title\",
      \"description\": \"What to do and why\",
      \"priority\": \"immediate | short-term | long-term\",
      \"code\": \"working Python code implementing this fix\"
    }}
  ]
}}
"""
    try:
        return _generate_json(prompt)
    except Exception as e:
        print(f"Explain fallback due to error: {e}")
        return _fallback_explanation(audit_results, str(e))


def chat_reply(message: str, audit_context: dict[str, Any], history: list[dict[str, str]]) -> str:
    prompt = f"""
You are BiasScope's AI audit assistant. You help compliance officers, HR managers, and legal teams understand their AI bias audit results.

You have full access to this audit:
{audit_context}

Conversation history:
{history}

User question:
{message}

Rules:
- Answer only questions about THIS audit
- Use plain English
- Be concise (2-4 sentences unless detail is requested)
- If asked outside context, say so honestly
- Never make up values
"""
    if not settings.gemini_api_key:
        return "Gemini is not configured. Please set GEMINI_API_KEY and retry."
    import google.generativeai as genai

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(settings.gemini_model)
    response = model.generate_content(prompt)
    return (response.text or "I could not generate a response.").strip()
