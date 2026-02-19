# Simple-Invoice-System-API
Simple RESTful Invoice System API supporting invoice creation, payments (including partial payments), and automated overdue processing with late fees. Implements clear domain-driven design, unit-tested business logic, and clean OOP practices. Containerized with Docker and easily extensible for future persistent storage integration.

# Invoice API Documentation

## Overview
A FastAPI-based Invoice Management System that handles creation, listing, payment processing, and overdue invoice management with in-memory storage.

**Base URL:** `/`  
**API Docs:** `/docs` (Swagger UI)  
**API Docs:** `/redoc` (ReDoc)

---

## API Endpoints

### 1. Create Invoice
- **Method:** `POST`
- **Path:** `/invoices`
- **Summary:** Create a new invoice
- **Status Code:** 201 Created

**Request Body:**
```json
{
  "amount": 1000.00,
  "due_date": "2026-03-15"
}
```

**Response:**
```json
{
  "id": "uuid-string"
}
```

---

### 2. List Invoices
- **Method:** `GET`
- **Path:** `/invoices`
- **Summary:** Retrieve all invoices

**Response:**
```json
[
  {
    "id": "uuid-string",
    "amount": 1000.00,
    "paid_amount": 0,
    "due_date": "2026-03-15",
    "status": "pending"
  }
]
```

---

### 3. Pay Invoice
- **Method:** `POST`
- **Path:** `/invoices/{invoice_id}/payments`
- **Summary:** Make a payment toward an invoice

**Request Body:**
```json
{
  "amount": 500.00
}
```

**Response:**
```json
{
  "id": "invoice-uuid",
  "status": "pending",
  "paid_amount": 500.00
}
```

**Error Responses:**
- `404` - Invoice not found
- `400` - Invoice is not pending

---

### 4. Process Overdue Invoices
- **Method:** `POST`
- **Path:** `/invoices/process-overdue`
- **Summary:** Process all overdue pending invoices and create new invoices with late fees

**Request Body:**
```json
{
  "late_fee": 50.00,
  "overdue_days": 30
}
```

**Response:**
```json
{
  "new_invoices": [
    {
      "id": "new-uuid",
      "amount": 1050.00,
      "paid_amount": 0,
      "due_date": "2026-03-21",
      "status": "pending"
    }
  ]
}
```

---

## Data Models

### Invoice
```
- id (string): Unique invoice identifier
- amount (float): Invoice total amount
- paid_amount (float): Amount paid so far (default: 0)
- due_date (date): Due date in YYYY-MM-DD format
- status (string): Invoice status (pending, paid, void)
```

### Invoice Status Values
- `pending` - Invoice awaiting payment
- `paid` - Invoice fully paid
- `void` - Invoice marked as void

---

## Business Logic

### Create Invoice
Generates a new invoice with PENDING status and stores it in memory.

### Pay Invoice
Accepts partial payments. Updates status to PAID when `paid_amount >= amount`.

### Process Overdue Invoices
1. Finds all PENDING invoices past their due date
2. For unpaid invoices: marks original as VOID, creates new invoice with late fee
3. For partially paid invoices: marks original as PAID, creates new invoice with remaining balance + late fee
4. New invoices get new due date based on `overdue_days` parameter

---

## Installation & Running

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Access API:** `http://localhost:8000`
