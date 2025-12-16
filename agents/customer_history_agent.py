from adk.agent import Agent
from data_models.transaction_models import Transaction, AnalysisResult


class CustomerHistoryAgent(Agent):
    """
    An agent that analyzes a transaction based on the customer's history.
    """
    def __init__(self):
        super().__init__()
        self.name = "CustomerHistoryAgent"

    def run(self, transaction: Transaction) -> AnalysisResult:
        """
        Analyzes a single transaction against the customer's (mock) history.

        A real agent would connect to a database to fetch customer data.
        """
        # Mock customer data. In a real scenario, this would be retrieved
        # from a database or another service.
        mock_payer_data = {
            "payer_12345": {"risk_level": "low", "average_transaction": 75.00},
            "payer_67890": {"risk_level": "high", "average_transaction": 1500.00},
        }

        payer_id = transaction.payer_id
        if payer_id in mock_payer_data:
            payer_profile = mock_payer_data[payer_id]

            # Example rule: If payer risk level is high, flag for review.
            if payer_profile["risk_level"] == "high":
                return AnalysisResult(
                    agent_name=self.name,
                    decision="Review",
                    reason=f"Payer '{payer_id}' has a high-risk profile.",
                    confidence_score=0.9
                )

            # Example rule: If transaction is much higher than average, flag it.
            if transaction.payment_amount > (payer_profile["average_transaction"] * 5):
                return AnalysisResult(
                    agent_name=self.name,
                    decision="Review",
                    reason=f"Transaction amount is significantly higher than payer's average.",
                    confidence_score=0.8
                )

        return AnalysisResult(
            agent_name=self.name,
            decision="Approve",
            reason="Transaction is consistent with customer history.",
            confidence_score=0.95
        )
