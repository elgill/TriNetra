# Running Tri-Netra with Google ADK

This guide explains different ways to run Tri-Netra using Google ADK.

## Prerequisites

Ensure you have the environment set up:

```bash
# Activate virtual environment
source venv/bin/activate

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Load environment variables
source .env  # or: export $(cat .env | grep -v '^#' | xargs)
```

## Method 1: ADK Web Interface (Recommended)

The ADK web interface provides an interactive UI for testing your agent.

### Start ADK Web

**Option A: Using the helper script**
```bash
./run_adk_web.sh
```

**Option B: Manually**
```bash
# Point to the agents directory
adk web agents/

# Or run from the project root
adk web
```

### Access the UI

1. Look for output like:
   ```
   Starting web server at http://localhost:8080
   ```

2. **On Local Machine**: Open http://localhost:8080 in your browser

3. **On Cloud Shell**:
   - Click the "Web Preview" button (🔗) in the toolbar
   - Select "Preview on port 8080"
   - Or click the generated URL

### Using the Web Interface

Once the UI loads:

1. You'll see the Tri-Netra agent listed
2. Click to start a conversation
3. You can either:
   - **Chat naturally**: "Analyze this transaction: [details]"
   - **Use structured input**: Paste JSON transaction data

Example message:
```
Analyze this transaction:
- Transaction ID: txn_001
- Amount: $1,500 USD
- From payer_12345 to payee_ABCDE
- Credit Card payment for Electronics Purchase
```

## Method 2: Python Script

For programmatic testing without the UI.

### Using the Provided Script

```bash
python run_agent.py
```

This runs a demo transaction and shows the analysis results.

### Modifying the Script

Edit `run_agent.py` to test different transactions:

```python
transaction = Transaction(
    transaction_id="your_test_id",
    payment_amount=999.99,
    # ... modify other fields
)
```

### Creating Your Own Script

```python
import asyncio
from datetime import datetime
from google.adk.agents import run_agent
from agents.tri_netra_orchestrator.agent import tri_netra_root_agent
from data_models.transaction_models import Transaction

async def analyze():
    tx = Transaction(
        transaction_id="test_123",
        payment_time=datetime.now(),
        payer_id="payer_001",
        payee_id="payee_001",
        payment_amount=500.00,
        payment_currency="USD",
        payment_method="Credit Card",
        payment_purpose="Test",
        vendor_id="vendor_test",
        payee_country="USA",
        vendor_country="USA",
        vendor_industry="Retail"
    )

    result = await run_agent(
        agent=tri_netra_root_agent,
        prompt=f"Analyze transaction {tx.transaction_id}",
        session_state={"transaction_data": tx.model_dump()}
    )

    print(result)

asyncio.run(analyze())
```

## Method 3: Using Example Script

Run the built-in examples:

```bash
python -m agents.tri_netra_orchestrator.example_usage
```

This demonstrates:
- Single transaction analysis
- Batch processing
- Different transaction scenarios

## Method 4: Direct Agent Import

For integration into your own applications:

```python
from agents.tri_netra_orchestrator import tri_netra_root_agent

# Use tri_netra_root_agent in your code
# The agent is pre-configured and ready to use
```

## Troubleshooting

### Issue: "No agents found"

**Solution**: Ensure you're running from the project root:
```bash
cd /path/to/TriNetra
adk web agents/
```

### Issue: "Module not found"

**Solution**: Set PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: Port already in use

**Solution**: Use a different port:
```bash
adk web agents/ --port 8081
```

Or kill the existing process:
```bash
lsof -i :8080
kill -9 <PID>
```

### Issue: Agent doesn't respond

**Check**:
1. Environment variables loaded (especially `GOOGLE_API_KEY`)
2. Virtual environment activated
3. All dependencies installed: `pip install -r requirements.txt`

### Issue: Import errors with google.adk

**Solution**: Reinstall ADK:
```bash
pip uninstall google-adk
pip install google-adk --upgrade
```

## Configuration

### Environment Variables

Required:
```bash
GOOGLE_API_KEY=your_api_key_here
```

Optional:
```bash
FRAUD_AMOUNT_THRESHOLD=10000.0
BUSINESS_RULES_ENABLED=true
TRI_NETRA_MODEL=gemini-2.0-flash-exp
LOG_LEVEL=INFO
```

### Model Selection

Change the model in `.env`:
```bash
TRI_NETRA_MODEL=gemini-1.5-pro  # More capable
TRI_NETRA_MODEL=gemini-2.0-flash-exp  # Faster, cheaper
```

Or in your code:
```python
from agents.tri_netra_orchestrator.agent import tri_netra_root_agent

# The agent uses the model specified in config.py
# Override if needed by modifying the agent definition
```

## Advanced Usage

### Custom Session State

Pass additional context to the agent:

```python
result = await run_agent(
    agent=tri_netra_root_agent,
    prompt="Analyze this transaction",
    session_state={
        "transaction_data": transaction.model_dump(),
        "user_id": "admin_001",
        "review_mode": "detailed",
        "custom_rules": {...}
    }
)
```

### Streaming Responses

For real-time output (if supported):

```python
async for chunk in run_agent_stream(
    agent=tri_netra_root_agent,
    prompt=prompt,
    session_state={"transaction_data": tx_data}
):
    print(chunk, end='', flush=True)
```

### Batch Processing

Process multiple transactions:

```python
transactions = [tx1, tx2, tx3]
results = []

for tx in transactions:
    result = await run_agent(
        agent=tri_netra_root_agent,
        prompt=f"Analyze transaction {tx.transaction_id}",
        session_state={"transaction_data": tx.model_dump()}
    )
    results.append(result)
```

## Testing Different Scenarios

### Normal Transaction
```python
Transaction(
    transaction_id="normal_001",
    payment_amount=150.00,
    payment_method="Credit Card",
    # ... standard values
)
```

### High-Risk Transaction
```python
Transaction(
    transaction_id="highrisk_001",
    payment_amount=50000.00,  # Large amount
    payment_method="Wire Transfer",
    vendor_country="High-Risk-Country",
    # ... other values
)
```

### Suspicious Pattern
```python
Transaction(
    transaction_id="suspicious_001",
    payment_time=datetime.now().replace(hour=3),  # Odd hours
    vendor_id="risky-vendor",  # Flagged vendor
    # ... other values
)
```

## Monitoring and Logging

### Enable Detailed Logging

```bash
export LOG_LEVEL=DEBUG
```

Or in Python:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### View Agent Execution

The console output shows:
1. Transaction validation
2. Each agent's analysis
3. Decision logic
4. Final recommendation

### Save Results

```python
import json

result = await run_agent(...)

# Save to file
with open('analysis_results.json', 'w') as f:
    json.dump(result, f, indent=2)
```

## Performance Tips

1. **Use Fast Model**: `gemini-2.0-flash-exp` for development
2. **Cache Results**: Store analyzed transactions
3. **Batch Processing**: Group similar transactions
4. **Async Operations**: Use asyncio for concurrent processing

## Next Steps

- **Customize Prompts**: Edit `agents/tri_netra_orchestrator/prompts/prompts.py`
- **Add Tools**: Implement real logic in `agents/tri_netra_orchestrator/tools.py`
- **Deploy**: Use `deploy_cloud_run.sh` for production
- **Monitor**: Set up Cloud Monitoring

## Resources

- [Google ADK Documentation](https://cloud.google.com/agent-developer-kit/docs)
- [Gemini API Docs](https://ai.google.dev/docs)
- Project README: `README.md`
- Cloud Setup: `CLOUD_SETUP.md`
- Quick Start: `QUICKSTART.md`
