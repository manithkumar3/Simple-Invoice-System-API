from datetime import date
from pydantic import BaseModel


class InvoiceStatus:
    PENDING = "pending"
    PAID = "paid"
    VOID = "void"


class Invoice(BaseModel):
    id: str
    amount: float
    paid_amount: float = 0
    due_date: date
    status: str = InvoiceStatus.PENDING


class CreateInvoiceRequest(BaseModel):
    amount: float
    due_date: date


class PaymentRequest(BaseModel):
    amount: float


class ProcessOverdueRequest(BaseModel):
    late_fee: float
    overdue_days: int
