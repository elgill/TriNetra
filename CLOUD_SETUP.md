# Tri-Netra Setup Guide for Google Cloud Shell

This guide walks you through setting up and running Tri-Netra using Google ADK Web in Google Cloud Shell.

## Prerequisites

- Google Cloud account
- A Google Cloud project with billing enabled
- Access to Google Cloud Shell

## Quick Start

### 1. Open Google Cloud Shell

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click the **Cloud Shell** icon in the top right corner (terminal icon)
3. Wait for Cloud Shell to initialize

### 2. Clone or Upload Your Project

If your project is in a Git repository:
```bash
git clone <your-repo-url>
cd TriNetra
```

Or upload the project files using the Cloud Shell file upload feature.

### 3. Run the Setup Script

```bash
chmod +x setup_cloud_shell.sh
./setup_cloud_shell.sh
```

This script will:
- ✅ Configure your GCP project
- ✅ Enable required APIs
- ✅ Set up Python virtual environment
- ✅ Install dependencies
- ✅ Create environment configuration

### 4. Activate the Environment

```bash
source venv/bin/activate
```

### 5. Configure Your Settings

Edit the `.env` file:
```bash
nano .env
```

**Important**: Set your Google API key:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

### 6. Run the Agent

You have three options:

#### Option A: ADK Web Interface (Recommended for Testing)

```bash
adk web
```

This starts a web interface where you can interact with the agent. Cloud Shell will provide a preview URL.

#### Option B: Python Script

```bash
python -m agents.tri_netra_orchestrator.example_usage
```

#### Option C: Deploy to Cloud Run (Production)

```bash
./deploy_cloud_run.sh
```

## Detailed Setup Steps

### Step 1: Configure GCP Project

Set your project ID:
```bash
gcloud config set project YOUR_PROJECT_ID
```

Check your configuration:
```bash
gcloud config list
```

### Step 2: Enable Required APIs

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudaicompanion.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 3: Get API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **APIs & Services** > **Credentials**
3. Click **Create Credentials** > **API Key**
4. Copy the API key
5. Add it to your `.env` file

### Step 4: Install Google ADK

The setup script installs ADK, but you can also install it manually:

```bash
pip install google-adk google-generativeai
```

### Step 5: Test Your Installation

Run a quick test:
```bash
python3 << EOF
from agents.tri_netra_orchestrator import tri_netra_root_agent
print(f"Agent loaded: {tri_netra_root_agent.name}")
print("Configuration is valid!")
EOF
```

## Using ADK Web

### Starting the Web Interface

```bash
adk web
```

You'll see output like:
```
Starting ADK web interface...
Access the UI at: https://8080-cs-xxxxx-yyy.cloudshell.dev/
```

### Using the Web Interface

1. Click on the preview URL or use the **Web Preview** button in Cloud Shell
2. You'll see the Tri-Netra agent interface
3. Enter transaction details in the form:
   - Transaction ID
   - Amount and currency
   - Payer and payee information
   - Payment method and purpose
   - Vendor details

4. Click **Analyze Transaction**
5. View the results from all parallel agents

### Example Transaction Input

```json
{
  "transaction_id": "txn_001",
  "payment_amount": 1500.00,
  "payment_currency": "USD",
  "payer_id": "payer_12345",
  "payee_id": "payee_ABCDE",
  "payment_method": "Credit Card",
  "payment_purpose": "Electronics Purchase",
  "vendor_id": "vendor_TechStore",
  "vendor_industry": "Electronics",
  "payee_country": "USA",
  "vendor_country": "USA"
}
```

## Alternative: Running with Python Script

Create a test script:

```bash
cat > test_transaction.py << 'EOF'
import asyncio
from datetime import datetime
from google.adk.agents import run_agent
from agents.tri_netra_orchestrator import tri_netra_root_agent
from data_models.transaction_models import Transaction

async def main():
    transaction = Transaction(
        transaction_id="txn_test_001",
        payment_time=datetime.now(),
        payer_id="payer_12345",
        payee_id="payee_ABCDE",
        payment_amount=1500.00,
        payment_currency="USD",
        payment_method="Credit Card",
        payment_purpose="Electronics Purchase",
        vendor_id="vendor_TechStore",
        payee_country="USA",
        vendor_country="USA",
        vendor_industry="Electronics"
    )

    transaction_data = transaction.model_dump()

    result = await run_agent(
        agent=tri_netra_root_agent,
        prompt=f"Analyze transaction {transaction.transaction_id}",
        session_state={"transaction_data": transaction_data}
    )

    print(result)

asyncio.run(main())
EOF

python test_transaction.py
```

## Deploying to Production

### Option 1: Cloud Run (Recommended)

Cloud Run is serverless and scales automatically:

```bash
./deploy_cloud_run.sh
```

### Option 2: App Engine

For more traditional deployment:

```bash
gcloud app deploy app.yaml
```

### Option 3: GKE (Kubernetes)

For complex deployments with multiple services:

```bash
# Build image
docker build -t gcr.io/$PROJECT_ID/tri-netra:latest .

# Push to registry
docker push gcr.io/$PROJECT_ID/tri-netra:latest

# Deploy to GKE
kubectl apply -f kubernetes/deployment.yaml
```

## Configuration Options

### Environment Variables

Edit `.env` or set in Cloud Shell:

```bash
export FRAUD_AMOUNT_THRESHOLD=10000.0
export HIGH_RISK_COUNTRIES="XX,YY,ZZ"
export BUSINESS_RULES_ENABLED=true
export TRI_NETRA_MODEL=gemini-2.0-flash-exp
export LOG_LEVEL=INFO
```

### Model Selection

Available models:
- `gemini-2.0-flash-exp` (Fast, recommended for development)
- `gemini-1.5-pro` (More capable)
- `gemini-2.5-flash` (Latest flash model)

Update in `.env`:
```bash
TRI_NETRA_MODEL=gemini-1.5-pro
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution**: Ensure you're in the project root and virtual environment is activated:
```bash
cd /path/to/TriNetra
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: "API not enabled" errors

**Solution**: Enable the required API:
```bash
gcloud services enable aiplatform.googleapis.com
```

### Issue: "Permission denied" errors

**Solution**: Ensure you have proper IAM roles:
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="user:your-email@example.com" \
    --role="roles/aiplatform.user"
```

### Issue: ADK web won't start

**Solution**: Check if port 8080 is available:
```bash
lsof -i :8080
# Kill any process using the port
kill -9 <PID>
# Try again
adk web
```

### Issue: Import errors with google.adk

**Solution**: Ensure correct ADK installation:
```bash
pip uninstall google-adk
pip install google-adk --upgrade
```

## Monitoring and Logs

### View Cloud Run Logs

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=tri-netra" \
    --limit 50 \
    --format json
```

### Enable Cloud Logging

Add to your code:
```python
import logging
from google.cloud import logging as cloud_logging

client = cloud_logging.Client()
client.setup_logging()
```

## Performance Optimization

### Cold Start Reduction

1. **Keep instances warm**:
```bash
gcloud run services update tri-netra \
    --min-instances=1
```

2. **Use faster model**:
```bash
export TRI_NETRA_MODEL=gemini-2.0-flash-exp
```

3. **Optimize imports**: Move heavy imports inside functions

### Scaling Configuration

For Cloud Run:
```bash
gcloud run services update tri-netra \
    --max-instances=100 \
    --concurrency=80
```

## Security Best Practices

1. **Use Secret Manager for sensitive data**:
```bash
gcloud secrets create tri-netra-api-key --data-file=api_key.txt
```

2. **Enable authentication**:
```bash
gcloud run services update tri-netra \
    --no-allow-unauthenticated
```

3. **Use VPC connector** for database access
4. **Enable audit logging**
5. **Use least privilege IAM roles**

## Cost Management

### Estimate Costs

- Cloud Run: Pay per use (first 2M requests free)
- Gemini API: Pay per token
- Cloud Storage: Pay per GB stored

### Cost Optimization Tips

1. Use `gemini-2.0-flash-exp` for lower costs
2. Set max instances limit
3. Enable request caching
4. Monitor usage with Budget Alerts:

```bash
gcloud billing budgets create \
    --billing-account=YOUR_BILLING_ACCOUNT \
    --display-name="Tri-Netra Budget" \
    --budget-amount=100USD
```

## Next Steps

1. **Customize the agents**: Edit prompts in `agents/tri_netra_orchestrator/prompts/prompts.py`
2. **Add real tools**: Replace mock implementations in `tools.py`
3. **Set up CI/CD**: Use Cloud Build with `cloudbuild.yaml`
4. **Add monitoring**: Integrate with Cloud Monitoring
5. **Create a frontend**: Build a UI for the human review queue

## Resources

- [Google ADK Documentation](https://cloud.google.com/agent-developer-kit/docs)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Shell Documentation](https://cloud.google.com/shell/docs)

## Support

For issues with:
- **Tri-Netra**: Check the main README.md
- **Google ADK**: See [ADK GitHub](https://github.com/googleapis/python-aiplatform)
- **Cloud Shell**: Contact Google Cloud Support

---

**Need Help?** Create an issue in the repository or contact the development team.
