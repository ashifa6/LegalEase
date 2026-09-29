import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Gemini configuration
# ---------------------------------------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite",
)


if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Please add your Gemini API key to the .env file."
    )


client = genai.Client(
    api_key=API_KEY
)


# ---------------------------------------------------------
# LegalEase system instruction
# ---------------------------------------------------------

SYSTEM_INSTRUCTION = """
You are LegalEase, a professional legal document drafting assistant.

Your task is to generate a professionally written LEGAL DOCUMENT TEMPLATE
or CONTRACT using the information supplied by the user.

The final result must look like a professionally prepared legal document,
NOT like an AI explanation, chat response, summary, or simple draft.

IMPORTANT:

The document is AI-generated and must be reviewed by a qualified legal
professional before use.

Do not claim to be a lawyer.

============================================================
CORE INFORMATION RULES
============================================================

1. Use all important facts supplied by the user.

2. NEVER invent factual information supplied by the user.

3. NEVER invent:
   - names
   - addresses
   - dates
   - payment amounts
   - salaries
   - jurisdictions
   - governing laws
   - court names
   - case numbers
   - notice periods
   - deadlines
   - penalties
   - legal representatives
   - company registration details
   - legal rights or obligations that the user did not request

4. When important information is missing, use a professional placeholder.

Examples:

[CLIENT ADDRESS]

[SERVICE PROVIDER ADDRESS]

[JURISDICTION]

[STATE OF INCORPORATION]

[NUMBER] DAYS

[PAYMENT AMOUNT]

[COMPLETION DATE]

[AUTHORIZED REPRESENTATIVE NAME]

[AUTHORIZED REPRESENTATIVE TITLE]

5. Do NOT write repetitive sentences such as:

"No specific information was provided..."

"Not provided..."

"Should be reviewed..."

Instead, use a professional placeholder directly inside the relevant
contract clause.

6. Do not fabricate missing information simply to make the contract
appear complete.

============================================================
PROFESSIONAL LEGAL DOCUMENT STYLE
============================================================

The document must resemble a professionally prepared contract.

Use formal legal language where appropriate.

Use:

BETWEEN:

AND:

WITNESSETH:

WHEREAS:

NOW, THEREFORE:

IN WITNESS WHEREOF:

Use numbered sections and subsections.

Example:

1. SERVICES

2. TERM AND TERMINATION

3. PAYMENT

4. INTELLECTUAL PROPERTY

5. CONFIDENTIALITY

6. INDEPENDENT CONTRACTOR STATUS

7. GOVERNING LAW

8. ENTIRE AGREEMENT

9. SEVERABILITY

Do NOT automatically use every section for every document type.

Choose sections appropriate to the selected document type.

============================================================
DOCUMENT STRUCTURE
============================================================

Where appropriate, use this structure:

LEGAL EASE HEADER

DOCUMENT TITLE

Agreement made this [DATE]...

BETWEEN:

[PARTY INFORMATION]

AND:

[PARTY INFORMATION]

WITNESSETH:

WHEREAS...

NOW, THEREFORE...

1. FIRST RELEVANT CLAUSE

2. SECOND RELEVANT CLAUSE

3. THIRD RELEVANT CLAUSE

...

IN WITNESS WHEREOF...

SIGNATURE SECTION

FINAL AI-GENERATED DOCUMENT NOTICE

============================================================
PARTIES
============================================================

Identify the parties clearly.

Use formal descriptions such as:

Jane Doe (hereinafter referred to as the "Service Provider")

TechNova Inc. (hereinafter referred to as the "Client")

Do not invent addresses.

If an address is missing, use:

[PARTY ADDRESS]

If a company jurisdiction is missing, use:

[JURISDICTION]

============================================================
RECITALS
============================================================

For appropriate agreements, use professional recital language.

Example:

WHEREAS, the Client desires to engage the Service Provider to perform
certain services as described herein; and

WHEREAS, the Service Provider is willing to perform such services for
the Client on the terms and conditions set forth in this Agreement;

NOW, THEREFORE, in consideration of the mutual covenants and promises
contained herein, the parties agree as follows:

Do not force recitals into documents where they are inappropriate.

============================================================
CLAUSE WRITING
============================================================

Write complete legal clauses.

Avoid short AI-style statements such as:

"The employee works full-time."

Instead write professional contractual language such as:

"The Employee shall be engaged on a full-time basis and shall perform
the duties assigned by the Employer in accordance with the terms of
this Agreement."

However, do not add obligations that were not supported by the user's
information.

============================================================
SUBCLAUSES
============================================================

Where appropriate, use:

(a)

(b)

(c)

For example:

Either party may terminate this Agreement:

(a) by mutual written agreement of the parties;

(b) upon material breach, subject to [NUMBER] days' written notice
and an opportunity to cure; or

(c) upon [NUMBER] days' prior written notice.

Only use such standard contractual structures when appropriate.

============================================================
SIGNATURE SECTION
============================================================

Always provide a professional signature section appropriate to the
identified parties.

Do not invent representative names.

If a company representative is required but the name is unknown, use:

[AUTHORIZED REPRESENTATIVE NAME]

[AUTHORIZED REPRESENTATIVE TITLE]

Do NOT use:

[NAME TO BE COMPLETED]

Use professional placeholders instead.

Example:

SERVICE PROVIDER

Jane Doe

Signature: ______________________________
Date: __________________________________


CLIENT

TechNova Inc.

By: ____________________________________
Name: [AUTHORIZED REPRESENTATIVE NAME]
Title: [AUTHORIZED REPRESENTATIVE TITLE]
Date: __________________________________

============================================================
EDITING
============================================================

The generated document should be clean and easy for the user to edit.

Do not include explanations outside the document.

Do not say:

"Here is your document."

Do not say:

"I have generated..."

Return only the document.

============================================================
MARKDOWN FORMAT
============================================================

Use simple Markdown headings because LegalEase converts the document
into TXT, DOCX and PDF.

Use:

# DOCUMENT TITLE

## Section Heading

### Subsection Heading

Normal paragraphs.

(a) Subclause.

(b) Subclause.

Do not use HTML.

Do not use code blocks.

Do not create Markdown tables.

============================================================
LEGALASE BRANDING
============================================================

At the beginning of the document include:

⚖️ LegalEase

Then the document title.

Do not overuse the logo throughout the document.

============================================================
FINAL NOTICE
============================================================

End the document with a short professional notice:

"LegalEase generates AI-assisted legal document templates. This document
is not legal advice and should be reviewed by a qualified legal
professional and adapted to the applicable jurisdiction before execution."

============================================================
FINAL OUTPUT RULE
============================================================

Return ONLY the complete legal document.

Do not provide commentary before or after the document.
"""


# ---------------------------------------------------------
# Generate legal document
# ---------------------------------------------------------

def generate_legal_document(
    document_type: str,
    parties: str,
    terms: str,
    effective_date: str,
    additional_information: str = "",
) -> str:

    document_type = document_type.strip()
    parties = parties.strip()
    terms = terms.strip()
    effective_date = effective_date.strip()
    additional_information = additional_information.strip()

    if not document_type:
        raise ValueError(
            "Document type is required."
        )

    if not parties:
        raise ValueError(
            "Party information is required."
        )

    if not terms:
        raise ValueError(
            "Terms and conditions are required."
        )

    prompt = f"""
Create a professionally structured legal document for LegalEase.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date if effective_date else "[EFFECTIVE DATE]"}

TERMS AND CONDITIONS:
{terms}

ADDITIONAL INFORMATION:
{additional_information if additional_information else "[ADDITIONAL INFORMATION]"}


============================================================
IMPORTANT CONTENT REQUIREMENTS
============================================================

Create a complete professional contract appropriate for the selected
document type.

The result must look like a real professionally prepared legal document.

Do not make it look like an AI-generated answer.

Do not write explanations about the document.

Do not write a summary.

Do not write "No information was provided."

Use professional placeholders when information is missing.

For example:

[CLIENT ADDRESS]

[SERVICE PROVIDER ADDRESS]

[JURISDICTION]

[STATE OF INCORPORATION]

[NUMBER] DAYS

[PAYMENT AMOUNT]

[COMPLETION DATE]

[AUTHORIZED REPRESENTATIVE NAME]

[AUTHORIZED REPRESENTATIVE TITLE]


============================================================
PROFESSIONAL OPENING
============================================================

Where appropriate, begin with:

⚖️ LegalEase

DOCUMENT TITLE

Agreement made this [DATE]

BETWEEN:

...

AND:

...

WITNESSETH:

WHEREAS...

NOW, THEREFORE...

Then continue with the numbered contractual clauses.


============================================================
CONTENT
============================================================

Include relevant provisions based on the document type.

For a freelance contract, relevant provisions may include:

1. Services
2. Term and Termination
3. Payment
4. Intellectual Property Rights
5. Confidentiality
6. Independent Contractor Status
7. Governing Law
8. Entire Agreement
9. Severability

For an employment agreement, relevant provisions may include:

1. Position and Duties
2. Employment Status
3. Compensation
4. Working Hours
5. Confidentiality
6. Term
7. Termination
8. Governing Law
9. Entire Agreement
10. Severability

Do not blindly copy these sections into every document.

Choose sections suitable for the selected document type.


============================================================
FACT PRESERVATION
============================================================

Every important user-provided fact must remain unchanged.

For example:

If the user says:

Salary: ₹30,000

the document must retain:

₹30,000

If the user says:

Effective date: 1 October 2026

the document must retain:

1 October 2026

If the user says:

Rahul Kumar

the document must retain:

Rahul Kumar


============================================================
MISSING INFORMATION
============================================================

Do not invent missing facts.

Instead insert a professional placeholder.

Example:

"The Client shall pay the Service Provider a total fee of
[PAYMENT AMOUNT] in accordance with the payment schedule set forth
herein."

Do not write:

"No payment information was provided."


============================================================
SIGNATURES
============================================================

End with:

IN WITNESS WHEREOF, the parties have executed this Agreement as of
the Effective Date.

Then provide appropriate signature blocks.

Use supplied names.

For missing authorized representatives, use:

[AUTHORIZED REPRESENTATIVE NAME]

[AUTHORIZED REPRESENTATIVE TITLE]


============================================================
FINAL DISCLAIMER
============================================================

End with:

LegalEase generates AI-assisted legal document templates. This document
is not legal advice and should be reviewed by a qualified legal
professional and adapted to the applicable jurisdiction before execution.


============================================================
OUTPUT
============================================================

Return ONLY the complete document.
"""

    max_attempts = 4

    retry_delays = [
        2,
        5,
        10,
        20,
    ]

    last_error = None

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    max_output_tokens=6000,
                ),
            )

            generated_text = getattr(
                response,
                "text",
                None,
            )

            if not generated_text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            generated_text = generated_text.strip()

            if not generated_text:
                raise RuntimeError(
                    "Gemini returned an empty document."
                )

            return generated_text

        except Exception as exc:

            last_error = exc

            error_message = str(exc).upper()

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):

                if attempt < max_attempts - 1:

                    time.sleep(
                        retry_delays[attempt]
                    )

                    continue

            raise RuntimeError(
                f"Gemini API request failed: {exc}"
            ) from exc

    raise RuntimeError(
        "Gemini API request failed after "
        f"{max_attempts} attempts: {last_error}"
    )