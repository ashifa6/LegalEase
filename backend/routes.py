from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import generate_legal_document


router = APIRouter(
    prefix="/api",
    tags=["Legal Document Generator"],
)


class GenerateDocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=200)
    parties: str = Field(..., min_length=2, max_length=2000)
    terms: str = Field(..., min_length=2, max_length=10000)
    effective_date: str = Field(default="", max_length=200)
    additional_information: str = Field(default="", max_length=10000)


class GenerateDocumentResponse(BaseModel):
    success: bool
    document: str


@router.get("/health")
def health_check():
    return {
        "success": True,
        "message": "LegalEase API is running.",
    }


@router.post(
    "/generate",
    response_model=GenerateDocumentResponse,
)
def generate_document(request: GenerateDocumentRequest):
    try:
        document = generate_legal_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            additional_information=request.additional_information,
        )

        return GenerateDocumentResponse(
            success=True,
            document=document,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected server error: {exc}",
        ) from exc