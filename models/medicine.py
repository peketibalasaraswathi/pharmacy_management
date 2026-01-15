from db_connector import get_db_connection, close_resources
from contextlib import contextmanager
import mysql.connector

class Medicine:
    def __init__(self, name, batch_no, quantity, price, expiry_date, supplier):
        self.name = name
        self.batch_no = batch_no
        self.quantity = quantity
        self.price = price
        self.expiry_date = expiry_date
        self.supplier = supplier

    @staticmethod
    @contextmanager
    def db_cursor():
        """Context manager for database operations"""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise
        finally:
            close_resources(cursor, conn)

    @staticmethod
    def create_table():
        """Create medicines table if not exists"""
        try:
            with Medicine.db_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS medicines (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        batch_no VARCHAR(50) UNIQUE NOT NULL,
                        quantity INT NOT NULL,
                        price DECIMAL(10,2) NOT NULL,
                        expiry_date DATE NOT NULL,
                        supplier VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        except mysql.connector.Error as err:
            print(f"Error creating medicines table: {err}")
            raise

    def save(self):
        """Save medicine to database"""
        try:
            with Medicine.db_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO medicines (name, batch_no, quantity, price, expiry_date, supplier)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (self.name, self.batch_no, self.quantity, self.price, 
                     self.expiry_date, self.supplier))
        except mysql.connector.Error as err:
            print(f"Error saving medicine: {err}")
            raise
