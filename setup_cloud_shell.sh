#!/bin/bash

# Setup script for Tri-Netra in Google Cloud Shell
# This script sets up the environment and deploys the agent to ADK Web

set -e  # Exit on error

echo "=========================================="
echo "Tri-Netra Setup for Google Cloud Shell"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Check if gcloud is configured
print_info "Checking Google Cloud configuration..."
PROJECT_ID=$(gcloud config get-value project)

if [ -z "$PROJECT_ID" ]; then
    print_error "No GCP project configured. Please run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

print_success "Using GCP Project: $PROJECT_ID"
echo ""

# Step 2: Enable required APIs
print_info "Enabling required Google Cloud APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudaicompanion.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
print_success "APIs enabled"
echo ""

# Step 3: Set up Python virtual environment
print_info "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
print_success "Virtual environment created and activated"
echo ""

# Step 4: Install dependencies
print_info "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencies installed"
echo ""

# Step 5: Set up environment variables
print_info "Setting up environment variables..."
if [ ! -f .env ]; then
    print_info "Running create_env.sh to auto-generate .env file..."
    ./create_env.sh
else
    print_info ".env file already exists"
    read -p "Do you want to regenerate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./create_env.sh
    fi
fi

# Export environment variables
export GOOGLE_PROJECT_ID=$PROJECT_ID
export GOOGLE_CLOUD_PROJECT=$PROJECT_ID
print_success "Environment variables configured"
echo ""

# Step 6: Test the agent locally
print_info "Testing agent configuration..."
python3 -c "from agents.tri_netra_orchestrator import tri_netra_root_agent; print('Agent loaded successfully')" 2>/dev/null
if [ $? -eq 0 ]; then
    print_success "Agent configuration is valid"
else
    print_error "Agent configuration test failed. Please check your code."
    exit 1
fi
echo ""

# Step 7: Install ADK CLI (if not already installed)
print_info "Checking for Google ADK CLI..."
if ! command -v adk &> /dev/null; then
    print_info "Installing Google ADK CLI..."
    pip install google-adk-cli
    print_success "ADK CLI installed"
else
    print_success "ADK CLI already installed"
fi
echo ""

# Step 8: Initialize ADK project (if needed)
print_info "Initializing ADK project..."
if [ ! -f "adk_config.yaml" ]; then
    print_error "adk_config.yaml not found. Please ensure it exists."
    exit 1
fi
print_success "ADK configuration found"
echo ""

# Step 9: Print next steps
echo "=========================================="
print_success "Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Activate the virtual environment:"
echo "   ${GREEN}source venv/bin/activate${NC}"
echo ""
echo "2. Edit the .env file with your configuration:"
echo "   ${GREEN}nano .env${NC}"
echo ""
echo "3. Test the agent locally:"
echo "   ${GREEN}python -m agents.tri_netra_orchestrator.example_usage${NC}"
echo ""
echo "4. Run the agent with ADK web:"
echo "   ${GREEN}adk web${NC}"
echo ""
echo "5. Or deploy to Cloud Run:"
echo "   ${GREEN}./deploy_cloud_run.sh${NC}"
echo ""
echo "For more information, see CLOUD_SETUP.md"
echo ""
