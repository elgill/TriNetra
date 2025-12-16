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
import google.auth

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode

from .prompts.prompts import ROOT_AGENT_INSTRUCTION
from .tools import get_approval_status

logger = logging.getLogger('google_adk.' + __name__)

# email_drafting_agent = SequentialAgent(
#     name="email_drafting_agent",
#     description="Drafts and sends an email announcement.",
#     sub_agents=[
#         Agent(
#             name="email_drafter",
#             model="gemini-2.5-flash",
#             instruction=EMAIL_DRAFTER_INSTRUCTION,
#             output_key="drafted_email"
#         ),
#         Agent(
#             name="email_publisher",
#             model="gemini-2.5-flash",
#             instruction=EMAIL_PUBLISHER_INSTRUCTION,
#             output_key="email_publication_result",
#             tools=[
#                 publish_email_announcement,
#                 # The gmail_mcp_tool shows an example MCP setup.
#                 # MCP Tools can be used to integrate with email providers that have MCP servers.
#                 # Users can uncomment if they connect their own MCP credentials and configs.
#                 # gmail_mcp_tool,
#             ]
#         )
#     ]
# )
#
# slack_drafting_agent = SequentialAgent(
#     name="slack_drafting_agent",
#     description="Drafts and sends a Slack message to multiple channels.",
#     sub_agents=[
#         Agent(
#             name="slack_drafter",
#             model="gemini-2.5-flash",
#             instruction=SLACK_DRAFTER_INSTRUCTION,
#             output_key="drafted_slack_message"
#         ),
#         Agent(
#             name="slack_publisher",
#             model="gemini-2.5-flash",
#             instruction=SLACK_PUBLISHER_INSTRUCTION,
#             output_key="slack_publication_result",
#             tools=[
#                 publish_slack_message,
#                 # The slack_mcp_tool shows an example MCP setup.
#                 # MCP Tools can be used to integrate with Slack.
#                 # Users can uncomment if they connect their own MCP credentials and configs.
#                 # slack_mcp_tool,
#             ]
#         )
#     ]
# )
#
# calendar_creation_agent = SequentialAgent(
#     name="calendar_creation_agent",
#     description="Creates a Google Calendar event.",
#     sub_agents=[
#         Agent(
#             name="event_details_extractor",
#             model="gemini-2.5-flash",
#             instruction=EVENT_DETAILS_EXTRACTOR_INSTRUCTION,
#             output_key="event_details"
#         ),
#         Agent(
#             name="calendar_publisher",
#             model="gemini-2.5-flash",
#             instruction=CALENDAR_PUBLISHER_INSTRUCTION,
#             output_key="calendar_creation_result",
#             tools=[
#                 create_calendar_event,
#                 # The calendar_mcp_tool shows an example MCP setup.
#                 # MCP Tools can be used to integrate with calendar services.
#                 # Users can uncomment if they connect their own MCP credentials and configs.
#                 # calendar_mcp_tool,
#             ]
#         )
#     ]
# )
#
# broadcast_agent = ParallelAgent(
#     name="broadcast_agent",
#     description="Broadcasts the announcement to email, Slack, and Google Calendar simultaneously.",
#     sub_agents=[
#         email_drafting_agent,
#         slack_drafting_agent,
#         calendar_creation_agent
#     ]
# )
#
# summary_agent = LlmAgent(
#     name="summary_agent",
#     model="gemini-2.5-flash",
#     instruction=SUMMARY_AGENT_INSTRUCTION,
#     description="Summarizes the results of the broadcast.",
# )
#
#
# main_flow_agent = SequentialAgent(
#     name="main_flow_agent",
#     description="Handles the main flow of enhancing the message and broadcasting it.",
#     sub_agents=[
#         Agent(
#             name="message_enhancer",
#             description="Enhances the user's message to make it more detailed and informative.",
#             model="gemini-2.5-flash",
#             instruction=MESSAGE_ENHANCER_INSTRUCTION,
#             tools=[google_search],
#             output_key="enhanced_message"
#         ),
#         broadcast_agent,
#         summary_agent
#     ]
# )

# Configure BigQuery toolset with read-only access
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

application_default_credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(
    credentials=application_default_credentials
)

bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config, bigquery_tool_config=tool_config
)

# Wrap the custom function in FunctionTool
get_approval_status_tool = FunctionTool(get_approval_status)

# Analysis agent with BigQuery access
analysis_agent = Agent(
    model="gemini-2.5-pro",
    name="analysis_agent",
    description="Agent to answer questions about BigQuery and SQL queries",
    instruction="""\
You are a data analysis agent with direct access to BigQuery.

## CRITICAL: Your Data Source
You MUST ONLY work with this specific table:
- **Full Table Path**: `ccibt-hack25ww7-746.Tri_Netra.Transactions`
- **Project ID**: ccibt-hack25ww7-746
- **Dataset**: Tri_Netra
- **Table**: Transactions

**DO NOT explore or use any other BigQuery datasets or projects.**
**DO NOT use tables like bigquery-public-data.thelook_ecommerce.orders or any other public datasets.**

## Table Schema
The Transactions table contains:
- `transaction_id`: Unique identifier for each transaction
- `payment_time`: Timestamp of the transaction
- `payer_id`: ID of the payer
- `payee_id`: ID of the payee
- `payment_amount`: Amount of the transaction
- `payment_currency`: Currency (USD, EUR, GBP, JPY, CAD, etc.)
- `payment_method`: Method used (Credit Card, Wire, ACH, Check, Bank Transfer)
- `payment_purpose`: Purpose of the payment
- `vendor_id`: ID of the vendor
- `payee_country`: Country of the payee
- `vendor_country`: Country of the vendor
- `vendor_industry`: Industry of the vendor
- `approval_status`: Status of the transaction ('REJECTED', 'APPROVED', etc.)
- `reject_reason`: Reason for rejection (only for rejected transactions)

## Available Tools
1. **get_approval_status**: Pre-built tool that queries `ccibt-hack25ww7-746.Tri_Netra.Transactions`
   and returns all REJECTED transactions with their details including reject_reason
2. **BigQuery tools**: For custom queries on the Tri_Netra.Transactions table only

## Instructions for Rejected Transactions
When asked about rejected transactions:
1. **ALWAYS use the `get_approval_status` tool FIRST**
2. This tool is pre-configured for the correct table and query
3. DO NOT explore other datasets or tables
4. DO NOT ask about table structure - use the schema above

## Instructions for Other Queries
For queries about approved transactions or other analysis:
- Use BigQuery tools to query `ccibt-hack25ww7-746.Tri_Netra.Transactions` directly
- Always specify the full table path in your queries
- DO NOT search for or use other tables

## Example Queries
- Rejected transactions: Use `get_approval_status` tool
- Approved transactions: Query `ccibt-hack25ww7-746.Tri_Netra.Transactions WHERE approval_status='APPROVED'`
- All transactions: Query `ccibt-hack25ww7-746.Tri_Netra.Transactions`
    """,
    tools=[
        get_approval_status_tool,
        bigquery_toolset
    ],
)

# Root orchestrator agent
root_agent = Agent(
    name="orchestrator_root_agent",
    description="TriNetra: Your Agent",
    model="gemini-2.5-flash",
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[
        analysis_agent
    ]
)

