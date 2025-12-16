#!/bin/bash

# Deployment script for Cloud Run
# Deploys Tri-Netra agent to Google Cloud Run

set -e

echo "=========================================="
echo "Deploying Tri-Netra to Cloud Run"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    print_error "No GCP project configured"
    exit 1
fi

# Configuration
SERVICE_NAME="tri-netra"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

print_info "Project: $PROJECT_ID"
print_info "Service: $SERVICE_NAME"
print_info "Region: $REGION"
echo ""

# Build the container
print_info "Building container image..."
gcloud builds submit --tag $IMAGE_NAME

print_success "Container image built"
echo ""

# Deploy to Cloud Run
print_info "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --set-env-vars "FRAUD_AMOUNT_THRESHOLD=10000.0,BUSINESS_RULES_ENABLED=true,TRI_NETRA_MODEL=gemini-2.0-flash-exp"

print_success "Deployment complete!"
echo ""

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "=========================================="
print_success "Tri-Netra is now live!"
echo "=========================================="
echo ""
echo "Service URL: ${GREEN}${SERVICE_URL}${NC}"
echo ""
echo "Test the service:"
echo "curl -X POST ${SERVICE_URL}/analyze \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"transaction_id\": \"test_001\", ...}'"
echo ""
