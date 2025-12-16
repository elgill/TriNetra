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
import datetime
import json
import asyncio
from typing import Dict, Any, List, Optional
from google.adk.tools.tool_context import ToolContext
from .config import (
    GOOGLE_OAUTH_CREDENTIALS_PATH,
    SLACK_MCP_XOXP_TOKEN,
)
from google import genai
from google.genai.types import HttpOptions
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

logger = logging.getLogger('google_adk.' + __name__)


