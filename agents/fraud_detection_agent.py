from adk.agent import Agent
from adk.prompt import Prompt
from data_models.transaction_models import Transaction, AnalysisResult


class FraudDetectionAgent(Agent):
    """
    An agent that analyzes a transaction for potential fraud.
    """
    def __init__(self):
        super().__init__()
        self.name = "FraudDetectionAgent"

    def run(self, transaction: Transaction) -> AnalysisResult:
        """
        Analyzes a single transaction for fraudulent patterns.

        This is a simple implementation. A real-world agent would use a more
        sophisticated model or rule set.
        """
        # Example rule: flag transactions over $1000 as needing review.
        if transaction.payment_amount > 1000:
            return AnalysisResult(
                agent_name=self.name,
                decision="Review",
                reason=f"Transaction amount of {transaction.payment_amount} {transaction.payment_currency} exceeds the $1000 threshold.",
                confidence_score=0.9
            )

        # Example rule: flag transactions from certain vendors.
        if "risky-vendor" in transaction.vendor_id.lower():
            return AnalysisResult(
                agent_name=self.name,
                decision="Reject",
                reason=f"Transaction is from a known risky vendor: {transaction.vendor_id}.",
                confidence_score=0.95
            )

        return AnalysisResult(
            agent_name=self.name,
            decision="Approve",
            reason="No fraudulent patterns detected.",
            confidence_score=0.98
        )
