# TriNetra Sample Prompts

This file contains sample prompts to test and demonstrate the TriNetra transaction approval system.

---

## 1. Basic Transaction Evaluation Prompts

### Example 1: High-Value Transaction (Should be REJECTED)
```
I have a transaction that needs evaluation:
- Payer: COMP0030
- Payee: PAYEE0319
- Amount: 22755.21 GBP
- Payment method: Check
- Payee country: UK
- Vendor country: Canada
- Vendor industry: Manufacturing

Should this transaction be approved?
```

### Example 2: Low-Value Normal Transaction (Should be APPROVED)
```
Please evaluate this transaction:
- Payer: COMP0032
- Payee: PAYEE0181
- Amount: 5924.68 JPY
- Payment method: Bank Transfer
- Payment purpose: Legal Fees
- Payee country: Japan
- Vendor country: India
- Vendor industry: Education

Should I approve this?
```

### Example 3: Currency Mismatch (Should be REJECTED)
```
Can you analyze this transaction?
- Payer: COMP0098
- Payee: PAYEE0076
- Amount: 770.91 JPY
- Payment currency: JPY
- Payment method: Credit Card
- Payment purpose: Rent Payment
- Payee country: Canada
- Vendor country: India
- Vendor industry: Shell Corporations

What's your recommendation?
```

### Example 4: High-Risk Industry (Should be REJECTED)
```
Transaction details:
- Payer: COMP0090
- Payee: PAYEE0254
- Amount: 1048.80 CAD
- Payment method: Bank Transfer
- Payment purpose: Maintenance Services
- Payee country: UK
- Vendor country: USA
- Vendor industry: Cannabis Industry

Should this be approved or rejected?
```

---

## 2. Edge Case Transactions

### Example 5: Borderline High Value
```
Evaluate this borderline case:
- Payer: COMP0045
- Payee: PAYEE0200
- Amount: 14800.00 USD
- Payment method: Wire
- Payment purpose: Consulting Services
- Payee country: USA
- Vendor country: USA
- Vendor industry: Technology

Is this approvable?
```

### Example 6: Multiple Risk Factors
```
Transaction for review:
- Payer: COMP0010
- Payee: PAYEE0150
- Amount: 25000.00 GBP
- Payment method: Check
- Payment purpose: Unusual Transfer - Review Required
- Payee country: UK
- Vendor country: Brazil
- Vendor industry: Precious Metals Trading

Your assessment?
```

### Example 7: Art & Antiques (High-Risk Industry)
```
Need your opinion on this:
- Payer: COMP0028
- Payee: PAYEE0183
- Amount: 8500.00 EUR
- Payment method: Wire
- Payment purpose: Art Purchase
- Payee country: France
- Vendor country: Italy
- Vendor industry: Art & Antiques Dealers

Approve or reject?
```

---

## 3. Feedback Scenarios

### Scenario A: Agreeing with Agent
After the agent provides a decision, respond with:
```
Yes, I agree with your assessment. That's correct.
```

or

```
Correct, I would have made the same decision.
```

### Scenario B: Disagreeing - Agent Says REJECT, Should be APPROVED
After a REJECT decision, respond with:
```
Actually, this should be APPROVED. This vendor has pre-approved status
and special authorization from our compliance team.
```

or

```
I disagree. This transaction should be APPROVED because we have a
standing agreement with this vendor that allows for currency flexibility.
```

### Scenario C: Disagreeing - Agent Says APPROVE, Should be REJECTED
After an APPROVE decision, respond with:
```
No, this should be REJECTED. I noticed this vendor was recently flagged
for compliance issues in our internal audit.
```

or

```
This needs to be REJECTED. The payment purpose is suspicious and doesn't
match the vendor's typical business category.
```

### Scenario D: Requesting Review Instead
After any decision, respond with:
```
I think this should be MARKED FOR REVIEW instead. There are some
additional factors we need to verify with the legal team first.
```

---

## 4. Complex Multi-Field Transactions

### Example 8: Complete Transaction Data
```
Full transaction details for evaluation:
- Transaction ID: NEW-2025-001
- Payer: COMP0055
- Payee: PAYEE0287
- Amount: 12500.00 EUR
- Payment currency: EUR
- Payment method: Wire
- Payment purpose: Equipment Purchase
- Vendor ID: VEND0420
- Payee country: Germany
- Vendor country: Germany
- Vendor industry: Manufacturing

Please provide your approval recommendation.
```

### Example 9: Minimal Information Transaction
```
Quick evaluation needed:
- Amount: 3000.00 USD
- Payment method: Credit Card
- Payee country: USA
- Vendor industry: Technology

Can this be approved?
```

---

## 5. Data Analysis Prompts (for analysis_agent)

### Query 1: Rejected Transactions
```
Show me all rejected transactions
```

or

```
Can you tell me about rejected transactions?
```

### Query 2: Rejection Reasons
```
What are the most common rejection reasons?
```

### Query 3: Transaction Statistics
```
How many transactions are approved vs rejected?
```

### Query 4: Industry Analysis
```
Which industries have the highest rejection rates?
```

### Query 5: Currency Analysis
```
Show me rejected transactions by currency
```

---

## 6. Test Workflow: Complete Feedback Loop

Use this sequence to test the full feedback loop:

**Step 1: Submit Transaction**
```
Transaction evaluation needed:
- Payer: COMP0075
- Payee: PAYEE0340
- Amount: 18000.00 GBP
- Payment method: Wire
- Payee country: UK
- Vendor country: Canada
- Vendor industry: Manufacturing

Should this be approved?
```

**Step 2: Wait for Agent Decision**
(Agent will analyze and provide a decision)

**Step 3: Provide Feedback**
```
Actually, I think this should be APPROVED. This is part of a pre-negotiated
contract with volume discounts that brings the effective per-unit cost
below our threshold. The vendor has excellent compliance history.
```

**Step 4: Verify Feedback Stored**
(Agent should confirm both tables were updated)

**Step 5: Query Similar Transaction**
```
New transaction - similar to the previous one:
- Payer: COMP0075
- Payee: PAYEE0340
- Amount: 17500.00 GBP
- Payment method: Wire
- Payee country: UK
- Vendor country: Canada
- Vendor industry: Manufacturing

What's your recommendation?
```

**Expected Result**: Agent should now reference the previous feedback in its analysis

---

## 7. Greeting and Help Prompts

### Get Agent Capabilities
```
Hello
```

or

```
What can you help me with?
```

### Out of Scope Request
```
What's the weather today?
```

---

## 8. Special Scenarios for Advanced Testing

### Example 10: Returning Customer with History
```
This is a returning payer we've worked with before:
- Payer: COMP0003
- Payee: PAYEE0018
- Amount: 45789.44 USD
- Payment method: Check
- Payment purpose: Utilities
- Payee country: USD
- Vendor country: Australia
- Vendor industry: Precious Metals Trading

Historical context: We've approved similar amounts for this payer before.
What do you recommend?
```

### Example 11: International Transfer
```
Cross-border transaction:
- Payer: COMP0062
- Payee: PAYEE0401
- Amount: 8750.00 CAD
- Payment method: Wire
- Payment purpose: Professional Services
- Payee country: Canada
- Vendor country: Japan
- Vendor industry: Consulting

Approve?
```

### Example 12: Urgent Transaction
```
URGENT - Need quick assessment:
- Amount: 9500.00 EUR
- Vendor industry: Healthcare
- Payee country: Germany
- Vendor country: France
- Payment method: Wire

Time-sensitive approval needed.
```

---

## 9. Batch Evaluation (Sequential)

Test multiple transactions in sequence:

```
First transaction:
- Payer: COMP0011, Amount: 5000 USD, Industry: Technology, Countries: USA-USA
```

Wait for response, then:

```
Second transaction:
- Payer: COMP0012, Amount: 25000 GBP, Industry: Cannabis Industry, Countries: UK-Canada
```

Wait for response, then:

```
Third transaction:
- Payer: COMP0013, Amount: 3500 EUR, Industry: Education, Countries: Germany-Germany
```

---

## 10. Tips for Testing

### Getting Detailed Analysis
Add phrases like:
- "Please explain your reasoning in detail"
- "What similar transactions did you find?"
- "Why did you make this decision?"

### Testing Feedback Loop
1. Submit a transaction
2. Disagree with the agent's decision
3. Submit a very similar transaction
4. Check if the agent references the previous feedback

### Testing Edge Cases
- Very high amounts (>$50,000)
- Very low amounts (<$100)
- Unusual currency combinations
- Missing fields
- Multiple risk factors combined

---

## Quick Reference: Transaction Fields

Required for best analysis:
- **payer_id**: ID of the company making payment
- **payee_id**: ID of the recipient
- **payment_amount**: Transaction amount (numeric)
- **payment_currency**: USD, EUR, GBP, JPY, CAD, etc.
- **payment_method**: Credit Card, Wire, ACH, Check, Bank Transfer
- **payment_purpose**: Description of what the payment is for
- **vendor_id**: Vendor identifier
- **payee_country**: Country of the payee
- **vendor_country**: Country where vendor operates
- **vendor_industry**: Business category of vendor

Optional:
- **transaction_id**: Unique identifier
- **payment_time**: Timestamp of transaction

---

## Notes

- The agent will always ask for feedback after providing a decision
- Feedback is stored in BigQuery for continuous learning
- Each user correction improves future decisions
- You can provide additional context or notes with your feedback
- The system learns from both agreements and disagreements

Happy testing! 🚀
