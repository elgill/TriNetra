# Tri-Netra Transaction Analysis Orchestrator

An AI-powered transaction analysis system built using the Google ADK (Agent Development Kit) parallel task decomposition pattern.

## Overview

Tri-Netra ("three-eyed" in Sanskrit) is a comprehensive transaction analysis system that evaluates financial transactions across multiple dimensions simultaneously. It uses parallel agent execution to provide fast, thorough analysis and intelligent recommendations for human review.

## Architecture

The system follows the **Parallel Task Decomposition** design pattern from Google ADK:

```
┌─────────────────────────────────────────────────────────────┐
│                   Tri-Netra Root Agent                       │
│              (Transaction Orchestrator)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            Transaction Analysis Flow (Sequential)            │
├─────────────────────────────────────────────────────────────┤
│  1. Transaction Validator                                   │
│     ├─ Validates data completeness                          │
│     └─ Prepares data for analysis                           │
│                                                              │
│  2. Parallel Analysis Agent                                 │
│     ├─ Fraud Detection Agent ──────────┐                    │
│     ├─ Rule Compliance Agent ──────────┤ (Run in Parallel) │
│     ├─ Customer History Agent ─────────┤                    │
│     └─ Anomaly Detection Agent ────────┘                    │
│                                                              │
│  3. Summary Agent                                           │
│     ├─ Aggregates all results                               │
│     ├─ Makes final recommendation                           │
│     └─ Prepares human review report                         │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Human Review Queue                         │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Analysis Agents (Parallel Execution)

#### Fraud Detection Agent
- **Purpose**: Identifies fraudulent patterns and suspicious activity
- **Analyzes**:
  - Unusual transaction amounts
  - Suspicious vendor patterns
  - Geographic inconsistencies
  - Payment method risks
- **Output**: Fraud risk assessment with decision and confidence score

#### Rule Compliance Agent
- **Purpose**: Verifies business rules and regulatory compliance
- **Checks**:
  - Transaction timing restrictions
  - Amount limits
  - Vendor allow/block lists
  - Jurisdiction compliance
- **Output**: Compliance status with specific rule violations (if any)

#### Customer History Agent
- **Purpose**: Analyzes transaction against customer behavior
- **Evaluates**:
  - Historical transaction patterns
  - Customer risk profile
  - Deviations from normal behavior
  - Account age and activity
- **Output**: Behavioral consistency assessment

#### Anomaly Detection Agent
- **Purpose**: Detects statistical anomalies and unusual patterns
- **Detects**:
  - Statistical outliers
  - Unusual attribute combinations
  - Timing anomalies
  - Payment method irregularities
- **Output**: Anomaly report with significance levels

### 2. Orchestration Agents

#### Transaction Validator
- Validates incoming transaction data
- Ensures all required fields are present
- Formats data for analysis agents

#### Summary Agent
- Aggregates results from all parallel agents
- Applies decision logic:
  - **Reject**: If ANY agent recommends rejection
  - **Review**: If ANY agent flags for review (and none reject)
  - **Approve**: Only if ALL agents approve
- Generates comprehensive human-readable report

#### Root Orchestrator
- Main entry point for the system
- Manages overall workflow
- Presents final results and recommendations

## Decision Logic

The system uses a conservative approach to decision-making:

1. **Reject** - Transaction should be blocked
   - Triggered if any agent detects clear fraud indicators or rule violations

2. **Review** - Human review required
   - Triggered if any agent has concerns but not clear rejection criteria
   - Used for edge cases and ambiguous situations

3. **Approve** - Transaction can proceed
   - Only triggered if ALL agents approve with high confidence

## Tools and Integrations

### Current Tools (Mock Implementation)

All tools are currently implemented as mock functions returning dummy data. In production, these would be replaced with actual integrations:

- `analyze_fraud_risk()` → Fraud detection service/ML model
- `check_compliance_rules()` → Rule engine/compliance platform
- `analyze_customer_history()` → Customer database/CRM
- `detect_anomalies()` → Anomaly detection ML model
- `submit_for_human_review()` → Review queue system

### Future Integrations

- Database connections for customer history
- ML model endpoints for fraud/anomaly detection
- External API calls for compliance checks
- Review queue management system
- Notification services for alerts

## Usage

### Basic Usage

```python
import asyncio
from google.adk.agents import run_agent
from agents.tri_netra_orchestrator import tri_netra_root_agent
from data_models.transaction_models import Transaction

async def analyze_transaction(transaction: Transaction):
    transaction_data = transaction.model_dump()

    prompt = f"Please analyze transaction {transaction.transaction_id}"

    result = await run_agent(
        agent=tri_netra_root_agent,
        prompt=prompt,
        session_state={"transaction_data": transaction_data}
    )

    return result

# Run the analysis
asyncio.run(analyze_transaction(my_transaction))
```

### Example Script

See `example_usage.py` for complete examples including:
- Single transaction analysis
- Batch transaction processing
- Error handling patterns

## Configuration

Configuration is managed through environment variables in `config.py`:

```bash
# Fraud detection thresholds
FRAUD_AMOUNT_THRESHOLD=10000.0
HIGH_RISK_COUNTRIES=XX,YY,ZZ

# Business rules
BUSINESS_RULES_ENABLED=true

# Model configuration
TRI_NETRA_MODEL=gemini-2.0-flash-exp
ANALYSIS_MODEL=gemini-2.0-flash-exp
```

## Development Roadmap

### Phase 1: Core Orchestrator (Current - COMPLETE)
- ✅ Parallel agent architecture
- ✅ Mock tool implementations
- ✅ Prompt engineering for all agents
- ✅ Basic decision logic

### Phase 2: Sub-Agent Implementation (Next)
- [ ] Replace mock tools with real implementations
- [ ] Integrate with actual fraud detection models
- [ ] Connect to customer database
- [ ] Implement rule engine
- [ ] Add anomaly detection ML model

### Phase 3: Human Review Integration
- [ ] Build review queue UI
- [ ] Add reviewer assignment logic
- [ ] Implement feedback loop
- [ ] Create audit trail system

### Phase 4: Production Hardening
- [ ] Add comprehensive error handling
- [ ] Implement rate limiting
- [ ] Add monitoring and alerting
- [ ] Create performance benchmarks
- [ ] Add comprehensive testing

## Key Features

1. **Parallel Processing**: All analysis agents run simultaneously for maximum speed
2. **Comprehensive Analysis**: Multi-dimensional risk assessment
3. **Explainable Decisions**: Clear reasoning for all recommendations
4. **Conservative Approach**: Errs on the side of caution with human review
5. **Extensible Architecture**: Easy to add new analysis agents
6. **Production-Ready Structure**: Based on Google ADK best practices

## Advantages Over Traditional Approaches

1. **Speed**: Parallel execution vs sequential analysis
2. **Thoroughness**: Multiple specialized agents vs single model
3. **Explainability**: Clear agent-specific reasoning vs black-box
4. **Flexibility**: Easy to add/remove/modify agents
5. **Scalability**: Cloud-native architecture with ADK

## Contributing

When adding new analysis agents:

1. Create agent definition in `agent.py`
2. Add instruction prompt in `prompts/prompts.py`
3. Implement tools in `tools.py`
4. Update the parallel_analysis_agent sub_agents list
5. Update this README

## License

[Your License Here]

## Contact

[Your Contact Information]
