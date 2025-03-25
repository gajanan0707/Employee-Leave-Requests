# Employee Leave Request System

A FastAPI-based REST API for managing employee leave requests.

## Project Structure

```
app/
├── __init__.py
├── main.py              # Application entry point
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic models
├── routes.py            # API routes
├── utils.py             # Utility functions
└── schema/
    ├── __init__.py
    └── schema.py        # Enums and shared schemas
```

## Setup

1. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Application:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Visit `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Features

- Create leave requests
- View employee leave history
- Automatic working days calculation
- Leave request validation
- Overlapping leave detection
- Maximum leave duration enforcement (14 days)