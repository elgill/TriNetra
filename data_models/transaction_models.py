from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Transaction(BaseModel):
    """A model representing a single transaction based on the provided dataset schema."""
    transaction_id: str = Field(..., description="The unique ID of the transaction.")
    payment_time: datetime = Field(..., description="The timestamp of the payment.")
    payer_id: str = Field(..., description="The ID of the entity making the payment.")
    payee_id: str = Field(..., description="The ID of the entity receiving the payment.")
    payment_amount: float = Field(..., description="The amount of the payment.")
    payment_currency: str = Field(..., description="The currency of the payment (e.g., USD, EUR).")
    payment_method: str = Field(..., description="The method used for the payment (e.g., Credit Card, Bank Transfer).")
    payment_purpose: str = Field(..., description="The stated purpose of the payment.")
    vendor_id: str = Field(..., description="The ID of the vendor involved in the transaction.")
    payee_country: str = Field(..., description="The country of the payee.")
    vendor_country: str = Field(..., description="The country of the vendor.")
    vendor_industry: str = Field(..., description="The industry of the vendor.")
    approval_status: Optional[str] = Field(None, description="The approval status of the transaction.")
    reject_reason: Optional[str] = Field(None, description="The reason for rejection, if applicable.")


class AnalysisResult(BaseModel):
    """A model for the result of a single analysis agent."""
    agent_name: str = Field(..., description="The name of the agent that produced this result.")
    decision: Literal["Approve", "Reject", "Review"] = Field(..., description="The decision of the agent.")
    reason: str = Field(..., description="The reason for the decision.")
    confidence_score: float = Field(..., ge=0, le=1, description="The confidence score of the decision.")
