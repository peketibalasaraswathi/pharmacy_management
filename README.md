# pharmacy_management

A Flask-based Pharmacy Management System that helps manage medicines, track sales, and monitor expiry dates using a MySQL database.


# Features

Add and view medicines

Record medicine sales

Dashboard showing:

Medicines expiring in the next 30 days

Recent sales

Automatic database & table creation

MySQL connection pooling

Sample data insertion script


# Tech Stack

Backend: Python (Flask)

Database: MySQL

Frontend: HTML (Jinja2)

Config: Environment variables (python-dotenv)


# Project Structure
app.py
config.py
db_connector.py
insert_test_data.py
requirements.txt
models/
templates/


# Setup & Run
Install dependencies
pip install -r requirements.txt


# Configure database (.env)
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=pharma_db


# Run the application
python app.py

Open: http://127.0.0.1:5000/


# Insert Sample Data (Optional)
python insert_test_data.py


# Future Enhancements

Expiry alerts

Sales reports

User authentication

Inventory analytics
