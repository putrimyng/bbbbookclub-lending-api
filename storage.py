from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from models import Book, BookCreate, Loan, LoanStatus, Member, MemberCreate


class InMemoryStorage:
    def __init__(self) -> None:
        self._members: Dict[int, Member] = {}
        self._books: Dict[int, Book] = {}
        self._loans: Dict[int, Loan] = {}

        self._member_seq = 0
        self._book_seq = 0
        self._loan_seq = 0

    # Members
    def create_member(self, data: MemberCreate) -> Member:
        self._member_seq += 1
        member = Member(
            id=self._member_seq,
            name=data.name,
            email=data.email,
            joined_at=datetime.utcnow(),
        )
        self._members[member.id] = member
        return member

    def list_members(self) -> List[Member]:
        return list(self._members.values())

    def get_member(self, member_id: int) -> Optional[Member]:
        return self._members.get(member_id)

    # Books
    def create_book(self, data: BookCreate) -> Book:
        self._book_seq += 1
        book = Book(
            id=self._book_seq,
            title=data.title,
            author=data.author,
            owner_id=data.owner_id,
            is_available=True,
        )
        self._books[book.id] = book
        return book

    def list_books(self) -> List[Book]:
        return list(self._books.values())

    def list_available_books(self) -> List[Book]:
        return [b for b in self._books.values() if b.is_available]

    def get_book(self, book_id: int) -> Optional[Book]:
        return self._books.get(book_id)

    def save_book(self, book: Book) -> None:
        self._books[book.id] = book

    # Loans
    def create_loan_request(self, *, book_id: int, lender_id: int, borrower_id: int) -> Loan:
        self._loan_seq += 1
        loan = Loan(
            id=self._loan_seq,
            book_id=book_id,
            lender_id=lender_id,
            borrower_id=borrower_id,
            status=LoanStatus.PENDING,
            requested_at=datetime.utcnow(),
        )
        self._loans[loan.id] = loan
        return loan

    def get_loan(self, loan_id: int) -> Optional[Loan]:
        return self._loans.get(loan_id)

    def save_loan(self, loan: Loan) -> None:
        self._loans[loan.id] = loan

    def list_loans(self) -> List[Loan]:
        return list(self._loans.values())


storage = InMemoryStorage()
