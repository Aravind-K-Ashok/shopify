# Shopify E-Commerce (FastAPI + MySQL + Static Frontend)

FastAPI backend with a static HTML/CSS/JS frontend (GitHub Pages). Supports customers, products, categories, cart, orders, reviews, seller panel, transactions.

## Live
- Frontend: https://aravind-k-ashok.github.io/shopify/
- API Base: https://shopify-backend-m9ce.onrender.com

## Features
- Customer registration / login (token + customerID in localStorage)
- Product + category + subcategory hierarchy
- Image upload (Supabase Storage; move anon key to server for production)
- Cart logic (add/remove/quantity) persisted client-side
- Checkout flow: index → product → cart → payment → transactions
- Order placement (`/orders/place`) and status updates
- Seller dashboard (orders, revenue summary)
- Reviews & average rating display

## Tech Stack
Backend: FastAPI, Uvicorn  
DB: MySQL (local or managed)  
Frontend: Plain HTML/CSS/JavaScript (no build step)  
Storage: Supabase (optional)  

## Structure
```
ecom_backend/
├── app/
│   ├── main.py
│   ├── database/ (connection, session)
│   ├── models/   (SQLAlchemy models)
│   ├── routes/   (product, order, customer, category, review)
│   ├── services/ (business helpers)
│   └── database_backup/ (SQL dump)
├── frontend/
│   ├── *.html
│   ├── css/
│   └── js/
└── requirements.txt
```

## Setup (Local)
```bash
git clone https://github.com/Aravind-K-Ashok/shopify.git
cd ecom_backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

Create MySQL database:
```sql
CREATE DATABASE ecomdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Environment Variables
Use a single URL (preferred) or individual parts.

```
# .env
DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/ecomdb
# Or:
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=pass
DB_NAME=ecomdb
# Optional TLS:
DB_SSL_CA=
```

Copy `.env.example` then fill values. Do NOT commit `.env`.

## Run Backend
```bash
uvicorn app.main:app --reload
```
Docs:  
- Swagger: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc  

## Frontend (Local)
Open `frontend/index.html` directly or serve:
```bash
python -m http.server 8001 -d frontend
```

## Core Flow
1. Browse products (index/product pages)
2. Add to cart (localStorage)
3. Proceed to payment (payment.html)
4. Place order (calls `/orders/place`)
5. View transactions (transactions.html)
6. Seller can view aggregated orders (orders_seller.html)

## Key Endpoints (Examples)
```bash
# Products
GET  /products
GET  /products/{productid}
POST /products/add

# Categories
GET  /products/categories
GET  /products/categories/{categoryid}/subcategories

# Orders
POST /orders/place?customerid=100001&productid=2&qty=1
GET  /orders/{orderid}
PATCH /orders/{orderid}/status?new_status=Delivered

# Transactions
GET  /orders/{orderid}/transaction
POST /orders/{orderid}/transaction?amount=999&status=Completed
```

## Import SQL Backup
```powershell
mysql -h <HOST> -P <PORT> -u <USER> -p --ssl-mode=REQUIRED <DB_NAME> < .\app\database_backup\data_20251107_212518.sql
```

## Supabase (Images)
Replace placeholder anon key. Move key server-side for production (never expose real service keys in public HTML).

## Security Checklist
- Remove secrets from frontend (Supabase key)
- Hash passwords (bcrypt) if not already
- Restrict CORS origins
- Add rate limiting (e.g. slowapi)
- Validate all inputs (Pydantic schemas)
- Sanitize review text
- Use HTTPS everywhere
- Consider JWT or secure cookies (current token is simple)

## Troubleshooting
| Issue | Cause | Fix |
|-------|-------|-----|
| Pylance missing import | VS Code path | Add `"python.analysis.extraPaths": ["${workspaceFolder}"]` |
| 404 `/place` | Missing `/orders` prefix | Use `/orders/place` |
| Broken fonts | Incomplete link | Ensure full Google Fonts href |
| Storage upload fails | Bucket/key mismatch | Verify bucket, move key to env |

## Future Improvements
- Server-side cart persistence
- Pagination & filtering
- Admin analytics endpoints
- JWT auth refactor
- Automated tests (pytest + CI)

## License
Add a LICENSE file (MIT recommended).

## Disclaimer
Demo configuration only. Harden before production deployment.
// ...existing code...
