from db_connector import get_db_connection, close_resources
from contextlib import contextmanager
from datetime import datetime
import mysql.connector

class Sale:
    def __init__(self, medicine_id, quantity, customer_info=None):
        self.medicine_id = medicine_id
        self.quantity = quantity
        self.customer_info = customer_info
        self.sale_date = datetime.now().date()

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
        """Create sales table if not exists"""
        try:
            with Sale.db_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sales (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        medicine_id INT NOT NULL,
                        quantity INT NOT NULL,
                        sale_date DATE NOT NULL,
                        customer_info TEXT,
                        FOREIGN KEY (medicine_id) REFERENCES medicines(id)
                    )
                """)
        except mysql.connector.Error as err:
            print(f"Error creating sales table: {err}")
            raise

    def save(self):
        """Save sale record to database"""
        try:
            with Sale.db_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO sales (medicine_id, quantity, sale_date, customer_info)
                    VALUES (%s, %s, %s, %s)
                """, (self.medicine_id, self.quantity, self.sale_date, self.customer_info))
        except mysql.connector.Error as err:
            print(f"Error saving sale: {err}")
            raise
