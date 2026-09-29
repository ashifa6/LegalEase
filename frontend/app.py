import os

import requests
import streamlit as st
from dotenv import load_dotenv

from utils.document_formatter import create_docx
from utils.pdf_generator import create_pdf
from utils.text_utils import (
    create_safe_filename,
    create_txt_document,
)


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "generated_document" not in st.session_state:
    st.session_state["generated_document"] = ""

if "editing" not in st.session_state:
    st.session_state["editing"] = False


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 0;
        }

        .subtitle {
            font-size: 18px;
            margin-top: 0;
            opacity: 0.75;
        }

        .document-container {
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(128, 128, 128, 0.25);
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# LegalEase Header
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Professional AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Create Document Section
# ---------------------------------------------------------

st.header("Create a Legal Document")


document_type = st.selectbox(
    "Document Type",
    [
        "Employment Agreement",
        "Freelance Work Contract",
        "Non-Disclosure Agreement",
        "Service Agreement",
        "Rental Agreement",
        "Partnership Agreement",
        "Sale Agreement",
        "General Legal Agreement",
        "Other",
    ],
)


# ---------------------------------------------------------
# Custom document type
# ---------------------------------------------------------

if document_type == "Other":

    custom_document_type = st.text_input(
        "Enter Document Type",
        placeholder="Example: Consulting Agreement",
    )

    if custom_document_type.strip():

        document_type = custom_document_type.strip()


# ---------------------------------------------------------
# Parties
# ---------------------------------------------------------

parties = st.text_area(
    "Parties",
    placeholder=(
        "Example:\n"
        "Jane Doe (Service Provider)\n"
        "TechNova Inc. (Client)"
    ),
    height=130,
)


# ---------------------------------------------------------
# Terms and Conditions
# ---------------------------------------------------------

terms = st.text_area(
    "Terms and Conditions",
    placeholder=(
        "Describe the important terms.\n\n"
        "Example:\n"
        "- Development of a mobile application\n"
        "- Payment of ₹50,000\n"
        "- Confidentiality must be maintained\n"
        "- Either party may terminate with 15 days notice"
    ),
    height=220,
)


# ---------------------------------------------------------
# Effective Date
# ---------------------------------------------------------

effective_date = st.text_input(
    "Effective Date",
    placeholder="Example: 15 April 2025",
)


# ---------------------------------------------------------
# Additional Information
# ---------------------------------------------------------

additional_information = st.text_area(
    "Additional Information (Optional)",
    placeholder=(
        "Add addresses, deliverables, payment details, "
        "representative information, jurisdiction, or "
        "other requirements."
    ),
    height=150,
)


# ---------------------------------------------------------
# Generate Document Button
# ---------------------------------------------------------

generate_button = st.button(
    "Generate Legal Document",
    type="primary",
    use_container_width=True,
)


if generate_button:

    if not parties.strip():

        st.error(
            "Please enter the parties."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date,
            "additional_information": additional_information,
        }

        with st.spinner(
            "Preparing your professional legal document..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/api/generate",
                    json=payload,
                    timeout=120,
                )

                if response.status_code == 200:

                    data = response.json()

                    if data.get("success"):

                        st.session_state[
                            "generated_document"
                        ] = data["document"]

                        st.session_state[
                            "editing"
                        ] = False

                        st.success(
                            "Professional legal document generated successfully."
                        )

                    else:

                        st.error(
                            "The backend did not return "
                            "a successful response."
                        )

                else:

                    try:

                        error_data = response.json()

                        detail = error_data.get(
                            "detail",
                            "Unknown backend error.",
                        )

                    except ValueError:

                        detail = response.text

                    st.error(
                        f"Backend error "
                        f"({response.status_code}): {detail}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the LegalEase backend. "
                    "Make sure FastAPI is running on port 8000."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. Please try again."
                )

            except requests.exceptions.RequestException as exc:

                st.error(
                    f"Request failed: {exc}"
                )


# ---------------------------------------------------------
# Generated Document
# ---------------------------------------------------------

if st.session_state["generated_document"]:

    st.divider()

    st.header("Generated Document")


    # =====================================================
    # VIEW MODE
    # =====================================================

    if not st.session_state["editing"]:

        st.text_area(
            "Generated Legal Document",
            value=st.session_state[
                "generated_document"
            ],
            height=700,
            disabled=True,
        )

        st.write("")


        # -------------------------------------------------
        # Edit / Generate New buttons
        # -------------------------------------------------

        edit_col, regenerate_col = st.columns(2)


        # -------------------------------------------------
        # EDIT DOCUMENT
        # -------------------------------------------------

        with edit_col:

            if st.button(
                "✏️ Edit Document",
                use_container_width=True,
            ):

                st.session_state[
                    "editing"
                ] = True

                st.rerun()


        # -------------------------------------------------
        # GENERATE NEW DOCUMENT
        # -------------------------------------------------

        with regenerate_col:

            if st.button(
                "🔄 Generate New Document",
                use_container_width=True,
            ):

                st.session_state[
                    "generated_document"
                ] = ""

                st.session_state[
                    "editing"
                ] = False

                st.rerun()


    # =====================================================
    # EDIT MODE
    # =====================================================

    else:

        st.info(
            "You are editing the document. "
            "Make your changes and click Save Changes."
        )


        edited_document = st.text_area(
            "Edit Legal Document",
            value=st.session_state[
                "generated_document"
            ],
            height=700,
        )

        st.write("")


        save_col, cancel_col = st.columns(2)


        # -------------------------------------------------
        # SAVE CHANGES
        # -------------------------------------------------

        with save_col:

            if st.button(
                "💾 Save Changes",
                type="primary",
                use_container_width=True,
            ):

                st.session_state[
                    "generated_document"
                ] = edited_document

                st.session_state[
                    "editing"
                ] = False

                st.success(
                    "Changes saved successfully."
                )

                st.rerun()


        # -------------------------------------------------
        # CANCEL EDITING
        # -------------------------------------------------

        with cancel_col:

            if st.button(
                "✖ Cancel",
                use_container_width=True,
            ):

                st.session_state[
                    "editing"
                ] = False

                st.rerun()


    # =====================================================
    # DOWNLOAD SECTION
    # =====================================================

    st.divider()

    st.subheader(
        "Download Your Legal Document"
    )


    # -----------------------------------------------------
    # Always use latest saved document
    # -----------------------------------------------------

    final_document = st.session_state[
        "generated_document"
    ]


    # -----------------------------------------------------
    # Safe filename
    # -----------------------------------------------------

    filename = create_safe_filename(
        document_type,
        default="legal_document",
    )


    # -----------------------------------------------------
    # TXT
    # -----------------------------------------------------

    formatted_txt = create_txt_document(
        final_document
    )

    txt_bytes = formatted_txt.encode(
        "utf-8"
    )


    # -----------------------------------------------------
    # DOCX
    # -----------------------------------------------------

    docx_bytes = create_docx(
        final_document
    )


    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    pdf_bytes = create_pdf(
        final_document
    )


    # -----------------------------------------------------
    # Download buttons
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)


    # TXT
    with col1:

        st.download_button(
            label="⬇️ Download TXT",
            data=txt_bytes,
            file_name=f"{filename}.txt",
            mime="text/plain",
            use_container_width=True,
        )


    # DOCX
    with col2:

        st.download_button(
            label="⬇️ Download DOCX",
            data=docx_bytes,
            file_name=f"{filename}.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )


    # PDF
    with col3:

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_bytes,
            file_name=f"{filename}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "LegalEase — Professional AI-Powered Legal Document Generator"
)

st.caption(
    "AI-assisted documents require appropriate human "
    "and legal review before use."
)