"""
VertexAI configuration and client initialization for Tri-Netra.
This module handles the setup for using VertexAI instead of direct Gemini API.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger('google_adk.' + __name__)


def setup_vertexai_client():
    """
    Sets up and returns a VertexAI client if configured to use VertexAI.
    Otherwise returns None to use default Gemini API client.
    """
    use_vertexai = os.getenv('GOOGLE_GENAI_USE_VERTEXAI', '').lower() == 'true'

    if not use_vertexai:
        logger.info("Using Gemini API (not VertexAI)")
        return None

    logger.info("Configuring VertexAI client...")

    # Get required configuration
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')

    if not project_id:
        logger.error("GOOGLE_CLOUD_PROJECT not set. Cannot use VertexAI.")
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT must be set when GOOGLE_GENAI_USE_VERTEXAI=True"
        )

    try:
        # Import VertexAI
        from google.cloud import aiplatform

        # Initialize VertexAI
        aiplatform.init(
            project=project_id,
            location=location
        )

        logger.info(f"VertexAI initialized: project={project_id}, location={location}")
        return {
            'project': project_id,
            'location': location,
            'use_vertexai': True
        }

    except ImportError:
        logger.error("google-cloud-aiplatform not installed. Install with: pip install google-cloud-aiplatform")
        raise
    except Exception as e:
        logger.error(f"Failed to initialize VertexAI: {e}")
        raise


def get_model_name() -> str:
    """
    Get the configured model name.
    When using VertexAI, model names may need to be formatted differently.
    """
    model = os.getenv('TRI_NETRA_MODEL', 'gemini-2.0-flash-exp')
    use_vertexai = os.getenv('GOOGLE_GENAI_USE_VERTEXAI', '').lower() == 'true'

    if use_vertexai:
        # VertexAI model names - ensure proper format
        # gemini-2.0-flash-exp is available in VertexAI
        logger.info(f"Using VertexAI model: {model}")
        return model
    else:
        logger.info(f"Using Gemini API model: {model}")
        return model


def get_client_config() -> dict:
    """
    Returns configuration dictionary for initializing the genai client.
    """
    use_vertexai = os.getenv('GOOGLE_GENAI_USE_VERTEXAI', '').lower() == 'true'

    if use_vertexai:
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')

        if not project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT must be set when GOOGLE_GENAI_USE_VERTEXAI=True"
            )

        return {
            'vertexai': True,
            'project': project_id,
            'location': location
        }
    else:
        api_key = os.getenv('GOOGLE_API_KEY')

        if not api_key:
            logger.warning("GOOGLE_API_KEY not set. API calls may fail.")

        return {
            'vertexai': False,
            'api_key': api_key
        }


# Initialize on module load
try:
    VERTEXAI_CONFIG = setup_vertexai_client()
    MODEL_NAME = get_model_name()
    logger.info("VertexAI configuration loaded successfully")
except Exception as e:
    logger.warning(f"VertexAI configuration failed: {e}")
    VERTEXAI_CONFIG = None
    MODEL_NAME = os.getenv('TRI_NETRA_MODEL', 'gemini-2.0-flash-exp')
