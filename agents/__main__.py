"""
Main entry point for running Tri-Netra agents with ADK.
This file makes the agents directory discoverable by ADK web.
"""

from agents.tri_netra_orchestrator.agent import tri_netra_root_agent

# Export the main agent for ADK to discover
__all__ = ['tri_netra_root_agent']

# Set as the default agent
agent = tri_netra_root_agent
