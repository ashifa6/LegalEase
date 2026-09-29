# LegalEase

## AI-Powered Legal Document Generator

LegalEase is a generative-AI-based application that creates structured
legal document drafts from user-provided information.

## Features

- AI-powered legal document generation
- Document type selection
- Party information
- Terms and conditions
- Effective date
- Additional information
- Editable generated document
- TXT download
- DOCX download
- PDF download
- FastAPI backend
- Streamlit frontend
- Google Gemini integration

## Technology Stack

- Python
- Streamlit
- FastAPI
- Google Gemini API
- Google GenAI Python SDK
- python-docx
- fpdf2
- Requests
- python-dotenv

## Project Structure

```text
LegalEase/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── routes.py
│
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
│
├── frontend/
│   └── app.py
│
├── utils/
│   ├── __init__.py
│   ├── document_formatter.py
│   ├── pdf_generator.py
│   └── text_utils.py
│
├── assets/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md