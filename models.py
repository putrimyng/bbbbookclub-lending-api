from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LoanStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RETURNED = "RETURNED"


class MemberCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr


class Member(MemberCreate):
    id: int
    joined_at: datetime


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    owner_id: int


class Book(BaseModel):
    id: int
    title: str
    author: str
    owner_id: int
    is_available: bool = True


class LoanRequest(BaseModel):
    book_id: int
    borrower_id: int


class LoanApprove(BaseModel):
    lender_id: int


class LoanReturn(BaseModel):
    borrower_id: int


class Loan(BaseModel):
    id: int
    book_id: int
    lender_id: int
    borrower_id: int
    status: LoanStatus
    requested_at: datetime
    approved_at: Optional[datetime] = None
    returned_at: Optional[datetime] = None
