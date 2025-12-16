# Tri-Netra Agent

Tri-Netra is a multi-agent system designed to analyze financial transactions for risk and compliance. It uses an orchestrator agent to manage a workflow where a transaction is simultaneously analyzed by three specialized agents. The final results are consolidated and presented for human review.

This project is built using the Google Agent Development Kit (ADK).

## Project Structure

- `main.py`: The main entry point to run the agent and process sample transactions.
- `requirements.txt`: A list of the Python dependencies for this project.
- `agents/`: This directory contains all the agents.
  - `__init__.py`: Makes the `agents` directory a Python package.
  - `orchestrator_agent.py`: The main "Tri-Netra" agent that orchestrates the workflow.
  - `fraud_detection_agent.py`: An agent that analyzes transactions for common fraud patterns.
  - `rule_check_agent.py`: An agent that checks transactions against a set of hard-coded business rules.
  - `customer_history_agent.py`: An agent that analyzes transactions in the context of the customer's past behavior.
- `data_models/`: This directory contains the Pydantic data models used by the agents.
  - `__init__.py`: Makes the `data_models` directory a Python package.
  - `transaction_models.py`: Defines the `Transaction` and `AnalysisResult` data structures.

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the agent:**
    ```bash
    python main.py
    ```
    This will run the `TriNetraOrchestratorAgent` with a set of sample transactions and print the analysis for each to the console.

## Ideas for Future Improvement

Here are a few ideas for extending the capabilities of the Tri-Netra agent:

- **Sophisticated Synthesis Logic:** The current orchestrator uses a simple "most severe outcome wins" logic to determine the final decision. This could be improved by:
  - Using a weighted voting system based on the confidence scores from each agent.
  - Implementing a dedicated "Checker" or "Meta" agent that reviews the outputs of the analysis agents to make a more nuanced final decision.

- **Stateful Agents:** The `CustomerHistoryAgent` and `RuleCheckAgent` are currently stateless. They could be made stateful to track customer behavior over time or to enforce more complex rules (e.g., transaction frequency limits).

- **Human-in-the-Loop:** The final output is currently printed to the console. This could be integrated with a human review system:
  - Create a simple web interface (using Flask or FastAPI) to display pending reviews.
  - Push notifications to a messaging platform like Slack.
  - Create tickets in a project management tool like Jira.

- **Configuration-Driven Rules:** The rules in the analysis agents are currently hard-coded. These could be moved to a configuration file (`config/rules.yaml`) to allow for easier updates without changing the agent's code.

- **LLM-Powered Analysis:** The agents currently use simple, deterministic logic. They could be enhanced to call out to Large Language Models (LLMs) for more sophisticated, context-aware analysis. For example, the `FraudDetectionAgent` could use an LLM to analyze the merchant name for signs of being a shell company.
