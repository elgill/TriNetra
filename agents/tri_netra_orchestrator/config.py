import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('google_adk.' + __name__)

# Configuration for Tri-Netra orchestrator

# Fraud detection thresholds
FRAUD_AMOUNT_THRESHOLD = float(os.environ.get("FRAUD_AMOUNT_THRESHOLD", "10000.0"))
HIGH_RISK_COUNTRIES = os.environ.get("HIGH_RISK_COUNTRIES", "").split(",")

# Rule engine configuration
BUSINESS_RULES_ENABLED = os.environ.get("BUSINESS_RULES_ENABLED", "true").lower() == "true"

# Model configuration
DEFAULT_MODEL = os.environ.get("TRI_NETRA_MODEL", "gemini-2.0-flash-exp")
ANALYSIS_MODEL = os.environ.get("ANALYSIS_MODEL", "gemini-2.0-flash-exp")

logger.info("Tri-Netra configuration loaded successfully")
