from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_full_lending_flow():
    # Create members
    lender = client.post(
        "/members",
        json={"name": "Alice", "email": "alice@example.com"},
    ).json()

    borrower = client.post(
        "/members",
        json={"name": "Bob", "email": "bob@example.com"},
    ).json()

    # Create book
    book = client.post(
        "/books",
        json={
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "owner_id": lender["id"],
        },
    ).json()

    # Request loan
    loan = client.post(
        "/loans/request",
        json={
            "book_id": book["id"],
            "borrower_id": borrower["id"],
        },
    ).json()

    assert loan["status"] == "PENDING"

    # Approve loan
    loan = client.post(
        f"/loans/{loan['id']}/approve",
        json={"lender_id": lender["id"]},
    ).json()

    assert loan["status"] == "APPROVED"

    # Return book
    loan = client.post(
        f"/loans/{loan['id']}/return",
        json={"borrower_id": borrower["id"]},
    ).json()

    assert loan["status"] == "RETURNED"
