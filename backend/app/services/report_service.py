from datetime import datetime, timezone
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_pdf_report(session: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="BiasScope Audit Report")
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("ReportTitle", parent=styles["Title"], fontSize=22, leading=28)

    elements = []
    elements.append(Paragraph("BiasScope - Bias Audit Report", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated: {datetime.now(timezone.utc).isoformat()}", styles["Normal"]))
    elements.append(Spacer(1, 10))

    bias = session.get("bias_results", {})
    cf = session.get("counterfactual_results", {})
    proxy = session.get("proxy_results", {})
    explain = session.get("explain_results", {})

    verdict = "PASSED" if bias.get("overall_passed") else "BIAS DETECTED"
    elements.append(Paragraph(f"Overall Verdict: <b>{verdict}</b>", styles["Heading2"]))
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Executive Summary", styles["Heading2"]))
    elements.append(Paragraph(explain.get("summary", "No summary available."), styles["BodyText"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Fairness Metrics", styles["Heading2"]))
    metric_rows = [["Metric", "Value", "Threshold", "Result"]]
    for metric in bias.get("metrics", []):
        metric_rows.append(
            [
                metric.get("name", ""),
                str(metric.get("value", "")),
                metric.get("threshold", ""),
                "PASS" if metric.get("passed") else "FAIL",
            ]
        )
    metric_table = Table(metric_rows, repeatRows=1)
    metric_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3B82F6")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ]
        )
    )
    elements.append(metric_table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Counterfactual Analysis", styles["Heading2"]))
    elements.append(Paragraph(f"Fairness Score: {cf.get('fairness_score', 0)}%", styles["Normal"]))
    elements.append(Paragraph(f"Flip Rate: {cf.get('flip_rate', 0)}%", styles["Normal"]))
    elements.append(Paragraph(f"Risk Label: {cf.get('risk_label', 'N/A')}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Proxy Bias Analysis", styles["Heading2"]))
    proxy_rows = [["Feature", "Attribute", "Correlation", "Risk"]]
    for row in proxy.get("proxy_features", [])[:5]:
        proxy_rows.append(
            [
                row.get("feature", ""),
                row.get("correlated_attribute", ""),
                str(row.get("correlation", "")),
                row.get("risk_level", ""),
            ]
        )
    proxy_table = Table(proxy_rows, repeatRows=1)
    proxy_table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1"))]))
    elements.append(proxy_table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Recommendations", styles["Heading2"]))
    for idx, rec in enumerate(explain.get("recommendations", []), start=1):
        elements.append(Paragraph(f"{idx}. {rec.get('title', '')} ({rec.get('priority', '')})", styles["BodyText"]))
        elements.append(Paragraph(rec.get("description", ""), styles["Normal"]))
        elements.append(Spacer(1, 6))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
