from flask import Flask, render_template, request, redirect, url_for, flash
from models.medicine import Medicine
from models.sale import Sale
from db_connector import get_db_connection, close_resources
from config import DB_CONFIG
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize database and tables
with app.app_context():
    # First create database if it doesn't exist
    try:
        # Connect without specifying database
        temp_config = DB_CONFIG.copy()
        temp_config.pop('database', None)
        conn = mysql.connector.connect(**temp_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.commit()
        cursor.close()
        conn.close()
        
        # Now create tables
        Medicine.create_table()
        Sale.create_table()
        print("Database and tables initialized successfully")
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
        raise

@app.route('/')
def dashboard():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get medicines nearing expiry (within 30 days)
        cursor.execute("""
            SELECT * FROM medicines 
            WHERE expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
            ORDER BY expiry_date ASC
            LIMIT 5
        """)
        expiring_soon = cursor.fetchall()
        
        # Get recent sales
        cursor.execute("""
            SELECT s.id, m.name, s.quantity, s.sale_date 
            FROM sales s JOIN medicines m ON s.medicine_id = m.id
            ORDER BY s.sale_date DESC
            LIMIT 5
        """)
        recent_sales = cursor.fetchall()
        
        return render_template('dashboard.html', 
                            expiring_soon=expiring_soon,
                            recent_sales=recent_sales)
    except mysql.connector.Error as err:
        flash('Database error occurred', 'danger')
        return render_template('error.html', error=str(err))
    finally:
        close_resources(cursor, conn)

@app.route('/medicines')
def list_medicines():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM medicines ORDER BY name ASC")
        medicines = cursor.fetchall()
        return render_template('medicines.html', medicines=medicines)
    except mysql.connector.Error as err:
        flash('Database error occurred', 'danger')
        return render_template('error.html', error=str(err))
    finally:
        close_resources(cursor, conn)

@app.route('/medicines/add', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        try:
            medicine = Medicine(
                name=request.form['name'],
                batch_no=request.form['batch_no'],
                quantity=int(request.form['quantity']),
                price=float(request.form['price']),
                expiry_date=request.form['expiry_date'],
                supplier=request.form.get('supplier', '')
            )
            medicine.save()
            flash('Medicine added successfully!', 'success')
            return redirect(url_for('list_medicines'))
        except (mysql.connector.Error, ValueError) as err:
            flash(f'Error: {err}', 'danger')
    
    return render_template('add_medicine.html')

@app.route('/sales', methods=['GET', 'POST'])
def record_sale():
    if request.method == 'POST':
        try:
            sale = Sale(
                medicine_id=int(request.form['medicine_id']),
                quantity=int(request.form['quantity']),
                customer_info=request.form.get('customer_info', '')
            )
            sale.save()
            flash('Sale recorded successfully!', 'success')
            return redirect(url_for('dashboard'))
        except (mysql.connector.Error, ValueError) as err:
            flash(f'Error: {err}', 'danger')
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM medicines ORDER BY name ASC")
        medicines = cursor.fetchall()
        return render_template('record_sale.html', medicines=medicines)
    except mysql.connector.Error as err:
        flash('Database error occurred', 'danger')
        return render_template('error.html', error=str(err))
    finally:
        close_resources(cursor, conn)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error='Internal server error'), 500

if __name__ == '__main__':
    app.run(debug=True)
