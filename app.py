from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret_key"

def get_cost_matrix():
    return [[100, 75, 50, 100] for _ in range(12)]

DATABASE = 'reservations.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    
    conn.row_factory = sqlite3.Row
    
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    
    conn.close()
    
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    seating_chart = None
    total_sales = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            flash("Username required", "error")
            return render_template('admin.html', seating_chart=seating_chart, total_sales=total_sales)
        if not password:
            flash("Password required", "error")
            return render_template('admin.html', seating_chart=seating_chart, total_sales=total_sales)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admins WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result['password']
            if password == stored_password:
                flash("Login successful", "success")
                # Generate seating chart and total sales
                seating_chart, total_sales = generate_seating_chart_and_sales(conn)
            else:
                flash("Invalid username or password combination", "error")
        else:
            flash("Invalid username or password combination", "error")

        conn.close()

    return render_template('admin.html', seating_chart=seating_chart, total_sales=total_sales)



@app.route('/admin/portal')
def admin_portal():
    pass

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    pass

def generate_seating_chart_and_sales(conn):
    
    # Fetch reserved seats
    cursor = conn.cursor()
    cursor.execute("SELECT seatRow, seatColumn FROM reservations")
    reserved_seats = cursor.fetchall()

    # Initialize seating chart and cost matrix
    rows, cols = 12, 4
    cost_matrix = [[100, 75, 50, 100] for _ in range(rows)]
    seating_chart = [['O' for _ in range(cols)] for _ in range(rows)]

    # Mark reserved seats and calculate total sales
    total_sales = 0
    for seat in reserved_seats:
        row, col = seat['seatRow'], seat['seatColumn']
        seating_chart[row][col] = 'X'
        total_sales += cost_matrix[row][col]

    return seating_chart, total_sales


if __name__ == '__main__':
    
    app.run(debug=True)