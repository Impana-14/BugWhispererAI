
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.genai import errors as gemini_errors
from pydantic import ValidationError

from app.agent import analyze_bug
from app.config import APP_NAME, APP_VERSION
from app.schemas import BugAnalysisRequest, BugAnalysisResponse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="An AI-powered assistant for analyzing and debugging code.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to BugWhisperer AI!",
        "docs": "/docs",
    }


@app.get("/api/health/")
def health_check():
    return {
        "status": "ok",
        "app": APP_NAME,
        "version": APP_VERSION,
    }


@app.post("/api/analyze/", response_model=BugAnalysisResponse)
def analyze(request: BugAnalysisRequest):
    try:
        return analyze_bug(request)

    except RuntimeError as exc:
        if "GEMINI_API_KEY is missing" in str(exc):
            raise HTTPException(
                status_code=503,
                detail="Gemini API key is not configured. Check your .env file.",
            ) from exc

        logger.exception("Unexpected error during bug analysis")
        raise HTTPException(
            status_code=502,
            detail="Bug analysis could not be completed.",
        ) from exc

    except gemini_errors.APIError as exc:
        logger.exception("Gemini API request failed")

        if exc.code == 503:
            status_code = 503
            detail = "Gemini is temporarily unavailable. Please try again later."
        elif exc.code == 429:
            status_code = 429
            detail = "Gemini request limit reached. Please try again later."
        else:
            status_code = 502
            detail = "The Gemini request failed. Check the server logs."

        raise HTTPException(
            status_code=status_code,
            detail=detail,
        ) from exc

    except ValidationError as exc:
        logger.exception("The AI response did not match the expected schema")
        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid bug report. Please try again.",
        ) from exc
