# E-Commerce Backend

A FastAPI-based e-commerce backend with a frontend interface.

## Features

- Customer management (registration, authentication)
- Product catalog with categories
- Shopping cart functionality
- Order processing
- Seller dashboard
- Review system

## Tech Stack

- Backend: Python/FastAPI
- Database: MySQL
- Frontend: HTML/CSS/JavaScript
- Authentication: Custom token-based

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Unix/macOS
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
   - Create a database named 'ecomdb'
   - Update database credentials in `app/database/database.py` if needed

4. Run the application:
```bash
uvicorn app.main:app --reload
```

5. Access the application:
   - API Documentation: http://localhost:8000/docs
   - Frontend: Open `frontend/index.html` in a browser

## Project Structure

```
ecom_backend/
├── app/
│   ├── database/       # Database configuration
│   ├── models/         # Data models
│   ├── routes/         # API endpoints
│   ├── services/       # Business logic
│   └── main.py        # Application entry point
├── frontend/
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   └── *.html         # Frontend pages
└── requirements.txt    # Python dependencies
```

## API Documentation

The API documentation is automatically generated and can be accessed at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Database configuration can be found in `app/database/database.py`. Update the following values as needed:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "ecomdb"
}
```

## Security Notes

Before deploying to production:
1. Move database credentials to environment variables
2. Enable CORS only for trusted domains
3. Add rate limiting
4. Enable HTTPS
5. Add proper authentication mechanisms