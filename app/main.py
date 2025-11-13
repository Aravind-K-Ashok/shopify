from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.customer_router import router as customer_router
from app.routes.seller_router import router as seller_router
from app.routes.order_router import router as order_router
from app.routes.product_router import router as product_router
from app.routes.category_router import router as category_router

app = FastAPI(
    title="E-Commerce API",
    description="Backend API for customers, sellers, products, categories, and orders (PyMySQL version)",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "https://aravind-k-ashok.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_router)
app.include_router(seller_router)
app.include_router(order_router)
app.include_router(product_router)
app.include_router(category_router)

@app.get("/")
def home():
    return {
        "message": "🚀 E-Commerce API is running successfully!",
        "version": "2.0.0",
        "routes": [
            "/customers",
            "/sellers",
            "/orders",
            "/products",
            "/products/categories",
            "/products/subcategories",
        ],
    }

@app.get("/healthz")
def health_check():
    """Health check endpoint for Render and load balancers."""
    return {"status": "ok"}
