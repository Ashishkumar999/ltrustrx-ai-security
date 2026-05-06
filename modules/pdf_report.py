from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

import os
from datetime import datetime


def generate_pdf_report(results):

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = f"reports/security_report_{timestamp}.pdf"

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "LtrustRx AI Security Report",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    target = Paragraph(
        f"<b>Target:</b> {results['target']}",
        styles['BodyText']
    )

    elements.append(target)

    status = Paragraph(
        f"<b>Status:</b> {results['status']}",
        styles['BodyText']
    )

    elements.append(status)
    elements.append(Spacer(1, 20))

    summary = results.get("summary", {})

    summary_text = f"""
    <b>Total Findings:</b> {summary.get('total', 0)}<br/>
    <b>High Severity:</b> {summary.get('high', 0)}<br/>
    <b>Medium Severity:</b> {summary.get('medium', 0)}<br/>
    <b>Low Severity:</b> {summary.get('low', 0)}
    """

    summary_paragraph = Paragraph(
        summary_text,
        styles['BodyText']
    )

    elements.append(summary_paragraph)
    elements.append(Spacer(1, 20))

    for issue in results.get("issues", []):

        issue_text = f"""
        <b>Issue:</b> {issue.get('issue')}<br/>
        <b>Severity:</b> {issue.get('severity')}<br/>
        <b>Payload:</b> {issue.get('payload')}<br/>
        <b>Recommendation:</b> {issue.get('recommendation')}
        """

        paragraph = Paragraph(
            issue_text,
            styles['BodyText']
        )

        elements.append(paragraph)
        elements.append(Spacer(1, 15))

    doc.build(elements)

    return file_path
