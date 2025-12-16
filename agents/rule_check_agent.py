from adk.agent import Agent
from data_models.transaction_models import Transaction, AnalysisResult
import datetime


class RuleCheckAgent(Agent):
    """
    An agent that checks a transaction against a set of hard-coded business rules.
    """
    def __init__(self):
        super().__init__()
        self.name = "RuleCheckAgent"

    def run(self, transaction: Transaction) -> AnalysisResult:
        """
        Analyzes a single transaction against business rules.
        """
        # Example rule: No transactions allowed between midnight and 5 AM.
        # Example rule: No transactions allowed between midnight and 5 AM.
        transaction_time = transaction.payment_time.time()
        if datetime.time(0, 0) <= transaction_time <= datetime.time(5, 0):
            return AnalysisResult(
                agent_name=self.name,
                decision="Review",
                reason=f"Transaction occurred during off-hours at {transaction_time}.",
                confidence_score=0.85
            )

        # Example rule: Limit on transaction frequency (this would require state).
        # For this example, we'll just approve if the time rule doesn't trigger.
        return AnalysisResult(
            agent_name=self.name,
            decision="Approve",
            reason="Transaction complies with business rules.",
            confidence_score=0.99
        )
