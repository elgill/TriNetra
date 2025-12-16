import datetime
from data_models.transaction_models import Transaction
from agents.orchestrator_agent import TriNetraOrchestratorAgent


def main():
    """
    Main function to run the Tri-Netra agent with sample transactions.
    """
    # Initialize the orchestrator agent
    orchestrator = TriNetraOrchestratorAgent()

    # Create some sample transactions to process
    sample_transactions = [
        # A normal transaction
        Transaction(
            transaction_id="txn_001",
            payment_time=datetime.datetime.now(),
            payer_id="payer_12345",
            payee_id="payee_ABCDE",
            payment_amount=150.75,
            payment_currency="USD",
            payment_method="Credit Card",
            payment_purpose="Online Purchase",
            vendor_id="vendor_TechGadgets",
            payee_country="USA",
            vendor_country="USA",
            vendor_industry="Electronics"
        ),
        # A transaction with a high amount, likely to be flagged by the FraudDetectionAgent
        Transaction(
            transaction_id="txn_002",
            payment_time=datetime.datetime.now(),
            payer_id="payer_12345",
            payee_id="payee_FGHIJ",
            payment_amount=2500.00,
            payment_currency="USD",
            payment_method="Bank Transfer",
            payment_purpose="Luxury Item Purchase",
            vendor_id="vendor_LuxuryGoods",
            payee_country="USA",
            vendor_country="USA",
            vendor_industry="Retail"
        ),
        # A transaction from a high-risk customer, to be flagged by the CustomerHistoryAgent
        Transaction(
            transaction_id="txn_003",
            payment_time=datetime.datetime.now(),
            payer_id="payer_67890", # This payer ID is used in CustomerHistoryAgent for high risk
            payee_id="payee_KLMNO",
            payment_amount=50.00,
            payment_currency="USD",
            payment_method="Debit Card",
            payment_purpose="Daily Coffee",
            vendor_id="vendor_CoffeeShop",
            payee_country="USA",
            vendor_country="USA",
            vendor_industry="Food & Beverage"
        ),
        # A transaction in the middle of the night, to be flagged by the RuleCheckAgent
        Transaction(
            transaction_id="txn_004",
            payment_time=datetime.datetime.now().replace(hour=3, minute=30),
            payer_id="payer_12345",
            payee_id="payee_PQRST",
            payment_amount=99.99,
            payment_currency="USD",
            payment_method="PayPal",
            payment_purpose="Game Subscription",
            vendor_id="vendor_OnlineGaming",
            payee_country="USA",
            vendor_country="USA",
            vendor_industry="Entertainment"
        ),
    ]

    # Run the orchestrator for each transaction
    for tx in sample_transactions:
        orchestrator.run(tx)


if __name__ == "__main__":
    main()
