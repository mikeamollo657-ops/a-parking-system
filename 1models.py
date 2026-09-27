from pydantic import BaseModel, Field
from typing import Optional



class RateUpdateRequest(BaseModel):
    base_rate: float = Field(..., ge=0.0)
    hourly_rate: float = Field(..., ge=0.0)
    grace_period_minutes: int = Field(15, ge=0)
    vat_percentage: float = Field(16.0, ge=0.0)


class VehicleEntryRequest(BaseModel):
    plate_number: str = Field(..., min_length=3, max_length=20)


class FeeCalculationResponse(BaseModel):
    session_id: int
    plate_number: str
    bay_number: str
    entry_time: str
    exit_time: str
    duration_hours: int
    net_amount: float
    vat_amount: float
    gross_payable: float


class PaymentRequest(BaseModel):
    session_id: int
    payment_method: str = Field(..., example="MPESA")
    amount_paid: float = Field(..., gt=0.0)
    mpesa_receipt_number: Optional[str] = None


class OverrideEntryRequest(BaseModel):
    plate_number: str
    flat_rate: float
    reason: str
