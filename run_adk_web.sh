#!/bin/bash

# Quick script to run ADK web with proper environment setup

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if ADK is installed
if ! command -v adk &> /dev/null; then
    echo "ADK CLI not found. Installing..."
    pip install google-adk
fi

# Start ADK web
echo "Starting Tri-Netra with ADK Web..."
echo "Access the UI at the URL shown below"
echo ""

# Run ADK web pointing to the agents directory
adk web agents/
