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
from google.adk.agents import LlmAgent, SequentialAgent, Agent, ParallelAgent
from google.adk.tools import google_search
from google.genai import types
from .prompts.prompts import (
    EMAIL_DRAFTER_INSTRUCTION,
    EMAIL_PUBLISHER_INSTRUCTION,
    SLACK_DRAFTER_INSTRUCTION,
    SLACK_PUBLISHER_INSTRUCTION,
    EVENT_DETAILS_EXTRACTOR_INSTRUCTION,
    CALENDAR_PUBLISHER_INSTRUCTION,
    SUMMARY_AGENT_INSTRUCTION,
    MESSAGE_ENHANCER_INSTRUCTION,
    ROOT_AGENT_INSTRUCTION,
)

logger = logging.getLogger('google_adk.' + __name__)

root_agent = Agent(
    name="orchestrator_root_agent",
    description="TriNetra: Your Agent",
    model="gemini-2.5-flash",
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[
    ]
)
