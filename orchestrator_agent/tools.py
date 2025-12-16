# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import json
from typing import Any, Dict, List, Optional

from google.cloud import bigquery
from .config import config

logger = logging.getLogger('google_adk.' + __name__)

def get_bigquery_client() -> bigquery.Client:
  """Get a configured BigQuery client."""
  return bigquery.Client(project=config.project_id)


def get_approval_status() -> str:
  """Get all rejected transactions with reasons from ccibt-hack25ww7-746.Tri_Netra.Transactions.

  USE THIS TOOL when users ask about:
  - Rejected transactions
  - Transactions that were rejected
  - Rejection reasons or why transactions were rejected
  - Failed transactions
  - Declined transactions

  This function is pre-configured to query the correct table:
  `ccibt-hack25ww7-746.Tri_Netra.Transactions` WHERE approval_status='REJECTED'

  Returns:
      str: JSON string containing rejected transaction details with:
           - transaction_id: Unique transaction identifier
           - payment_time: When the transaction occurred
           - payer_id: ID of the payer
           - payee_id: ID of the payee
           - payment_amount: Amount of the transaction
           - payment_currency: Currency used (USD, EUR, GBP, etc.)
           - reject_reason: The reason why the transaction was rejected
  """
  client = get_bigquery_client()

  query = f"""
        SELECT transaction_id, payment_time, payer_id, payee_id,
               payment_amount, payment_currency, reject_reason
        FROM `ccibt-hack25ww7-746.Tri_Netra.Transactions`
        WHERE approval_status='REJECTED'
     """

  try:
    query_job = client.query(query)
    results = query_job.result()
    routine_info_list = [dict(row.items()) for row in results]

    if not routine_info_list:
      return json.dumps(
          {
              "message": (
                  f"No data found"
                  f" in dataset."
              )
          },
          indent=2,
      )

    return json.dumps(routine_info_list, indent=2, default=str)

  except Exception as e:
    return json.dumps(
        {
            "error": (
                f"Error retrieving routines from dataset {e}"
            )
        },
        indent=2,
    )


def get_similar_transactions(
    payer_id: Optional[str] = None,
    payee_id: Optional[str] = None,
    payment_currency: Optional[str] = None,
    payment_method: Optional[str] = None,
    vendor_id: Optional[str] = None,
    payee_country: Optional[str] = None,
    vendor_country: Optional[str] = None,
    vendor_industry: Optional[str] = None,
    payment_amount: Optional[float] = None,
    limit: int = 100
) -> str:
  """Get similar transactions based on transaction characteristics.

  USE THIS TOOL when you need to analyze a transaction and find similar historical transactions
  to determine if it should be approved or rejected.

  Args:
      payer_id: ID of the payer (optional)
      payee_id: ID of the payee (optional)
      payment_currency: Currency used (USD, EUR, GBP, JPY, CAD) (optional)
      payment_method: Payment method (Credit Card, Wire, ACH, Check, Bank Transfer) (optional)
      vendor_id: ID of the vendor (optional)
      payee_country: Country of the payee (optional)
      vendor_country: Country of the vendor (optional)
      vendor_industry: Industry of the vendor (optional)
      payment_amount: Amount of the payment (optional) - if provided, will find transactions within +/- 20% range
      limit: Maximum number of transactions to return (default 100)

  Returns:
      str: JSON string containing similar transaction details with:
           - transaction_id: Unique transaction identifier
           - payment_time: When the transaction occurred
           - payer_id: ID of the payer
           - payee_id: ID of the payee
           - payment_amount: Amount of the transaction
           - payment_currency: Currency used
           - payment_method: Method used
           - payment_purpose: Purpose of payment
           - vendor_id: Vendor ID
           - payee_country: Country of payee
           - vendor_country: Country of vendor
           - vendor_industry: Industry of vendor
           - approval_status: Status (APPROVED, REJECTED, MARKED FOR REVIEW)
           - reject_reason: Reason for rejection (if rejected)
  """
  client = get_bigquery_client()

  # Build WHERE clauses dynamically based on provided parameters
  where_clauses = []

  if payer_id:
    where_clauses.append(f"payer_id = '{payer_id}'")
  if payee_id:
    where_clauses.append(f"payee_id = '{payee_id}'")
  if payment_currency:
    where_clauses.append(f"payment_currency = '{payment_currency}'")
  if payment_method:
    where_clauses.append(f"payment_method = '{payment_method}'")
  if vendor_id:
    where_clauses.append(f"vendor_id = '{vendor_id}'")
  if payee_country:
    where_clauses.append(f"payee_country = '{payee_country}'")
  if vendor_country:
    where_clauses.append(f"vendor_country = '{vendor_country}'")
  if vendor_industry:
    where_clauses.append(f"vendor_industry = '{vendor_industry}'")
  if payment_amount is not None:
    # Find transactions within +/- 20% of the amount
    lower_bound = payment_amount * 0.8
    upper_bound = payment_amount * 1.2
    where_clauses.append(f"payment_amount BETWEEN {lower_bound} AND {upper_bound}")

  # Construct the WHERE clause
  where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

  query = f"""
        SELECT
            transaction_id,
            payment_time,
            payer_id,
            payee_id,
            payment_amount,
            payment_currency,
            payment_method,
            payment_purpose,
            vendor_id,
            payee_country,
            vendor_country,
            vendor_industry,
            approval_status,
            reject_reason
        FROM `ccibt-hack25ww7-746.Tri_Netra.Transactions`
        WHERE {where_sql}
        ORDER BY payment_time DESC
        LIMIT {limit}
     """

  try:
    query_job = client.query(query)
    results = query_job.result()
    transaction_list = [dict(row.items()) for row in results]

    if not transaction_list:
      return json.dumps(
          {
              "message": "No similar transactions found in the dataset.",
              "query_parameters": {
                  "payer_id": payer_id,
                  "payee_id": payee_id,
                  "payment_currency": payment_currency,
                  "payment_method": payment_method,
                  "vendor_id": vendor_id,
                  "payee_country": payee_country,
                  "vendor_country": vendor_country,
                  "vendor_industry": vendor_industry,
                  "payment_amount": payment_amount
              }
          },
          indent=2,
      )

    # Add summary statistics
    approved_count = sum(1 for t in transaction_list if t.get('approval_status') == 'APPROVED')
    rejected_count = sum(1 for t in transaction_list if t.get('approval_status') == 'REJECTED')
    review_count = sum(1 for t in transaction_list if t.get('approval_status') == 'MARKED FOR REVIEW')

    response = {
        "summary": {
            "total_similar_transactions": len(transaction_list),
            "approved": approved_count,
            "rejected": rejected_count,
            "marked_for_review": review_count
        },
        "transactions": transaction_list
    }

    return json.dumps(response, indent=2, default=str)

  except Exception as e:
    return json.dumps(
        {
            "error": f"Error retrieving similar transactions: {e}"
        },
        indent=2,
    )

