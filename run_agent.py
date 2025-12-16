#!/usr/bin/env python3
"""
Simple script to run the Tri-Netra agent interactively.
Alternative to using ADK web for quick testing.
"""

import asyncio
import json
from datetime import datetime
from google.adk.agents import run_agent
from agents.tri_netra_orchestrator.agent import tri_netra_root_agent
from data_models.transaction_models import Transaction


async def main():
    """Interactive agent runner."""

    print("=" * 60)
    print("Tri-Netra Transaction Analysis Agent")
    print("=" * 60)
    print()

    # Example transaction - you can modify this
    transaction = Transaction(
        transaction_id="txn_demo_001",
        payment_time=datetime.now(),
        payer_id="payer_12345",
        payee_id="payee_ABCDE",
        payment_amount=1500.00,
        payment_currency="USD",
        payment_method="Credit Card",
        payment_purpose="Electronics Purchase",
        vendor_id="vendor_TechStore",
        payee_country="USA",
        vendor_country="USA",
        vendor_industry="Electronics"
    )

    print("Analyzing Transaction:")
    print(f"  ID: {transaction.transaction_id}")
    print(f"  Amount: {transaction.payment_amount} {transaction.payment_currency}")
    print(f"  From: {transaction.payer_id} → {transaction.payee_id}")
    print(f"  Purpose: {transaction.payment_purpose}")
    print()
    print("-" * 60)
    print()

    # Convert to dict for the agent
    transaction_data = transaction.model_dump()

    # Prepare the prompt
    prompt = f"""
Please analyze the following transaction:

Transaction ID: {transaction_data['transaction_id']}
Payer: {transaction_data['payer_id']}
Payee: {transaction_data['payee_id']}
Amount: {transaction_data['payment_amount']} {transaction_data['payment_currency']}
Payment Method: {transaction_data['payment_method']}
Purpose: {transaction_data['payment_purpose']}
Vendor: {transaction_data['vendor_id']} ({transaction_data['vendor_industry']})
"""

    try:
        # Run the agent
        result = await run_agent(
            agent=tri_netra_root_agent,
            prompt=prompt,
            session_state={"transaction_data": transaction_data}
        )

        print()
        print("=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        print()
        print(result)
        print()

    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
