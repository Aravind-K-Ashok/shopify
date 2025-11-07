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

Database configuration is now read from environment variables. You can provide either a single `DATABASE_URL` (recommended) or the individual `DB_*` variables.

Preferred: set `DATABASE_URL` (example, do NOT commit secrets):

```text
# Example (remove credentials and fill in your password before use):
# DATABASE_URL=mysql://avnadmin:REPLACE_WITH_PASSWORD@mysql-29c6b70f-aravindkashok10-db91.i.aivencloud.com:18523/defaultdb?ssl-mode=REQUIRED
DATABASE_URL=
```

Or set individual variables (used when `DATABASE_URL` is not present):

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=ecomdb
```

Optional: If your provider requires TLS verification, upload the provider's CA bundle to the host/container and set:

```text
DB_SSL_CA=/path/to/ca-bundle.pem
```

A `.env.example` file has been added to the repository to show the variables and expected format. For local development copy it to `.env` and fill values (do NOT commit `.env`).

## Importing the provided SQL backup

To import the SQL backup located at `app/database_backup/data_*.sql` into a remote MySQL (Aiven) instance from your local machine, run:

```powershell
mysql -h <HOST> -P <PORT> -u <USER> -p --ssl-mode=REQUIRED <DB_NAME> < .\app\database_backup\data_20251107_212518.sql
```

Example (replace with your actual values):

```powershell
mysql -h mysql-29c6b70f-aravindkashok10-db91.i.aivencloud.com -P 18523 -u avnadmin -p --ssl-mode=REQUIRED defaultdb < .\app\database_backup\data_20251107_212518.sql
```

The command will prompt for the password. Make sure the `mysql` client is installed locally. If you prefer, you can import via the provider's console/GUI.

## Security Notes

Before deploying to production:
1. Move database credentials to environment variables (done)
2. Enable CORS only for trusted domains
3. Add rate limiting
4. Enable HTTPS
5. Add proper authentication mechanisms