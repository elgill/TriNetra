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


# Log configuration mode
if USE_VERTEXAI:
    logger.info(f"Using VertexAI with project={GOOGLE_CLOUD_PROJECT}, location={GOOGLE_CLOUD_LOCATION}")
    if not GOOGLE_CLOUD_PROJECT:
        logger.error("GOOGLE_CLOUD_PROJECT must be set when using VertexAI")
else:
    logger.info("Using Gemini API (API key required)")

logger.info("Tri-Netra configuration loaded successfully")
