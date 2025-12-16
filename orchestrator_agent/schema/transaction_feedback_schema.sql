-- Transaction Feedback Table Schema
-- This table stores user feedback on transaction approval decisions made by the agent
-- Purpose: Enable the system to learn from user corrections and improve decision accuracy

CREATE TABLE IF NOT EXISTS `ccibt-hack25ww7-746.Tri_Netra.Transaction_Feedback` (
  -- Feedback identification
  feedback_id STRING NOT NULL,
  feedback_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),

  -- Transaction details (from user input)
  transaction_id STRING,
  payer_id STRING,
  payee_id STRING,
  payment_amount FLOAT64,
  payment_currency STRING,
  payment_method STRING,
  payment_purpose STRING,
  vendor_id STRING,
  payee_country STRING,
  vendor_country STRING,
  vendor_industry STRING,

  -- Agent decision
  agent_decision STRING NOT NULL,  -- 'APPROVE', 'REJECT', or 'MARKED FOR REVIEW'
  agent_reasoning TEXT,
  agent_confidence STRING,  -- 'High', 'Medium', 'Low'

  -- User feedback
  user_decision STRING NOT NULL,  -- 'APPROVE', 'REJECT', or 'MARKED FOR REVIEW'
  is_agent_correct BOOLEAN NOT NULL,  -- TRUE if agent decision matches user decision
  feedback_notes TEXT,  -- Optional user comments/explanation

  -- Metadata
  session_id STRING,
  agent_version STRING
);

-- Add description to the table
ALTER TABLE `ccibt-hack25ww7-746.Tri_Netra.Transaction_Feedback`
SET OPTIONS (
  description = 'Stores user feedback on transaction approval decisions to improve agent accuracy over time'
);
