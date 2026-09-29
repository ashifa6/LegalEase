import re


def clean_text(text: str) -> str:
    """
    Clean generated document text while preserving structure.
    """

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

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

    text = text.replace("\u00A0", " ")

    # Convert common bullet characters.
    text = text.replace("•", "*")
    text = text.replace("●", "*")
    text = text.replace("▪", "*")

    # Normalize dashes.
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    lines = []

    for line in text.split("\n"):
        lines.append(line.rstrip())

    text = "\n".join(lines)

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


def remove_markdown_formatting(text: str) -> str:
    """
    Convert Markdown formatting into clean plain text.
    """

    text = clean_text(text)

    # Main and section headings.
    text = re.sub(
        r"^\s*#{1,6}\s*",
        "",
        text,
        flags=re.MULTILINE,
    )

    # Bullets.
    text = re.sub(
        r"^\s*[-*+]\s+",
        "• ",
        text,
        flags=re.MULTILINE,
    )

    # Bold / italic.
    text = text.replace("**", "")
    text = text.replace("__", "")

    text = re.sub(
        r"(?<!\*)\*(?!\*)",
        "",
        text,
    )

    # Inline code.
    text = text.replace("`", "")

    return text.strip()


def create_txt_document(text: str) -> str:
    """
    Create a professional plain-text version of the document.
    """

    text = clean_text(text)

    lines = []

    for line in text.split("\n"):

        stripped = line.strip()

        if not stripped:
            lines.append("")
            continue

        # Main title.
        if (
            stripped.startswith("# ")
            and not stripped.startswith("## ")
        ):

            title = stripped[2:].strip()

            title = title.replace(
                "**",
                "",
            )

            lines.append("")
            lines.append(title.upper())
            lines.append("=" * len(title))
            lines.append("")

            continue

        # Level 2 heading.
        if (
            stripped.startswith("## ")
            and not stripped.startswith("### ")
        ):

            heading = stripped[3:].strip()

            heading = heading.replace(
                "**",
                "",
            )

            lines.append("")
            lines.append(heading.upper())
            lines.append("-" * len(heading))
            lines.append("")

            continue

        # Level 3 heading.
        if stripped.startswith("### "):

            heading = stripped[4:].strip()

            heading = heading.replace(
                "**",
                "",
            )

            lines.append("")
            lines.append(heading)
            lines.append("-" * len(heading))
            lines.append("")

            continue

        # Bullet.
        bullet_match = re.match(
            r"^[-*+]\s+(.*)",
            stripped,
        )

        if bullet_match:

            bullet_text = bullet_match.group(1)

            bullet_text = bullet_text.replace(
                "**",
                "",
            )

            bullet_text = bullet_text.replace(
                "`",
                "",
            )

            lines.append(
                "• " + bullet_text
            )

            continue

        # Normal text.
        cleaned_line = stripped

        cleaned_line = cleaned_line.replace(
            "**",
            "",
        )

        cleaned_line = cleaned_line.replace(
            "__",
            "",
        )

        cleaned_line = cleaned_line.replace(
            "`",
            "",
        )

        lines.append(cleaned_line)

    result = "\n".join(lines)

    result = re.sub(
        r"\n{3,}",
        "\n\n",
        result,
    )

    return result.strip() + "\n"


def create_safe_filename(
    document_type: str,
    default: str = "legal_document",
) -> str:
    """
    Convert document type into a safe Windows filename.
    """

    if not document_type:
        return default

    filename = document_type.strip()

    filename = re.sub(
        r"\s+",
        "_",
        filename,
    )

    filename = re.sub(
        r'[<>:"/\\|?*]',
        "",
        filename,
    )

    filename = re.sub(
        r"[^A-Za-z0-9_.-]",
        "",
        filename,
    )

    filename = re.sub(
        r"_+",
        "_",
        filename,
    )

    filename = filename.strip(
        "._"
    )

    if not filename:
        return default

    return filename.lower()