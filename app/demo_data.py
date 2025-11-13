from app.database.database import SessionLocal
from app.services.order_service import place_order
from app.services.seller_service import update_stock

db = SessionLocal()

print(update_stock(db, product_id=1, seller_id=1, new_stock=5))

print(place_order(db, customer_id=1, product_id=1, qty=2, amount=149999.0))

print(place_order(db, customer_id=1, product_id=1, qty=10, amount=749995.0))
