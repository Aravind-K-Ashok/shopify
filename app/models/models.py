import pymysql
from pymysql.cursors import DictCursor
from dataclasses import dataclass, fields
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "ecomdb",
    "cursorclass": DictCursor
}

@dataclass
class Customer:
    customerid: int | None
    fname: str
    lname: str
    phoneno: str
    password_hash: str
    address: str
    pincode: str
    district: str
    state: str
    housename: str

@dataclass
class Seller:
    sellerid: int | None
    customerid: int
    rating: float

@dataclass
class Category:
    categoryid: int | None
    name: str

@dataclass
class SubCategory:
    subcategoryid: int | None
    name: str
    categoryid: int

@dataclass
class Product:
    productid: int | None
    product_name: str
    description: str
    sellerid: int
    subcategoryid: int
    rating: float
    stock: int
    price: float
    images_url: str

@dataclass
class Order:
    orderid: int | None
    customerid: int
    productid: int
    sellerid: int
    qty: int
    status: str

@dataclass
class Transaction:
    transid: int | None Primary key, auto-increment
    orderid: int
    customerid: int
    amount: float
    status: str
    transDate: datetime

    def __post_init__(self):
        if self.transid is None:
            self.transid = None


class DatabaseManager:
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()

    def _python_to_sql(self, py_type: type) -> str:
        """Convert Python type to MySQL type."""
        if py_type in (int, type(None)):
            return "INT"
        elif py_type is float:
            return "FLOAT"
        elif py_type is str:
            return "VARCHAR(255)"
        elif py_type is datetime:
            return "DATETIME"
        else:
            return "TEXT"

    def create_table_from_dataclass(self, cls):
        table_name = cls.__name__.lower() + "s"
        cols = []

        for f in fields(cls):
            col_name = f.name
            col_type = self._python_to_sql(f.type)

            if col_name == f"{cls.__name__.lower()}id" or (table_name == "transactions" and col_name == "transid"):
                cols.append(f"{col_name} INT AUTO_INCREMENT PRIMARY KEY")
            else:
                cols.append(f"{col_name} {col_type}")

        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        
        create_sql = f"CREATE TABLE {table_name} ({', '.join(cols)}) ENGINE=InnoDB;"
        print(f"Creating table: {table_name}")
        self.cursor.execute(create_sql)

        if table_name == "customers":
            self.cursor.execute("ALTER TABLE customers AUTO_INCREMENT = 100000;")
        elif table_name == "transactions":
            self.cursor.execute("ALTER TABLE transactions AUTO_INCREMENT = 1;")

        self.conn.commit()

    def add_foreign_keys(self):
        """Add foreign key relationships after tables are created."""
        fk_commands = [
            "ALTER TABLE sellers ADD CONSTRAINT fk_seller_customer FOREIGN KEY (customerid) REFERENCES customers(customerid) ON DELETE CASCADE ON UPDATE CASCADE;",
            "ALTER TABLE subcategories ADD CONSTRAINT fk_subcat_category FOREIGN KEY (categoryid) REFERENCES categories(categoryid) ON DELETE CASCADE ON UPDATE CASCADE;",
            "ALTER TABLE products ADD CONSTRAINT fk_product_seller FOREIGN KEY (sellerid) REFERENCES sellers(sellerid) ON DELETE CASCADE ON UPDATE CASCADE;",
            "ALTER TABLE products ADD CONSTRAINT fk_product_subcat FOREIGN KEY (subcategoryid) REFERENCES subcategories(subcategoryid) ON DELETE CASCADE ON UPDATE CASCADE;",
            "ALTER TABLE orders ADD CONSTRAINT fk_order_customer FOREIGN KEY (customerid) REFERENCES customers(customerid) ON DELETE CASCADE ON UPDATE CASCADE;",
            "ALTER TABLE orders ADD CONSTRAINT fk_order_product FOREIGN KEY (productid) REFERENCES products(productid) ON DELETE CASCADE ON UPDATE CASCADE;",
            "ALTER TABLE orders ADD CONSTRAINT fk_order_seller FOREIGN KEY (sellerid) REFERENCES sellers(sellerid) ON DELETE CASCADE ON UPDATE CASCADE;",
            "ALTER TABLE transactions ADD CONSTRAINT fk_trans_order FOREIGN KEY (orderid) REFERENCES orders(orderid) ON DELETE CASCADE ON UPDATE CASCADE;",
            "ALTER TABLE transactions ADD CONSTRAINT fk_trans_customer FOREIGN KEY (customerid) REFERENCES customers(customerid) ON DELETE CASCADE ON UPDATE CASCADE;"
        ]

        for cmd in fk_commands:
            try:
                self.cursor.execute(cmd)
            except pymysql.err.InternalError as e:
                if "errno: 1061" not in str(e):
                    print("⚠️", e)
        self.conn.commit()
        print("🔗 Foreign keys added successfully.")

    def create_all_tables(self, models: list):
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        for model in models:
            self.create_table_from_dataclass(model)
            
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("✅ All tables created successfully.")
        self.add_foreign_keys()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    models = [Customer, Seller, Category, SubCategory, Product, Order, Transaction]
    db = DatabaseManager()
    db.create_all_tables(models)
    db.close()
