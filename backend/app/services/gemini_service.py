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


def _generate_with_groq(prompt: str) -> dict[str, Any]:
    if not settings.groq_api_key:
        raise ValueError("Groq key not set")
    from groq import Groq
    client = Groq(api_key=settings.groq_api_key)
    completion = client.chat.completions.create(
        model=settings.groq_model or "llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)


def _generate_with_gemini(prompt: str) -> dict[str, Any]:
    if not settings.gemini_api_key:
        raise ValueError("Gemini key not set")
    import google.generativeai as genai
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(settings.gemini_model or "gemini-1.5-flash")
    response = model.generate_content(prompt)
    try:
        return _extract_json(response.text)
    except Exception as e:
        raise ValueError(f"Gemini error: {e}")


def _generate_json(prompt: str) -> dict[str, Any]:
    # Try Groq first
    if settings.groq_api_key:
        try:
            return _generate_with_groq(prompt)
        except Exception as e:
            print(f"Groq failed, falling back to Gemini: {e}")
    
    # Try Gemini second
    if settings.gemini_api_key:
        try:
            return _generate_with_gemini(prompt)
        except Exception as e:
            print(f"Gemini failed: {e}")
    
    raise ValueError("No AI providers (Groq/Gemini) worked or are configured.")


def _fallback_detection(columns: list[str], sample_rows: list[dict], reason: str) -> dict[str, Any]:
    target_candidates = ["prediction", "target", "label", "survived", "decision"]
    protected_candidates = ["gender", "sex", "race", "age"]
    lowered = {col.lower(): col for col in columns}
    target = next((lowered[name] for name in target_candidates if name in lowered), columns[-1] if columns else "")
    protected = [lowered[name] for name in protected_candidates if name in lowered]
    return {
        "target_variable": target,
        "protected_attributes": protected[:2],
        "domain": "other",
        "confidence": "low",
        "reasoning": f"Heuristic fallback: {reason}",
    }


def detect_columns(columns: list[str], sample_rows: list[dict]) -> dict[str, Any]:
    prompt = f"""
Analyze this dataset sample and return valid JSON:
Columns: {columns}
Sample rows: {sample_rows[:5]}

JSON structure:
{{
  "target_variable": "column_name",
  "protected_attributes": ["col1", "col2"],
  "domain": "hiring | loan | medical | other",
  "confidence": "high | medium | low",
  "reasoning": "description"
}}
"""
    try:
        return _generate_json(prompt)
    except Exception as e:
        return _fallback_detection(columns, sample_rows, str(e))


def explain_audit(audit_results: dict[str, Any]) -> dict[str, Any]:
    prompt = f"Audit results: {audit_results}\nExplain these results in plain English. Return ONLY JSON with summary, severity, issues list, and recommendations list."
    try:
        return _generate_json(prompt)
    except Exception as e:
        return {"summary": f"Fallback explanation (AI error: {e})", "severity": "medium", "issues": [], "recommendations": []}


def chat_reply(message: str, audit_context: dict[str, Any], history: list[dict[str, str]]) -> str:
    prompt = f"Audit data: {audit_context}\nHistory: {history}\nQuestion: {message}\nAssistant, provide a concise answer."
    try:
        # For chat, we can use a simpler generation or just reuse _generate_json and extract a string
        # To keep it simple, let's just use Groq/Gemini directly for text
        if settings.groq_api_key:
            from groq import Groq
            client = Groq(api_key=settings.groq_api_key)
            completion = client.chat.completions.create(
                model=settings.groq_model or "llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
        elif settings.gemini_api_key:
            import google.generativeai as genai
            genai.configure(api_key=settings.gemini_api_key)
            model = genai.GenerativeModel(settings.gemini_model or "gemini-1.5-flash")
            return model.generate_content(prompt).text
        return "AI not configured."
    except Exception as e:
        return f"Chat error: {e}"
