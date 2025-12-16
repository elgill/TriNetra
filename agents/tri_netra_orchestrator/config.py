import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('google_adk.' + __name__)

# Configuration for Tri-Netra orchestrator

# Google Cloud configuration
USE_VERTEXAI = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "False").lower() == "true"
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

# Fraud detection thresholds
FRAUD_AMOUNT_THRESHOLD = float(os.environ.get("FRAUD_AMOUNT_THRESHOLD", "10000.0"))
HIGH_RISK_COUNTRIES = os.environ.get("HIGH_RISK_COUNTRIES", "").split(",")

# Rule engine configuration
BUSINESS_RULES_ENABLED = os.environ.get("BUSINESS_RULES_ENABLED", "true").lower() == "true"

# Model configuration
DEFAULT_MODEL = os.environ.get("TRI_NETRA_MODEL", "gemini-2.0-flash-exp")
ANALYSIS_MODEL = os.environ.get("ANALYSIS_MODEL", "gemini-2.0-flash-exp")

# Log configuration mode
if USE_VERTEXAI:
    logger.info(f"Using VertexAI with project={GOOGLE_CLOUD_PROJECT}, location={GOOGLE_CLOUD_LOCATION}")
    if not GOOGLE_CLOUD_PROJECT:
        logger.error("GOOGLE_CLOUD_PROJECT must be set when using VertexAI")
else:
    logger.info("Using Gemini API (API key required)")

logger.info("Tri-Netra configuration loaded successfully")
