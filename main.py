from __future__ import annotations

from datetime import datetime

from fastapi import FastAPI, HTTPException, status

from models import (
    Book,
    BookCreate,
    Loan,
    LoanApprove,
    LoanRequest,
    LoanReturn,
    LoanStatus,
    Member,
    MemberCreate,
)
from storage import storage

app = FastAPI(
    title="BBBBookclub Lending API",
    description="Demo API for a community book lending flow.",
    version="0.1.0",
)


@app.post("/members", response_model=Member, status_code=status.HTTP_201_CREATED)
def create_member(payload: MemberCreate) -> Member:
    return storage.create_member(payload)


@app.get("/members", response_model=list[Member])
def list_members() -> list[Member]:
    return storage.list_members()


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate) -> Book:
    owner = storage.get_member(payload.owner_id)
    if not owner:
        raise HTTPException(status_code=400, detail="Owner member does not exist")
    return storage.create_book(payload)


@app.get("/books", response_model=list[Book])
def list_books() -> list[Book]:
    return storage.list_books()


@app.get("/books/available", response_model=list[Book])
def list_available_books() -> list[Book]:
    return storage.list_available_books()


@app.post("/loans/request", response_model=Loan, status_code=status.HTTP_201_CREATED)
def request_loan(payload: LoanRequest) -> Loan:
    book = storage.get_book(payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    borrower = storage.get_member(payload.borrower_id)
    if not borrower:
        raise HTTPException(status_code=400, detail="Borrower does not exist")

    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is not available")

    if book.owner_id == payload.borrower_id:
        raise HTTPException(status_code=400, detail="Owner cannot borrow their own book")

    lender = storage.get_member(book.owner_id)
    if not lender:
        raise HTTPException(status_code=500, detail="Book owner record is missing")

    loan = storage.create_loan_request(book_id=book.id, lender_id=lender.id, borrower_id=borrower.id)

    book.is_available = False
    storage.save_book(book)

    return loan


@app.post("/loans/{loan_id}/approve", response_model=Loan)
def approve_loan(loan_id: int, payload: LoanApprove) -> Loan:
    loan = storage.get_loan(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.lender_id != payload.lender_id:
        raise HTTPException(status_code=403, detail="Only lender can approve the loan")

    if loan.status != LoanStatus.PENDING:
        raise HTTPException(status_code=400, detail="Loan is not in PENDING status")

    loan.status = LoanStatus.APPROVED
    loan.approved_at = datetime.utcnow()
    storage.save_loan(loan)
    return loan


@app.post("/loans/{loan_id}/reject", response_model=Loan)
def reject_loan(loan_id: int, payload: LoanApprove) -> Loan:
    loan = storage.get_loan(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.lender_id != payload.lender_id:
        raise HTTPException(status_code=403, detail="Only lender can reject the loan")

    if loan.status != LoanStatus.PENDING:
        raise HTTPException(status_code=400, detail="Loan is not in PENDING status")

    loan.status = LoanStatus.REJECTED
    loan.approved_at = datetime.utcnow()
    storage.save_loan(loan)

    book = storage.get_book(loan.book_id)
    if book:
        book.is_available = True
        storage.save_book(book)

    return loan


@app.post("/loans/{loan_id}/return", response_model=Loan)
def return_book(loan_id: int, payload: LoanReturn) -> Loan:
    loan = storage.get_loan(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.borrower_id != payload.borrower_id:
        raise HTTPException(status_code=403, detail="Only borrower can return the book")

    if loan.status != LoanStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Only APPROVED loans can be returned")

    loan.status = LoanStatus.RETURNED
    loan.returned_at = datetime.utcnow()
    storage.save_loan(loan)

    book = storage.get_book(loan.book_id)
    if book:
        book.is_available = True
        storage.save_book(book)

    return loan


@app.get("/loans", response_model=list[Loan])
def list_loans() -> list[Loan]:
    return storage.list_loans()
