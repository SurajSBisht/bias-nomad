# Bias Nomad Backend

A FastAPI-based backend API for **Bias Nomad** - a platform that helps users (especially people with disabilities) find inclusive and accessible job opportunities.

## 🏗️ Architecture

This backend follows a clean, modular architecture:

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── routes/              # API endpoint handlers
│   │   ├── users.py         # User management endpoints
│   │   ├── jobs.py          # Job listing endpoints
│   │   └── ml_routes.py     # ML recommendation endpoints
│   ├── database/            # Database configuration and models
│   │   ├── db_init.py       # Database connection and session management
│   │   └── models.py        # SQLAlchemy ORM models
│   ├── services/            # Business logic layer (for future use)
│   ├── utils/               # Utility functions
│   │   └── schemas.py       # Pydantic request/response schemas
│   └── __init__.py
├── ml/                      # Machine learning module
│   ├── train_recommender.py # Recommendation model training
│   ├── train_nlp_scoring.py # NLP scoring model training
│   └── saved_models/        # Trained model storage
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   # Option 1: Using uvicorn directly
   uvicorn app.main:app --reload
   
   # Option 2: Using Python
   python -m app.main
   ```

5. **Access the API:**
   - API Base URL: `http://localhost:8000`
   - Interactive API Docs (Swagger): `http://localhost:8000/docs`
   - Alternative Docs (ReDoc): `http://localhost:8000/redoc`

## 📚 API Endpoints

### Users

- `GET /users/` - Get all users (with pagination)
- `GET /users/{user_id}` - Get a specific user by ID
- `POST /users/` - Create a new user

### Jobs

- `GET /jobs/` - Get all jobs (with filtering and pagination)
  - Query parameters:
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum records to return (default: 100)
    - `is_remote`: Filter by remote work (optional)
    - `is_inclusive`: Filter by inclusive flag (optional)
    - `location`: Filter by location (optional, partial match)
- `GET /jobs/{job_id}` - Get a specific job by ID

### Machine Learning

- `POST /ml/recommend` - Get job recommendations for a user
  - Request body:
    ```json
    {
      "user_id": 1,
      "limit": 10
    }
    ```

## 🗄️ Database

The application uses **SQLite** by default (stored as `bias_nomad.db` in the backend directory).

### Database Models

- **User**: Stores user profiles with accessibility needs
- **Job**: Stores job postings with inclusivity and accessibility information

### Switching to PostgreSQL

To use PostgreSQL instead of SQLite:

1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `app/database/db_init.py`:
   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/bias_nomad"
   ```

3. Remove `connect_args={"check_same_thread": False}` from the engine creation

## 🧪 Testing the API

### Using Swagger UI

1. Navigate to `http://localhost:8000/docs`
2. Use the interactive interface to test endpoints

### Using cURL

**Create a user:**
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "has_disability": true,
    "disability_type": "Visual impairment",
    "accessibility_needs": "Screen reader compatible applications"
  }'
```

**Get all jobs:**
```bash
curl "http://localhost:8000/jobs/"
```

**Get job recommendations:**
```bash
curl -X POST "http://localhost:8000/ml/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "limit": 5
  }'
```

## 🔮 Future Enhancements

- [ ] Implement actual ML recommendation models
- [ ] Add NLP-based job scoring
- [ ] Add user authentication and authorization
- [ ] Add job application tracking
- [ ] Add email notifications
- [ ] Add comprehensive test suite
- [ ] Add API rate limiting
- [ ] Add request logging and monitoring
- [ ] Deploy to cloud infrastructure

## 📝 Development Notes

- The ML recommendation endpoint currently uses dummy scoring logic
- All models use Pydantic for automatic validation
- The codebase follows PEP 8 style guidelines
- Type hints are used throughout for better code clarity

## 🤝 Contributing

This is a starter project. Feel free to extend it with additional features as needed.

## 📄 License

This project is part of the Bias Nomad platform.

