"""
Example usage of the Tri-Netra orchestrator agent.

This script demonstrates how to use the Tri-Netra transaction analysis system
to analyze financial transactions using parallel analysis agents.
"""

import asyncio
import logging
from datetime import datetime
from google.adk.agents import run_agent
from .agent import tri_netra_root_agent
from data_models.transaction_models import Transaction

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def analyze_transaction_example():
    """
    Example function demonstrating how to analyze a transaction using Tri-Netra.
    """

    # Create a sample transaction
    sample_transaction = Transaction(
        transaction_id="txn_demo_001",
        payment_time=datetime.now(),
        payer_id="payer_12345",
        payee_id="payee_ABCDE",
        payment_amount=1500.75,
        payment_currency="USD",
        payment_method="Credit Card",
        payment_purpose="Online Purchase - Electronics",
        vendor_id="vendor_TechGadgets",
        payee_country="USA",
        vendor_country="USA",
        vendor_industry="Electronics"
    )

    logger.info(f"Analyzing transaction: {sample_transaction.transaction_id}")

    # Convert transaction to dictionary for the agent
    transaction_data = sample_transaction.model_dump()

    # Prepare the prompt for the agent
    prompt = f"""
Please analyze the following transaction:

Transaction ID: {transaction_data['transaction_id']}
Payer: {transaction_data['payer_id']}
Payee: {transaction_data['payee_id']}
Amount: {transaction_data['payment_amount']} {transaction_data['payment_currency']}
Payment Method: {transaction_data['payment_method']}
Purpose: {transaction_data['payment_purpose']}
Vendor: {transaction_data['vendor_id']} ({transaction_data['vendor_industry']})
Countries: Payer in {transaction_data['payee_country']}, Vendor in {transaction_data['vendor_country']}
"""

    # Run the Tri-Netra agent
    try:
        result = await run_agent(
            agent=tri_netra_root_agent,
            prompt=prompt,
            session_state={"transaction_data": transaction_data}
        )

        logger.info("Analysis completed successfully")
        logger.info(f"Result: {result}")

        return result

    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise


async def analyze_multiple_transactions():
    """
    Example function demonstrating batch analysis of multiple transactions.
    """

    # Create multiple sample transactions
    transactions = [
        Transaction(
            transaction_id="txn_001",
            payment_time=datetime.now(),
            payer_id="payer_12345",
            payee_id="payee_001",
            payment_amount=150.00,
            payment_currency="USD",
            payment_method="Credit Card",
            payment_purpose="Coffee Shop",
            vendor_id="vendor_CoffeeShop",
            payee_country="USA",
            vendor_country="USA",
            vendor_industry="Food & Beverage"
        ),
        Transaction(
            transaction_id="txn_002",
            payment_time=datetime.now(),
            payer_id="payer_67890",
            payee_id="payee_002",
            payment_amount=25000.00,
            payment_currency="USD",
            payment_method="Wire Transfer",
            payment_purpose="Equipment Purchase",
            vendor_id="vendor_IndustrialEquip",
            payee_country="USA",
            vendor_country="China",
            vendor_industry="Manufacturing"
        ),
    ]

    logger.info(f"Analyzing {len(transactions)} transactions...")

    # Note: In production, you might want to process these with rate limiting
    # or batch processing to avoid overwhelming the system
    results = []
    for transaction in transactions:
        transaction_data = transaction.model_dump()

        prompt = f"""
Please analyze transaction {transaction_data['transaction_id']}:
Amount: {transaction_data['payment_amount']} {transaction_data['payment_currency']}
From: {transaction_data['payer_id']} to {transaction_data['payee_id']}
Purpose: {transaction_data['payment_purpose']}
"""

        try:
            result = await run_agent(
                agent=tri_netra_root_agent,
                prompt=prompt,
                session_state={"transaction_data": transaction_data}
            )
            results.append(result)
        except Exception as e:
            logger.error(f"Error analyzing transaction {transaction.transaction_id}: {e}")

    logger.info(f"Batch analysis complete. Processed {len(results)} transactions.")
    return results


def main():
    """Main entry point for the example."""

    print("=" * 60)
    print("Tri-Netra Transaction Analysis System - Example Usage")
    print("=" * 60)
    print()

    # Run single transaction analysis
    print("Example 1: Analyzing a single transaction")
    print("-" * 60)
    asyncio.run(analyze_transaction_example())

    print()
    print("=" * 60)
    print()

    # Run batch analysis
    print("Example 2: Analyzing multiple transactions")
    print("-" * 60)
    asyncio.run(analyze_multiple_transactions())


if __name__ == "__main__":
    main()
