from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    filename,
    disease,
    confidence,
    explanation,
    solution
):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("MedVision AI Medical Report", styles["Title"])
    )

    content.append(Spacer(1,20))

    content.append(
        Paragraph(
            f"<b>Disease:</b> {disease}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Confidence:</b> {confidence}%",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Explanation:</b> {explanation}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Solution:</b> {solution}",
            styles["BodyText"]
        )
    )

    pdf.build(content)