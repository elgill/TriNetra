# Tri-Netra Quick Start - Google Cloud Shell

Get up and running with Tri-Netra in 5 minutes using Google Cloud Shell.

## 🚀 Super Quick Start

Open [Google Cloud Shell](https://shell.cloud.google.com/) and run:

```bash
# 1. Set your project
gcloud config set project YOUR_PROJECT_ID

# 2. Upload/clone this project to Cloud Shell

# 3. Run setup
./setup_cloud_shell.sh

# 4. Activate environment
source venv/bin/activate

# 5. Edit .env and add your Google API key
nano .env

# 6. Run ADK Web
./run_adk_web.sh
```

That's it! 🎉

## 📋 Step-by-Step Guide

### 1. Open Cloud Shell

1. Go to https://console.cloud.google.com
2. Click the terminal icon (⌨️) in top right
3. Cloud Shell opens at the bottom

### 2. Get Your Code into Cloud Shell

**Option A: Upload Files**
- Click the ⋮ menu in Cloud Shell
- Select "Upload"
- Upload your TriNetra folder

**Option B: Clone from Git**
```bash
git clone YOUR_REPO_URL
cd TriNetra
```

**Option C: Use Cloud Shell Editor**
- Click the pencil icon to open editor
- Create files manually

### 3. Configure Your Project

```bash
# Set your GCP project
gcloud config set project YOUR_PROJECT_ID

# Verify
gcloud config list
```

### 4. Run Setup

```bash
chmod +x setup_cloud_shell.sh
./setup_cloud_shell.sh
```

Wait for it to complete (2-3 minutes).

### 5. Get Your API Key

**Method 1: Using Console**
1. Go to https://console.cloud.google.com/apis/credentials
2. Click "Create Credentials" > "API Key"
3. Copy the key

**Method 2: Using CLI**
```bash
gcloud alpha services api-keys create tri-netra-key \
    --display-name="Tri-Netra API Key"
```

### 6. Configure Environment

```bash
# Edit .env file
nano .env

# Add this line:
GOOGLE_API_KEY=your_actual_api_key_here

# Save: Ctrl+O, Enter
# Exit: Ctrl+X
```

### 7. Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` in your prompt.

### 8. Run Tri-Netra

**Option A: ADK Web Interface** (Recommended)
```bash
./run_adk_web.sh
```

Click the **Web Preview** button (🔗) in Cloud Shell and select port 8080.

**Option B: Simple Python Script**
```bash
python run_agent.py
```

**Option C: Example Scenarios**
```bash
python -m agents.tri_netra_orchestrator.example_usage
```

## 🧪 Testing the Agent

### Test 1: Simple Transaction

In ADK Web, enter:
```json
{
  "transaction_id": "test_001",
  "payment_amount": 100.00,
  "payment_currency": "USD",
  "payer_id": "payer_001",
  "payee_id": "payee_001",
  "payment_method": "Credit Card",
  "payment_purpose": "Test Transaction",
  "vendor_id": "vendor_test",
  "vendor_industry": "Retail",
  "payee_country": "USA",
  "vendor_country": "USA"
}
```

### Test 2: High-Risk Transaction

```json
{
  "transaction_id": "test_002",
  "payment_amount": 50000.00,
  "payment_currency": "USD",
  "payer_id": "payer_002",
  "payee_id": "payee_002",
  "payment_method": "Wire Transfer",
  "payment_purpose": "Large Equipment Purchase",
  "vendor_id": "vendor_industrial",
  "vendor_industry": "Manufacturing",
  "payee_country": "USA",
  "vendor_country": "China"
}
```

### Test 3: Using Python Script

Create a test file:
```bash
cat > quick_test.py << 'EOF'
import asyncio
from datetime import datetime
from google.adk.agents import run_agent
from agents.tri_netra_orchestrator import tri_netra_root_agent
from data_models.transaction_models import Transaction

async def test():
    tx = Transaction(
        transaction_id="quick_test",
        payment_time=datetime.now(),
        payer_id="payer_123",
        payee_id="payee_456",
        payment_amount=250.00,
        payment_currency="USD",
        payment_method="Credit Card",
        payment_purpose="Office Supplies",
        vendor_id="vendor_supplies",
        payee_country="USA",
        vendor_country="USA",
        vendor_industry="Office Equipment"
    )

    result = await run_agent(
        agent=tri_netra_root_agent,
        prompt=f"Analyze transaction {tx.transaction_id}",
        session_state={"transaction_data": tx.model_dump()}
    )

    print("\n" + "="*50)
    print("ANALYSIS RESULT")
    print("="*50)
    print(result)

asyncio.run(test())
EOF

python quick_test.py
```

## 🎯 What to Expect

When you submit a transaction, you'll see:

1. **Transaction Validation** - Confirms data is complete
2. **Parallel Analysis** - Four agents analyze simultaneously:
   - ✅ Fraud Detection
   - ✅ Rule Compliance
   - ✅ Customer History
   - ✅ Anomaly Detection
3. **Summary Report** - Aggregated recommendation
4. **Final Decision** - Approve/Review/Reject

## 🔧 Troubleshooting

### Problem: "No module named 'agents'"

**Solution:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Problem: "API key not valid"

**Solution:**
1. Check your API key in `.env`
2. Ensure it's not wrapped in quotes
3. Verify the key in Cloud Console

### Problem: "Port 8080 already in use"

**Solution:**
```bash
# Find and kill the process
lsof -i :8080
kill -9 <PID>

# Or use a different port
adk web --port 8081
```

### Problem: ADK command not found

**Solution:**
```bash
source venv/bin/activate
pip install google-adk google-adk-cli
```

### Problem: Permission denied on scripts

**Solution:**
```bash
chmod +x *.sh
```

## 📊 Viewing Results

### In ADK Web
- Results appear in the chat interface
- Each agent's decision is shown
- Final recommendation is highlighted

### In Python Output
- Console shows detailed logs
- Each agent's analysis is printed
- Final summary at the end

### Logs
```bash
# View recent logs
gcloud logging read --limit 10

# Follow logs in real-time
gcloud logging tail
```

## 🚢 Deploying to Production

Once you've tested locally, deploy to Cloud Run:

```bash
./deploy_cloud_run.sh
```

This gives you a public URL for your agent.

## 📚 Next Steps

1. **Customize prompts**: Edit `agents/tri_netra_orchestrator/prompts/prompts.py`
2. **Add real tools**: Update `agents/tri_netra_orchestrator/tools.py`
3. **Connect database**: Add customer history lookup
4. **Build UI**: Create a review dashboard
5. **Set up monitoring**: Add Cloud Monitoring

## 💡 Tips

- **Save your work**: Cloud Shell sessions timeout after 20 minutes of inactivity
- **Use tmux**: Keep sessions alive across disconnects
  ```bash
  tmux new -s trinetra
  # Work here
  # Detach: Ctrl+B then D
  # Reattach: tmux attach -t trinetra
  ```
- **Boost Cloud Shell**: Get more resources with "Boost Mode"
- **Clone to local**: Use `gcloud cloud-shell scp` to download files

## 🆘 Getting Help

1. Check `CLOUD_SETUP.md` for detailed docs
2. Review `agents/tri_netra_orchestrator/README.md` for architecture
3. See ADK docs: https://cloud.google.com/agent-developer-kit/docs
4. Report issues: Create a GitHub issue

## ✅ Checklist

- [ ] Cloud Shell opened
- [ ] Project configured
- [ ] Code uploaded/cloned
- [ ] Setup script run
- [ ] Environment activated
- [ ] API key configured
- [ ] ADK web started
- [ ] Test transaction submitted
- [ ] Results reviewed

Congratulations! You're now running Tri-Netra! 🎉
