from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
import time

app = Flask(__name__)
app.secret_key = "secret_key"

def get_cost_matrix():
    return [[100, 75, 50, 100] for _ in range(12)]

DATABASE = 'reservations.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    
    conn.row_factory = sqlite3.Row
    
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        userOption = request.form.get('choice')

        if userOption == "reserve":
            return redirect(url_for('reservation'))
        elif userOption == "admin":
            return redirect(url_for('admin'))
        else:
            flash('Something went wrong. Please select a choice.')
            return redirect(url_for('index'))
    
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
def  reservationcodeMaker(firstName):
    timeaddOn = int(time.time()) % 1000
    return f"{firstName}{timeaddOn}TC4320"
    
@app.route('/reservation', methods=['GET', 'POST'])
def reservation():

    if request.method== 'POST':

        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        seatRow = request.form.get('seat_row')
        seatColumn = request.form.get('seat_column')

        if not firstName or not lastName or not seatRow or not seatColumn:
            flash ("You must fill out all fields.")
            return redirect(url_for('reservation'))
        
        try:
            seatRow = int(seatRow)-1
            seatColumn = int(seatColumn)-1
            if not( 0<= seatRow <12 )or not (0 <= seatColumn <4):
                raise ValueError
        except ValueError:
            flash("Selected seat is not valid...Please pick a valid seat :)")
            return redirect(url_for('reservation'))
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM reservations WHERE seatRow = ? AND seatColumn = ?", (seatRow,seatColumn))
        if cursor.fetchone():
            flash("Unfortunately selected seat is already reserved! Please pick another seat.")
            conn.close()
            return redirect(url_for('reservation'))
        
        reservationCode = reservationcodeMaker(firstName)
        
        cursor.execute(
            "INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber) VALUES(?,?,?,?)",
            (firstName,seatRow,seatColumn,reservationCode)
        )

        conn.commit()
        conn.close()
        flash (f"Yay! Reservation was succefful. Here is your reservation code: {reservationCode}. Please make sure to save it!")
    
    conn = get_db_connection()
    seatingChart, _ = generate_seating_chart_and_sales(conn)
    conn.close()

    return render_template('reservation.html', seating_chart =seatingChart)


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