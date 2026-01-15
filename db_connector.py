import mysql.connector
from mysql.connector import pooling
from config import DB_CONFIG
import time

# Create connection pool
connection_pool = None

try:
    connection_pool = pooling.MySQLConnectionPool(**DB_CONFIG)
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")
    raise

def get_db_connection(max_retries=3, retry_delay=1):
    """Get a connection from the pool with retry logic"""
    for attempt in range(max_retries):
        try:
            return connection_pool.get_connection()
        except mysql.connector.Error as err:
            if attempt == max_retries - 1:
                raise
            print(f"Connection attempt {attempt + 1} failed: {err}")
            time.sleep(retry_delay)

def close_resources(cursor=None, connection=None):
    """Safely close database resources"""
    try:
        if cursor:
            cursor.close()
    except Exception as e:
        print(f"Error closing cursor: {e}")
    try:
        if connection and connection.is_connected():
            connection.close()
    except Exception as e:
        print(f"Error closing connection: {e}")
