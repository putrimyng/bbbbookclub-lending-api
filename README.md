# BBBBookclub Lending API

A simple proof-of-concept backend for a community-based book lending system (BBBBookclub).
This project is built as a technical product manager demo, focusing on clear domain modeling, API design, and readable code.

## Features
- Member registration
- Book registration
- Request / approve / reject / return book loans
- In-memory storage (no database)
- End-to-end API test covering the full lending flow

## Tech Stack
- Python
- FastAPI
- Pydantic
- Pytest

## Run locally
```bash
python3 -m pip install -r requirements.txt
uvicorn main:app --reload
