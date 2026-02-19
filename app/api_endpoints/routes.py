from fastapi import APIRouter, status
from app.api_endpoints.v1.invoice import (
    create_invoice, list_invoices, pay_invoice,
    process_overdue_invoices
)

router = APIRouter(tags=["Invoice API's"])

router.add_api_route(
    path="/invoices",
    endpoint=create_invoice,
    methods=["POST"],
    summary="Create Invoice",
    description="Creates a new invoice with the specified details.",
    status_code=status.HTTP_201_CREATED
)

router.add_api_route(
    path="/invoices",
    endpoint=list_invoices,
    methods=["GET"],
    summary="List Invoices",
    description="Lists all invoices."
)

router.add_api_route(
    path="/invoices/{invoice_id}/payments",
    endpoint=pay_invoice,
    methods=["POST"],
    summary="Pay Invoice",
    description="Pay an invoice."
)

router.add_api_route(
    path="/invoices/process-overdue",
    endpoint=process_overdue_invoices,
    methods=["POST"],
    summary="Process Overdue Invoices",
    description="Process all overdue invoices."
)
