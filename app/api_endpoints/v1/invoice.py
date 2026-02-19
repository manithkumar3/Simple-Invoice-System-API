import uuid
from datetime import date, timedelta
from fastapi import HTTPException
from app.api_endpoints.parser import (
    CreateInvoiceRequest, Invoice, InvoiceStatus, PaymentRequest,
    ProcessOverdueRequest
)


# In-memory store for invoices (i am not using a database for simplicity)
invoices = {}


def create_invoice(request: CreateInvoiceRequest):
    """Create a new invoice with the given amount and due date."""
    try:
        invoice_id = str(uuid.uuid4())
        invoice = Invoice(
            id=invoice_id,
            amount=request.amount,
            due_date=request.due_date,
            status=InvoiceStatus.PENDING
        )
        invoices[invoice_id] = invoice
        return {"id": invoice_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def list_invoices():
    """Return all invoices."""
    try:
        return [invoice.dict() for invoice in invoices.values()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def pay_invoice(invoice_id: str, request: PaymentRequest):
    """Make a payment toward an invoice."""
    try:
        invoice = invoices.get(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        if invoice.status != InvoiceStatus.PENDING:
            raise HTTPException(
                status_code=400, detail="Invoice is not pending"
            )
        invoice.paid_amount += request.amount
        if invoice.paid_amount >= invoice.amount:
            invoice.status = InvoiceStatus.PAID
        invoices[invoice_id] = invoice
        return {
            "id": invoice_id,
            "status": invoice.status,
            "paid_amount": invoice.paid_amount
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def process_overdue_invoices(request: ProcessOverdueRequest):
    """Process overdue invoices and create new invoices with late fees."""
    try:
        today = date.today()
        new_invoices = []
        for invoice in list(invoices.values()):
            if (
                invoice.status == InvoiceStatus.PENDING
                and invoice.due_date < today
            ):
                if invoice.paid_amount == 0:
                    invoice.status = InvoiceStatus.VOID
                    new_amount = invoice.amount + request.late_fee
                elif invoice.paid_amount < invoice.amount:
                    invoice.status = InvoiceStatus.PAID
                    new_amount = (
                        invoice.amount - invoice.paid_amount
                    ) + request.late_fee

                new_invoice_id = str(uuid.uuid4())
                new_due_date = today + timedelta(days=request.overdue_days)
                new_invoice = Invoice(
                    id=new_invoice_id,
                    amount=new_amount,
                    due_date=new_due_date,
                    status=InvoiceStatus.PENDING
                )
                invoices[new_invoice_id] = new_invoice
                new_invoices.append(new_invoice.model_dump())
        return {"new_invoices": new_invoices}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
