#!/bin/bash

# Script to automatically create .env file from Cloud Shell environment
# This pulls configuration from gcloud and creates a properly configured .env file

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "=========================================="
echo "Tri-Netra Environment Configuration"
echo "=========================================="
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    print_warning ".env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Keeping existing .env file. Exiting."
        exit 0
    fi
    # Backup existing .env
    cp .env .env.backup
    print_info "Backed up existing .env to .env.backup"
fi

# Get GCP Project ID
print_info "Getting GCP project configuration..."
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    print_error "No GCP project configured!"
    print_info "Please run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

print_success "GCP Project: $PROJECT_ID"

# Get or set location
LOCATION=$(gcloud config get-value compute/region 2>/dev/null)

if [ -z "$LOCATION" ]; then
    print_warning "No default region configured"
    print_info "Available regions: us-central1, us-east1, us-west1, europe-west1, asia-southeast1"
    read -p "Enter your preferred location [us-central1]: " USER_LOCATION
    LOCATION=${USER_LOCATION:-us-central1}
fi

print_success "Location: $LOCATION"



echo ""
echo "=========================================="
print_success "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Load the environment variables:"
echo "   ${GREEN}source .env${NC}"
echo "   ${GREEN}export \$(cat .env | grep -v '^#' | xargs)${NC}"
echo ""
echo "2. Test your configuration:"
echo "   ${GREEN}python run_agent.py${NC}"
echo ""
echo "3. Start ADK web:"
echo "   ${GREEN}./run_adk_web.sh${NC}"
echo ""
echo "4. Or deploy to Cloud Run:"
echo "   ${GREEN}./deploy_cloud_run.sh${NC}"
echo ""
echo "Your .env file is at: $(pwd)/.env"
echo ""
