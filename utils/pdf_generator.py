import re

from fpdf import FPDF


# ---------------------------------------------------------
# LegalEase PDF
# ---------------------------------------------------------

class LegalEasePDF(FPDF):

    def header(self):
        self.set_font(
            "Times",
            style="B",
            size=10,
        )

        self.cell(
            0,
            7,
            "LegalEase",
            align="C",
        )

        self.ln(7)

    def footer(self):
        self.set_y(-15)

        self.set_font(
            "Times",
            size=8,
        )

        self.cell(
            0,
            5,
            "LegalEase | AI-Powered Legal Document Generator",
            align="C",
        )

        self.ln(4)

        self.cell(
            0,
            5,
            f"Page {self.page_no()}",
            align="C",
        )


# ---------------------------------------------------------
# Clean text
# ---------------------------------------------------------

def _clean_text(text: str) -> str:

    text = text.replace(
        "\r\n",
        "\n",
    )

    text = text.replace(
        "\r",
        "\n",
    )

    text = re.sub(
        r"^```(?:markdown|md|text)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    text = text.replace(
        "\u00A0",
        " ",
    )

    text = text.replace(
        "–",
        "-",
    )

    text = text.replace(
        "—",
        "-",
    )

    # Remove the LegalEase emoji if Gemini includes it.
    text = text.replace(
        "⚖️",
        "",
    )

    text = text.replace(
        "⚖",
        "",
    )

    # FPDF Times font does not support the Indian Rupee symbol.
    text = text.replace(
        "₹",
        "Rs. ",
    )

    return text


# ---------------------------------------------------------
# Remove Markdown formatting
# ---------------------------------------------------------

def _remove_inline_markdown(
    text: str,
) -> str:

    text = text.replace(
        "**",
        "",
    )

    text = text.replace(
        "__",
        "",
    )

    text = text.replace(
        "`",
        "",
    )

    return text.strip()


# ---------------------------------------------------------
# Write normal paragraph
# ---------------------------------------------------------

def _write_paragraph(
    pdf: FPDF,
    text: str,
):

    pdf.set_font(
        "Times",
        size=11,
    )

    pdf.multi_cell(
        0,
        6,
        text,
        align="L",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(1)


# ---------------------------------------------------------
# Create PDF
# ---------------------------------------------------------

def create_pdf(
    document_text: str,
) -> bytes:

    document_text = _clean_text(
        document_text
    )

    pdf = LegalEasePDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_margins(
        left=20,
        top=20,
        right=20,
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=23,
    )

    pdf.add_page()

    # -----------------------------------------------------
    # Process document
    # -----------------------------------------------------

    lines = document_text.split(
        "\n"
    )

    for line in lines:

        stripped = line.strip()

        # -------------------------------------------------
        # Empty line
        # -------------------------------------------------

        if not stripped:

            pdf.ln(3)

            continue

        # -------------------------------------------------
        # Main title
        # -------------------------------------------------

        if (
            stripped.startswith("# ")
            and not stripped.startswith("## ")
        ):

            title = stripped[2:].strip()

            title = _remove_inline_markdown(
                title
            )

            pdf.set_font(
                "Times",
                style="B",
                size=18,
            )

            pdf.multi_cell(
                0,
                9,
                title,
                align="C",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            pdf.ln(5)

            continue

        # -------------------------------------------------
        # Section heading
        # -------------------------------------------------

        if (
            stripped.startswith("## ")
            and not stripped.startswith("### ")
        ):

            heading = stripped[3:].strip()

            heading = _remove_inline_markdown(
                heading
            )

            pdf.ln(3)

            pdf.set_font(
                "Times",
                style="B",
                size=13,
            )

            pdf.multi_cell(
                0,
                7,
                heading,
                new_x="LMARGIN",
                new_y="NEXT",
            )

            pdf.ln(1)

            continue

        # -------------------------------------------------
        # Subheading
        # -------------------------------------------------

        if stripped.startswith("### "):

            heading = stripped[4:].strip()

            heading = _remove_inline_markdown(
                heading
            )

            pdf.ln(2)

            pdf.set_font(
                "Times",
                style="B",
                size=12,
            )

            pdf.multi_cell(
                0,
                6.5,
                heading,
                new_x="LMARGIN",
                new_y="NEXT",
            )

            pdf.ln(1)

            continue

        # -------------------------------------------------
        # Bullet
        # -------------------------------------------------

        bullet_match = re.match(
            r"^[-*+]\s+(.*)",
            stripped,
        )

        if bullet_match:

            bullet_text = (
                bullet_match.group(1)
            )

            bullet_text = (
                _remove_inline_markdown(
                    bullet_text
                )
            )

            pdf.set_font(
                "Times",
                size=11,
            )

            pdf.set_x(
                pdf.l_margin + 5
            )

            pdf.multi_cell(
                0,
                6,
                "- " + bullet_text,
                new_x="LMARGIN",
                new_y="NEXT",
            )

            continue

        # -------------------------------------------------
        # Numbered clause
        # -------------------------------------------------

        numbered_match = re.match(
            r"^(\d+)[.)]\s+(.*)",
            stripped,
        )

        if numbered_match:

            number = (
                numbered_match.group(1)
            )

            content = (
                numbered_match.group(2)
            )

            content = (
                _remove_inline_markdown(
                    content
                )
            )

            pdf.set_font(
                "Times",
                style="B",
                size=11,
            )

            pdf.multi_cell(
                0,
                6,
                number + ". " + content,
                new_x="LMARGIN",
                new_y="NEXT",
            )

            pdf.ln(1)

            continue

        # -------------------------------------------------
        # Lettered subclause
        # -------------------------------------------------

        lettered_match = re.match(
            r"^([a-z])\)\s+(.*)",
            stripped,
            flags=re.IGNORECASE,
        )

        if lettered_match:

            letter = (
                lettered_match.group(1)
            )

            content = (
                lettered_match.group(2)
            )

            content = (
                _remove_inline_markdown(
                    content
                )
            )

            pdf.set_x(
                pdf.l_margin + 7
            )

            pdf.set_font(
                "Times",
                size=11,
            )

            pdf.multi_cell(
                0,
                6,
                letter + ") " + content,
                new_x="LMARGIN",
                new_y="NEXT",
            )

            continue

        # -------------------------------------------------
        # Signature fields
        # -------------------------------------------------

        if (
            stripped.startswith("By:")
            or stripped.startswith("Name:")
            or stripped.startswith("Title:")
            or stripped.startswith("Date:")
            or stripped.startswith("Signature:")
            or stripped.startswith(
                "Authorized Representative:"
            )
        ):

            signature_text = (
                _remove_inline_markdown(
                    stripped
                )
            )

            pdf.set_font(
                "Times",
                size=11,
            )

            pdf.multi_cell(
                0,
                6,
                signature_text,
                new_x="LMARGIN",
                new_y="NEXT",
            )

            continue

        # -------------------------------------------------
        # Normal paragraph
        # -------------------------------------------------

        paragraph = (
            _remove_inline_markdown(
                stripped
            )
        )

        _write_paragraph(
            pdf,
            paragraph,
        )

    # -----------------------------------------------------
    # Generate PDF
    # -----------------------------------------------------

    output = pdf.output()

    if isinstance(
        output,
        bytes,
    ):
        return output

    return bytes(output)