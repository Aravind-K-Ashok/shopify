from app.database.database import get_connection
import pymysql


class CategoryService:
    def add_category(self, name: str):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM categories WHERE name = %s", (name,))
            existing = cursor.fetchone()
            if existing:
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

    def update_category(self, category_id: int, new_name: str):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM categories WHERE categoryid = %s", (category_id,))
            category = cursor.fetchone()
            if not category:
                return {"error": "❌ Category not found."}

            cursor.execute(
                "UPDATE categories SET name = %s WHERE categoryid = %s",
                (new_name, category_id),
            )
            conn.commit()
            return {"message": f"📝 Category ID {category_id} updated to '{new_name}'."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def delete_category(self, category_id: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM categories WHERE categoryid = %s", (category_id,))
            category = cursor.fetchone()
            if not category:
                return {"error": "❌ Category not found."}

            cursor.execute("DELETE FROM subcategories WHERE categoryid = %s", (category_id,))
            cursor.execute("DELETE FROM categories WHERE categoryid = %s", (category_id,))
            conn.commit()
            return {
                "message": f"🗑️ Category '{category['name']}' and its subcategories deleted successfully."
            }
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_all_categories(self):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM categories")
            categories = cursor.fetchall()
            return categories or []
        finally:
            cursor.close()
            conn.close()

    def add_subcategory(self, category_id: int, name: str):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM categories WHERE categoryid = %s", (category_id,))
            category = cursor.fetchone()
            if not category:
                return {"error": "❌ Parent category not found."}

            cursor.execute(
                "SELECT * FROM subcategories WHERE name = %s AND categoryid = %s",
                (name, category_id),
            )
            existing = cursor.fetchone()
            if existing:
                return {"error": "❌ Subcategory already exists under this category."}

            cursor.execute(
                "INSERT INTO subcategories (name, categoryid) VALUES (%s, %s)",
                (name, category_id),
            )
            conn.commit()
            return {"message": f"✅ Subcategory '{name}' added under '{category['name']}'."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def update_subcategory(self, subcategory_id: int, new_name: str):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM subcategories WHERE subcategoryid = %s", (subcategory_id,))
            subcategory = cursor.fetchone()
            if not subcategory:
                return {"error": "❌ Subcategory not found."}

            cursor.execute(
                "UPDATE subcategories SET name = %s WHERE subcategoryid = %s",
                (new_name, subcategory_id),
            )
            conn.commit()
            return {"message": f"📝 Subcategory ID {subcategory_id} updated to '{new_name}'."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def delete_subcategory(self, subcategory_id: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM subcategories WHERE subcategoryid = %s", (subcategory_id,))
            subcategory = cursor.fetchone()
            if not subcategory:
                return {"error": "❌ Subcategory not found."}

            cursor.execute("DELETE FROM subcategories WHERE subcategoryid = %s", (subcategory_id,))
            conn.commit()
            return {"message": f"🗑️ Subcategory '{subcategory['name']}' deleted successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_subcategories_by_category(self, category_id: int):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM subcategories WHERE categoryid = %s", (category_id,))
            subcategories = cursor.fetchall()
            return subcategories or []
        finally:
            cursor.close()
            conn.close()
