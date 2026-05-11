import html

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime


def generate_pdf_report(results):

    filename = (

        "reports/"

        +

        str(datetime.now().timestamp())

        +

        ".pdf"

    )


    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []


    title = Paragraph(

        "LtrustRx AI Security Assessment Report",

        styles["Title"]

    )

    elements.append(title)

    elements.append(Spacer(1, 20))


    summary = results["summary"]


    elements.append(

        Paragraph(

            f"Risk Score: {summary['risk_score']}",

            styles["BodyText"]

        )

    )


    elements.append(

        Paragraph(

            f"Security Posture: {summary['posture']}",

            styles["BodyText"]

        )

    )


    elements.append(

        Paragraph(

            f"Critical Findings: {summary['critical']}",

            styles["BodyText"]

        )

    )


    elements.append(Spacer(1, 20))


    for issue in results["issues"]:

        safe_issue = html.escape(
            issue["issue"]
        )

        safe_payload = html.escape(
            issue["payload"]
        )

        safe_recommendation = html.escape(
            issue["recommendation"]
        )

        text = f"""

        <b>Issue:</b> {safe_issue}<br/>

        <b>Severity:</b> {issue['severity']}<br/>

        <b>Payload:</b> {safe_payload}<br/>

        <b>Recommendation:</b>

        {safe_recommendation}<br/><br/>

        """

        elements.append(

            Paragraph(
                text,
                styles["BodyText"]
            )

        )


    doc.build(elements)


    return filename
