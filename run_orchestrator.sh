#!/bin/bash

# Setup and run the TriNetra Orchestrator Agent

# Set Google Cloud Project
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
echo "Using Google Cloud Project: $GOOGLE_CLOUD_PROJECT"

# Create an isolated python environment to avoid dependency issues
if [ ! -d ".adk-venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .adk-venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .adk-venv/bin/activate



# Launch ADK Web for the orchestrator agent
echo "Launching ADK Web for Orchestrator Agent..."
adk web
