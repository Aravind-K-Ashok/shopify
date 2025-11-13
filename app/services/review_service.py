import pymysql
from datetime import datetime
from app.database.database import get_connection


class ReviewService:
    """Handles storing and retrieving product reviews."""

    def ensure_table(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    reviewid INT AUTO_INCREMENT PRIMARY KEY,
                    productid INT NOT NULL,
                    customerid INT NOT NULL,
                    rating INT NOT NULL,
                    comment TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX(productid),
                    INDEX(customerid)
                ) ENGINE=InnoDB;
            """)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_reviews(self, productid: int, page: int = 1, per_page: int = 10):
        self.ensure_table()
        offset = (page - 1) * per_page
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT COUNT(*) AS cnt FROM reviews WHERE productid = %s", (productid,))
            total = cursor.fetchone().get('cnt', 0)

            cursor.execute("SELECT AVG(rating) AS avg_rating FROM reviews WHERE productid = %s", (productid,))
            avg_row = cursor.fetchone() or {}
            avg_rating = float(avg_row.get('avg_rating')) if avg_row and avg_row.get('avg_rating') is not None else 0.0

            cursor.execute(
                "SELECT r.*, c.fname, c.lname FROM reviews r LEFT JOIN customers c ON r.customerid = c.customerid WHERE r.productid = %s ORDER BY r.created_at DESC LIMIT %s OFFSET %s",
                (productid, per_page, offset)
            )
            rows = cursor.fetchall()
            for r in rows:
                r['name'] = ((r.get('fname') or '') + ' ' + (r.get('lname') or '')).strip() or None
            return {"reviews": rows, "total": total, "avg_rating": avg_rating}
        finally:
            cursor.close()
            conn.close()

    def add_review(self, productid: int, customerid: int, rating: int, comment: str):
        self.ensure_table()
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM orders WHERE productid = %s AND customerid = %s", (productid, customerid))
            order = cursor.fetchone()
            if not order:
                return {"error": "You can only review products you have purchased."}

            cursor.execute("INSERT INTO reviews (productid, customerid, rating, comment, created_at) VALUES (%s, %s, %s, %s, %s)",
                           (productid, customerid, int(rating), comment, datetime.utcnow()))
            conn.commit()
            return {"message": "Review submitted successfully."}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()
