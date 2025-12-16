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
  """Get all rejected transactions from the Transactions table.

  This function queries the Tri_Netra.Transactions table in project ccibt-hack25ww7-746
  and returns all transactions where approval_status='REJECTED'.

  Returns:
      str: JSON string containing rejected transaction details (payment_time, payer_id, payee_id).
  """
  client = get_bigquery_client()

  query = f"""
        SELECT payment_time,payer_id,payee_id
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

