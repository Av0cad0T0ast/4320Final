from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret_key"

def get_cost_matrix():
    return [[100, 75, 50, 100] for _ in range(12)]

DATABASE = 'reservations.db'

def get_db_connection():
    pass

@app.route('/')
def index():
    pass

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    pass

@app.route('/admin/portal')
def admin_portal():
    pass

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    pass

def generate_seating_chart(reservations):
    pass

def calculate_total_sales(reservations):
    pass

if __name__ == '__main__':
    
    app.run(debug=True)