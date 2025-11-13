import pymysql
from app.database.database import get_connection

class ProductService:
    """Handles product, category, subcategory, and product management using PyMySQL."""

    def add_category(self, name: str):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM categories WHERE name = %s", (name,))
            if cursor.fetchone():
                return {"error": "❌ Category already exists."}

            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
            conn.commit()
            return {"message": f"✅ Category '{name}' added successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def update_category(self, categoryid: int, new_name: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE categories SET name = %s WHERE categoryid = %s",
                (new_name, categoryid),
            )
            if cursor.rowcount == 0:
                return {"error": "❌ Category not found."}
            conn.commit()
            return {"message": f"📝 Category ID {categoryid} updated to '{new_name}'."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def delete_category(self, categoryid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM categories WHERE categoryid = %s", (categoryid,))
            cat = cursor.fetchone()
            if not cat:
                return {"error": "❌ Category not found."}

            cursor.execute("DELETE FROM categories WHERE categoryid = %s", (categoryid,))
            conn.commit()
            return {"message": f"🗑️ Category '{cat['name']}' deleted successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    
    def list_products(self, subcategoryid=None):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT 
                productid,
                sellerid,
                name AS product_name,
                description,
                subcategoryid,
                price,
                stock,
                images_url,
                rating
            FROM products
            """
            params = ()
            if subcategoryid:
                query += " WHERE subcategoryid = %s"
                params = (subcategoryid,)

            cursor.execute(query, params)
            products = cursor.fetchall()
            return products or []
        finally:
            cursor.close()
            conn.close()

    def add_subcategory(self, name: str, categoryid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM categories WHERE categoryid = %s", (categoryid,))
            cat = cursor.fetchone()
            if not cat:
                return {"error": "❌ Parent category not found."}

            cursor.execute(
                "SELECT * FROM subcategories WHERE name = %s AND categoryid = %s",
                (name, categoryid),
            )
            if cursor.fetchone():
                return {"error": "❌ Subcategory already exists under this category."}

            cursor.execute(
                "INSERT INTO subcategories (name, categoryid) VALUES (%s, %s)",
                (name, categoryid),
            )
            conn.commit()
            return {"message": f"✅ Subcategory '{name}' added under '{cat['name']}'."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def update_subcategory(self, subcategoryid: int, new_name: str):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE subcategories SET name = %s WHERE subcategoryid = %s",
                (new_name, subcategoryid),
            )
            if cursor.rowcount == 0:
                return {"error": "❌ Subcategory not found."}
            conn.commit()
            return {"message": f"📝 Subcategory ID {subcategoryid} updated to '{new_name}'."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def delete_subcategory(self, subcategoryid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(
                "SELECT * FROM subcategories WHERE subcategoryid = %s", (subcategoryid,)
            )
            sub = cursor.fetchone()
            if not sub:
                return {"error": "❌ Subcategory not found."}

            cursor.execute("DELETE FROM subcategories WHERE subcategoryid = %s", (subcategoryid,))
            conn.commit()
            return {"message": f"🗑️ Subcategory '{sub['name']}' deleted successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def list_subcategories(self, categoryid: int = None):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            if categoryid:
                cursor.execute(
                    "SELECT * FROM subcategories WHERE categoryid = %s", (categoryid,)
                )
            else:
                cursor.execute("SELECT * FROM subcategories")
            data = cursor.fetchall()
            return data if data else {"message": "No subcategories found."}
        finally:
            cursor.close()
            conn.close()

    def add_product(
        self,
        sellerid: int,
        product_name: str,
        description: str,
        subcategoryid: int,
        price: float,
        stock: int,
        images_url: str,
        rating: float = 0.0,
    ):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(
                "SELECT * FROM sellers WHERE sellerid = %s OR customerid = %s",
                (sellerid, sellerid),
            )
            seller = cursor.fetchone()
            if not seller:
                return {
                    "error": f"❌ Seller not found for ID {sellerid}. Please register as a seller first."
                }

            real_sellerid = seller["sellerid"]

            cursor.execute(
                "SELECT * FROM subcategories WHERE subcategoryid = %s", (subcategoryid,)
            )
            if not cursor.fetchone():
                return {"error": "❌ Subcategory not found."}

            cursor.execute(
                """
                INSERT INTO products (product_name, description, sellerid, subcategoryid, price, stock, images_url, rating)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    product_name,
                    description,
                    real_sellerid,
                    subcategoryid,
                    price,
                    stock,
                    images_url,
                    rating,
                ),
            )
            conn.commit()
            return {"message": f"✅ Product '{product_name}' added successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def update_product(self, productid: int, description: str = None, stock: int = None, rating: float = None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            updates = []
            values = []

            if description is not None:
                updates.append("description = %s")
                values.append(description)
            if stock is not None:
                updates.append("stock = %s")
                values.append(stock)
            if rating is not None:
                updates.append("rating = %s")
                values.append(rating)

            if not updates:
                return {"error": "❌ No fields to update."}

            sql = f"UPDATE products SET {', '.join(updates)} WHERE productid = %s"
            values.append(productid)
            cursor.execute(sql, tuple(values))
            if cursor.rowcount == 0:
                return {"error": "❌ Product not found."}

            conn.commit()
            return {"message": f"📝 Product ID {productid} updated successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def delete_product(self, productid: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM products WHERE productid = %s", (productid,))
            product = cursor.fetchone()
            if not product:
                return {"error": "❌ Product not found."}

            cursor.execute("DELETE FROM products WHERE productid = %s", (productid,))
            conn.commit()
            return {"message": f"🗑️ Product '{product['product_name']}' deleted successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_product(self, productid: int):
        """Return a single product by id (dict) or None if not found."""
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(
                """
                SELECT
                    productid,
                    sellerid,
                    product_name,
                    description,
                    subcategoryid,
                    price,
                    stock,
                    images_url,
                    rating
                FROM products
                WHERE productid = %s
                """,
                (productid,)
            )
            product = cursor.fetchone()
            return product
        finally:
            cursor.close()
            conn.close()

    def list_products(self, subcategoryid: int = None):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            if subcategoryid:
                cursor.execute("SELECT * FROM products WHERE subcategoryid = %s", (subcategoryid,))
            else:
                cursor.execute("SELECT * FROM products")
            data = cursor.fetchall()
            return data if data else {"message": "No products found."}
        finally:
            cursor.close()
            conn.close()

    def search_products(self, keyword: str):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(
                "SELECT * FROM products WHERE product_name LIKE %s OR description LIKE %s",
                (f"%{keyword}%", f"%{keyword}%"),
            )
            data = cursor.fetchall()
            return data if data else {"message": f"No products found matching '{keyword}'."}
        finally:
            cursor.close()
            conn.close()
