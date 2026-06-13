from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from datetime import datetime


def create_health_report(
    report_text
):

    filename = (
        f"Health_Report_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Health Monitoring Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(
            1,
            20
        )
    )

    for line in report_text.split("\n"):

        if line.strip():

            content.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

            content.append(
                Spacer(
                    1,
                    5
                )
            )

    doc.build(
        content
    )

    return filename