import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.database import get_connection


class CustomerService:
    """Handles customer registration, authentication, and profile management using PyMySQL."""

    def register_customer(self, fname, lname, phoneno, password, address, pincode, district, state, housename):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM customers WHERE phoneno = %s", (phoneno,))
            if cursor.fetchone():
                return {"error": "❌ Phone number already registered"}

            hashed_password = generate_password_hash(password)

            cursor.execute("""
                INSERT INTO customers 
                (fname, lname, phoneno, password_hash, address, pincode, district, state, housename)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (fname, lname, phoneno, hashed_password, address, pincode, district, state, housename))

            conn.commit()

            customer_id = cursor.lastrowid

            return {
                "message": f"✅ Customer {fname} {lname} registered successfully!",
                "customerid": customer_id
            }

        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()


    def authenticate_customer(self, customerID, password):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", (customerID,))
            customer = cursor.fetchone()
            if not customer or not check_password_hash(customer["password_hash"], password):
                return {"error": "❌ Invalid Customer ID or Password"}
            return {"message": f"✅ Customer {customer['fname']} {customer['lname']} login successful"}
        finally:
            cursor.close()
            conn.close()

    def get_customer_details(self, customerID):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", (customerID,))
            customer = cursor.fetchone()
            if not customer:
                return {"error": "❌ Customer not found"}
            return {"customer": customer}
        finally:
            cursor.close()
            conn.close()

    def update_customer_phone(self, customerID, newphoneno):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", (customerID,))
            if not cursor.fetchone():
                return {"error": "❌ Customer not found"}

            cursor.execute("UPDATE customers SET phoneno = %s WHERE customerid = %s", (newphoneno, customerID))
            conn.commit()
            return {"message": f"✅ Phone number updated successfully"}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def update_customer_address(self, customerID, newaddress, newpincode, newdistrict, newstate, newhousename):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", (customerID,))
            if not cursor.fetchone():
                return {"error": "❌ Customer not found"}

            cursor.execute("""
                UPDATE customers 
                SET address = %s, pincode = %s, district = %s, state = %s, housename = %s 
                WHERE customerid = %s
            """, (newaddress, newpincode, newdistrict, newstate, newhousename, customerID))
            conn.commit()
            return {"message": f"✅ Address updated successfully"}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def change_customer_password(self, customerID, oldpassword, newpassword):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", (customerID,))
            customer = cursor.fetchone()
            if not customer:
                return {"error": "❌ Customer not found"}
            if not check_password_hash(customer["password_hash"], oldpassword):
                return {"error": "❌ Old password is incorrect"}

            hashed = generate_password_hash(newpassword)
            cursor.execute("UPDATE customers SET password_hash = %s WHERE customerid = %s", (hashed, customerID))
            conn.commit()
            return {"message": f"✅ Password changed successfully"}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def delete_customer(self, customerID):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", (customerID,))
            customer = cursor.fetchone()
            if not customer:
                return {"error": "❌ Customer not found"}

            cursor.execute("DELETE FROM customers WHERE customerid = %s", (customerID,))
            conn.commit()
            return {"message": f"🗑️ Customer deleted successfully"}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def change_phone_password(self, customerID, phoneno, newpassword):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM customers WHERE customerid = %s AND phoneno = %s", (customerID, phoneno))
            customer = cursor.fetchone()
            if not customer:
                return {"error": "❌ Customer not found or phone number does not match"}

            hashed = generate_password_hash(newpassword)
            cursor.execute("UPDATE customers SET password_hash = %s WHERE customerid = %s", (hashed, customerID))
            conn.commit()
            return {"message": f"✅ Password changed successfully"}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()

    def change_name(self, customerID, newfname, newlname):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", (customerID,))
            if not cursor.fetchone():
                return {"error": "❌ Customer not found"}

            cursor.execute("UPDATE customers SET fname = %s, lname = %s WHERE customerid = %s", (newfname, newlname, customerID))
            conn.commit()
            return {"message": f"✅ Customer name updated to {newfname} {newlname}"}
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            conn.close()
