import pymysql
from app.database.database import get_connection


class SellerService:
    """Handles seller registration, product management, and order updates using PyMySQL."""

    def register_seller(self, customerid: int, rating: float = 0.0):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", (customerid,))
            if not cursor.fetchone():
                return {"error": "❌ Customer ID not found."}

            cursor.execute("SELECT * FROM sellers WHERE customerid = %s", (customerid,))
            if cursor.fetchone():
                return {"error": "❌ This customer is already a seller."}

            cursor.execute(
                "INSERT INTO sellers (customerid, rating) VALUES (%s, %s)",
                (customerid, rating),
            )
            conn.commit()
            return {"message": "✅ Seller registered successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def add_product(self, sellerid: int, description: str, subcategoryid: int, stock: int, rating: float = 0.0):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM sellers WHERE sellerid = %s", (sellerid,))
            if not cursor.fetchone():
                return {"error": "❌ Seller not found."}

            cursor.execute("SELECT * FROM subcategories WHERE subcategoryid = %s", (subcategoryid,))
            if not cursor.fetchone():
                return {"error": "❌ Invalid subcategory."}

            cursor.execute("""
                INSERT INTO products (description, sellerid, subcategoryid, stock, rating)
                VALUES (%s, %s, %s, %s, %s)
            """, (description, sellerid, subcategoryid, stock, rating))
            conn.commit()
            return {"message": f"✅ Product '{description}' added successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def update_product(self, sellerid: int, productid: int, description=None, subcategoryid=None, rating=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM products WHERE productid = %s AND sellerid = %s", (productid, sellerid))
            if not cursor.fetchone():
                return {"error": "❌ Product not found or not owned by seller."}

            updates = []
            values = []
            if description:
                updates.append("description = %s")
                values.append(description)
            if subcategoryid:
                cursor.execute("SELECT * FROM subcategories WHERE subcategoryid = %s", (subcategoryid,))
                if not cursor.fetchone():
                    return {"error": "❌ Invalid subcategory."}
                updates.append("subcategoryid = %s")
                values.append(subcategoryid)
            if rating is not None:
                updates.append("rating = %s")
                values.append(rating)

            if not updates:
                return {"error": "❌ No fields to update."}

            sql = f"UPDATE products SET {', '.join(updates)} WHERE productid = %s AND sellerid = %s"
            values.extend([productid, sellerid])
            cursor.execute(sql, tuple(values))
            conn.commit()
            return {"message": f"✅ Product {productid} updated successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def delete_product(self, sellerid: int, productid: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM products WHERE productid = %s AND sellerid = %s", (productid, sellerid))
            if not cursor.fetchone():
                return {"error": "❌ Product not found or not owned by seller."}

            cursor.execute("DELETE FROM products WHERE productid = %s AND sellerid = %s", (productid, sellerid))
            conn.commit()
            return {"message": f"🗑️ Product {productid} deleted successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_seller_products(self, sellerid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM products WHERE sellerid = %s", (sellerid,))
            products = cursor.fetchall()
            return products if products else {"message": "No products found."}
        finally:
            cursor.close()
            conn.close()

    def update_stock(self, sellerid: int, productid: int, new_stock: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE products SET stock = %s WHERE productid = %s AND sellerid = %s",
                           (new_stock, productid, sellerid))
            if cursor.rowcount == 0:
                return {"error": "❌ Product not found or not owned by seller."}
            conn.commit()
            return {"message": f"✅ Stock updated to {new_stock}."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def change_stock(self, sellerid: int, productid: int, delta: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT stock FROM products WHERE productid = %s AND sellerid = %s", (productid, sellerid))
            prod = cursor.fetchone()
            if not prod:
                return {"error": "❌ Product not found."}

            new_stock = prod["stock"] + delta
            if new_stock < 0:
                return {"error": "❌ Stock cannot go below zero."}

            cursor.execute("UPDATE products SET stock = %s WHERE productid = %s AND sellerid = %s",
                           (new_stock, productid, sellerid))
            conn.commit()
            return {"message": f"✅ Stock adjusted by {delta}. New stock: {new_stock}"}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_seller_orders(self, sellerid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT o.*, p.price AS product_price, t.amount AS transaction_amount, t.status AS transaction_status, t.transDate AS transaction_date,
                       c.fname, c.lname
                FROM orders o
                LEFT JOIN products p ON o.productid = p.productid
                LEFT JOIN transactions t ON o.orderid = t.orderid
                LEFT JOIN customers c ON o.customerid = c.customerid
                WHERE o.sellerid = %s
            """, (sellerid,))
            rows = cursor.fetchall()
            if not rows:
                return {"message": "No orders found."}

            orders = []
            for r in rows:
                order = dict(r)
                if order.get('transaction_amount') is not None:
                    order['total_amount'] = float(order['transaction_amount'])
                else:
                    price = order.get('product_price') or 0
                    qty = order.get('qty') or 1
                    order['total_amount'] = float(qty) * float(price)

                order['items_count'] = int(order.get('qty') or 1)
                order['customer_name'] = ((order.get('fname') or '') + ' ' + (order.get('lname') or '')).strip() or None
                order['order_date'] = order.get('transaction_date') or order.get('order_date') or order.get('created_at') or None
                orders.append(order)

            return orders
        finally:
            cursor.close()
            conn.close()

    def update_order_status(self, sellerid: int, orderid: int, new_status: str):
        valid_status = ["Pending", "Dispatched", "On The Way", "Delivered", "Cancelled"]
        if new_status not in valid_status:
            return {"error": f"❌ Invalid status. Choose from: {valid_status}"}

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM orders WHERE orderid = %s AND sellerid = %s", (orderid, sellerid))
            if not cursor.fetchone():
                return {"error": "❌ Order not found or does not belong to this seller."}

            cursor.execute("UPDATE orders SET status = %s WHERE orderid = %s AND sellerid = %s",
                           (new_status, orderid, sellerid))
            conn.commit()
            return {"message": f"🚚 Order {orderid} status updated to '{new_status}'."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_seller_profile(self, sellerid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM sellers WHERE sellerid = %s", (sellerid,))
            seller = cursor.fetchone()
            return seller if seller else {"error": "❌ Seller not found."}
        finally:
            cursor.close()
            conn.close()

    def get_seller_by_customer(self, customerid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM sellers WHERE customerid = %s", (customerid,))
            seller = cursor.fetchone()
            return seller if seller else {"error": "❌ Seller not found for this customer."}
        finally:
            cursor.close()
            conn.close()

    def update_seller_rating(self, sellerid: int, new_rating: float):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE sellers SET rating = %s WHERE sellerid = %s", (new_rating, sellerid))
            if cursor.rowcount == 0:
                return {"error": "❌ Seller not found."}
            conn.commit()
            return {"message": f"⭐ Seller {sellerid} rating updated to {new_rating}"}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()
