import logging
from google.adk.agents import LlmAgent, SequentialAgent, Agent, ParallelAgent
from .tools import (
    analyze_fraud_risk,
    check_compliance_rules,
    analyze_customer_history,
    detect_anomalies,
    submit_for_human_review,
)
from .prompts.prompts import (
    FRAUD_DETECTION_INSTRUCTION,
    RULE_COMPLIANCE_INSTRUCTION,
    CUSTOMER_HISTORY_INSTRUCTION,
    ANOMALY_DETECTION_INSTRUCTION,
    SUMMARY_AGENT_INSTRUCTION,
    ROOT_AGENT_INSTRUCTION,
    TRANSACTION_VALIDATOR_INSTRUCTION,
)

logger = logging.getLogger('google_adk.' + __name__)

# -------------------------
# Parallel Analysis Agents
# -------------------------

# Fraud Detection Agent - Analyzes for fraudulent patterns
fraud_detection_agent = Agent(
    name="fraud_detection_agent",
    description="Analyzes transaction for potential fraud and suspicious activity.",
    model="gemini-2.0-flash-exp",
    instruction=FRAUD_DETECTION_INSTRUCTION,
    output_key="fraud_analysis_result",
    tools=[analyze_fraud_risk]
)

# Rule Compliance Agent - Checks business rules and compliance
rule_compliance_agent = Agent(
    name="rule_compliance_agent",
    description="Verifies transaction compliance with business rules and regulations.",
    model="gemini-2.0-flash-exp",
    instruction=RULE_COMPLIANCE_INSTRUCTION,
    output_key="compliance_analysis_result",
    tools=[check_compliance_rules]
)

# Customer History Agent - Analyzes customer behavior patterns
customer_history_agent = Agent(
    name="customer_history_agent",
    description="Analyzes transaction against customer's historical behavior.",
    model="gemini-2.0-flash-exp",
    instruction=CUSTOMER_HISTORY_INSTRUCTION,
    output_key="history_analysis_result",
    tools=[analyze_customer_history]
)

# Anomaly Detection Agent - Detects statistical anomalies
anomaly_detection_agent = Agent(
    name="anomaly_detection_agent",
    description="Detects unusual patterns and anomalies in transaction data.",
    model="gemini-2.0-flash-exp",
    instruction=ANOMALY_DETECTION_INSTRUCTION,
    output_key="anomaly_analysis_result",
    tools=[detect_anomalies]
)

# -------------------------
# Parallel Agent Coordinator
# -------------------------

parallel_analysis_agent = ParallelAgent(
    name="parallel_analysis_agent",
    description="Executes all transaction analysis agents simultaneously for comprehensive risk assessment.",
    sub_agents=[
        fraud_detection_agent,
        rule_compliance_agent,
        customer_history_agent,
        anomaly_detection_agent
    ]
)

# -------------------------
# Summary and Aggregation Agent
# -------------------------

summary_agent = LlmAgent(
    name="summary_agent",
    model="gemini-2.0-flash-exp",
    instruction=SUMMARY_AGENT_INSTRUCTION,
    description="Aggregates results from all analysis agents and makes final recommendation.",
)

# -------------------------
# Main Transaction Analysis Flow
# -------------------------

transaction_analysis_flow = SequentialAgent(
    name="transaction_analysis_flow",
    description="Handles the main flow of transaction validation, parallel analysis, and summary generation.",
    sub_agents=[
        Agent(
            name="transaction_validator",
            description="Validates and prepares transaction data for analysis.",
            model="gemini-2.0-flash-exp",
            instruction=TRANSACTION_VALIDATOR_INSTRUCTION,
            output_key="validated_transaction"
        ),
        parallel_analysis_agent,
        summary_agent
    ]
)

# -------------------------
# Root Orchestrator Agent
# -------------------------

tri_netra_root_agent = Agent(
    name="tri_netra_orchestrator",
    description="Tri-Netra: AI-powered transaction analysis system for fraud detection and risk assessment.",
    model="gemini-2.0-flash-exp",
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[
        transaction_analysis_flow
    ],
    tools=[submit_for_human_review]
)

logger.info("Tri-Netra orchestrator agent initialized successfully")
