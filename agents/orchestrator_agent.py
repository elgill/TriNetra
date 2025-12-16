from typing import List
from adk.agent import Agent
from adk.parallel import parallel
from data_models.transaction_models import Transaction, AnalysisResult



class TriNetraOrchestratorAgent(Agent):
    """
    The main orchestrator agent that analyzes a transaction by delegating
    to a set of parallel analysis agents.
    """
    def __init__(self):
        super().__init__()
        # Instantiate the analysis agents
        self.analysis_agents = [
        ]

    def run(self, transaction: Transaction):
        """
        Orchestrates the parallel analysis of a transaction and prints a
        consolidated report for human review.
        """
        print(f"[*] Starting analysis for transaction: {transaction.transaction_id}")

        # Run all analysis agents in parallel
        results: List[AnalysisResult] = parallel(
            lambda agent: agent.run(transaction),
            self.analysis_agents
        )

        print(f"\n[+] Analysis complete for transaction: {transaction.transaction_id}")
        self.present_for_human_review(transaction, results)

    def present_for_human_review(self, transaction: Transaction, results: List[AnalysisResult]):
        """Formats and prints the results for a human reviewer."""
        print("\n--- Human Review Required ---")
        print(f"Transaction ID: {transaction.transaction_id}")
        print(f"Amount: {transaction.amount} {transaction.currency}")
        print(f"Customer: {transaction.customer_id}")
        print(f"Merchant: {transaction.merchant}")
        print("-" * 20)
        print("Agent Analysis:")

        final_decision = "Approve"
        for res in results:
            print(f"  - Agent: {res.agent_name}")
            print(f"    Decision: {res.decision} (Confidence: {res.confidence_score:.2f})")
            print(f"    Reason: {res.reason}")

            # Determine the final decision based on the most severe outcome.
            if res.decision == "Reject":
                final_decision = "Reject"
            elif res.decision == "Review" and final_decision != "Reject":
                final_decision = "Review"

        print("-" * 20)
        print(f"Suggested Final Decision: {final_decision}")
        print("--- End of Report ---\n")
