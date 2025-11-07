import pymysql
from datetime import datetime
from app.database.database import get_connection


class OrderService:
    """Handles order management, status updates, and transactions using PyMySQL."""

    # 🟢 Place new order
    def place_order(self, customerid: int, productid: int, qty: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            # Validate customer
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", (customerid,))
            customer = cursor.fetchone()
            if not customer:
                return {"error": "❌ Customer not found"}

            # Validate product
            cursor.execute("SELECT * FROM products WHERE productid = %s", (productid,))
            product = cursor.fetchone()
            if not product:
                return {"error": "❌ Product not found"}

            if product["stock"] < qty:
                return {"error": f"❌ Not enough stock for '{product['description']}' (Available: {product['stock']})"}

            # Deduct stock
            new_stock = product["stock"] - qty
            cursor.execute("UPDATE products SET stock = %s WHERE productid = %s", (new_stock, productid))

            # Create order
            cursor.execute("""
                INSERT INTO orders (customerid, productid, sellerid, qty, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (customerid, productid, product["sellerid"], qty, "Pending"))
            orderid = cursor.lastrowid

            # Get product price and calculate total amount
            cursor.execute("SELECT price FROM products WHERE productid = %s", (productid,))
            product_price = cursor.fetchone()["price"]
            amount = float(qty * product_price)

            # Create transaction and mark payment as completed immediately
            cursor.execute("""
                INSERT INTO transactions (orderid, customerid, amount, status, transDate)
                VALUES (%s, %s, %s, %s, %s)
            """, (orderid, customerid, amount, "Completed", datetime.utcnow()))

            conn.commit()
            return {"message": f"✅ Order {orderid} placed successfully. Payment of ₹{amount:.2f} completed."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    # 🔍 Get order details
    def get_order_details(self, orderid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM orders WHERE orderid = %s", (orderid,))
            order = cursor.fetchone()
            return order if order else {"error": "❌ Order not found"}
        finally:
            cursor.close()
            conn.close()

    # 🔍 Get all orders by customer
    def get_orders_by_customer(self, customerid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM orders WHERE customerid = %s", (customerid,))
            orders = cursor.fetchall()
            return orders if orders else {"message": "No orders found for this customer."}
        finally:
            cursor.close()
            conn.close()

    # 🔍 Get all orders by seller
    def get_orders_by_seller(self, sellerid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM orders WHERE sellerid = %s", (sellerid,))
            orders = cursor.fetchall()
            return orders if orders else {"message": "No orders found for this seller."}
        finally:
            cursor.close()
            conn.close()

    # 🚚 Update order status
    def update_order_status(self, orderid: int, new_status: str):
        valid_statuses = ["Pending", "Dispatched", "On The Way", "Delivered", "Cancelled"]
        if new_status not in valid_statuses:
            return {"error": f"Invalid status '{new_status}'. Valid: {valid_statuses}"}

        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM orders WHERE orderid = %s", (orderid,))
            order = cursor.fetchone()
            if not order:
                return {"error": "❌ Order not found"}
            if order["status"] == "Cancelled":
                return {"error": "❌ Cannot change status of a cancelled order"}

            cursor.execute("UPDATE orders SET status = %s WHERE orderid = %s", (new_status, orderid))

            # Auto-update transaction if delivered
            if new_status == "Delivered":
                cursor.execute("UPDATE transactions SET status = %s WHERE orderid = %s", ("Completed", orderid))

            conn.commit()
            return {"message": f"🚚 Order {orderid} status updated to '{new_status}'."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    # 🟥 Cancel order
    def cancel_order(self, orderid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM orders WHERE orderid = %s", (orderid,))
            order = cursor.fetchone()
            if not order:
                return {"error": "❌ Order not found"}

            if order["status"] in ["Dispatched", "On The Way", "Delivered"]:
                return {"error": "❌ Order cannot be cancelled after dispatch"}

            cursor.execute("UPDATE orders SET status = 'Cancelled' WHERE orderid = %s", (orderid,))

            # Return stock
            cursor.execute("UPDATE products SET stock = stock + %s WHERE productid = %s", (order["qty"], order["productid"]))

            # Update transaction
            cursor.execute("UPDATE transactions SET status = 'Refunded' WHERE orderid = %s", (orderid,))

            conn.commit()
            return {"message": f"❌ Order {orderid} cancelled successfully and refund initiated."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    # 💳 Create or update transaction
    def create_or_update_transaction(self, orderid: int, amount: float, status: str = "Completed"):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM orders WHERE orderid = %s", (orderid,))
            order = cursor.fetchone()
            if not order:
                return {"error": "❌ Order not found"}

            cursor.execute("SELECT * FROM transactions WHERE orderid = %s", (orderid,))
            trans = cursor.fetchone()

            if trans:
                cursor.execute("""
                    UPDATE transactions
                    SET amount = %s, status = %s, transDate = %s
                    WHERE orderid = %s
                """, (amount, status, datetime.utcnow(), orderid))
            else:
                cursor.execute("""
                    INSERT INTO transactions (orderid, customerid, amount, status, transDate)
                    VALUES (%s, %s, %s, %s, %s)
                """, (orderid, order["customerid"], amount, status, datetime.utcnow()))

            conn.commit()
            return {"message": f"💳 Transaction for order {orderid} recorded as '{status}' (₹{amount:.2f})."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    # 💵 Get transaction for an order
    def get_transaction_for_order(self, orderid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM transactions WHERE orderid = %s", (orderid,))
            trans = cursor.fetchone()
            return trans if trans else {"message": "No transaction found for this order."}
        finally:
            cursor.close()
            conn.close()

    # 📜 Get all transactions for a customer
    def get_transactions_by_customer(self, customerid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM transactions WHERE customerid = %s", (customerid,))
            trans = cursor.fetchall()
            return trans if trans else {"message": "No transactions found for this customer."}
        finally:
            cursor.close()
            conn.close()
