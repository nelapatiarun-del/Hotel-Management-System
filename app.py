
import sqlite3
from flask import Flask, render_template, request, redirect
from database import create_database

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('login.html')

create_database()


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'admin123':
        return redirect('/dashboard')
    else:
        return "Invalid Username or Password"


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/customers', methods=['GET', 'POST'])
def customers():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute(
            "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone)
        )
        conn.commit()

    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()
    conn.close()

    return render_template('customers.html', customers=data)


@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    if request.method == 'POST':
        room_no = request.form['room_no']
        room_type = request.form['room_type']
        price = request.form['price']
        status = request.form['status']

        cursor.execute(
            """INSERT INTO rooms
            (room_no, room_type, price, status)
            VALUES (?, ?, ?, ?)""",
            (room_no, room_type, price, status)
        )
        conn.commit()

    cursor.execute("SELECT * FROM rooms")
    data = cursor.fetchall()
    conn.close()

    return render_template('rooms.html', rooms=data)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    if request.method == 'POST':
        customer = request.form['customer']
        room_no = request.form['room_no']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        status = request.form['status']

        cursor.execute(
            """INSERT INTO bookings
            (customer, room_no, checkin, checkout, status)
            VALUES (?, ?, ?, ?, ?)""",
            (customer, room_no, checkin, checkout, status)
        )
        conn.commit()

    cursor.execute("SELECT * FROM bookings")
    data = cursor.fetchall()
    conn.close()

    return render_template('booking.html', bookings=data)


@app.route('/payments', methods=['GET', 'POST'])
def payments():

    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    if request.method == 'POST':
        customer = request.form['customer']
        amount = request.form['amount']
        method = request.form['method']
        status = request.form['status']

        cursor.execute(
            """INSERT INTO payments
            (customer, amount, method, status)
            VALUES (?, ?, ?, ?)""",
            (customer, amount, method, status)
        )

        conn.commit()

    cursor.execute("SELECT * FROM payments")
    data = cursor.fetchall()

    conn.close()

    return render_template('payments.html', payments=data)

@app.route('/reports')
def reports():

    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM payments WHERE status='Paid'")
    total_revenue = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM rooms")
    total_rooms = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'reports.html',
        total_customers=total_customers,
        total_bookings=total_bookings,
        total_revenue=total_revenue,
        total_rooms=total_rooms
    )


if __name__ == '__main__':
    app.run(debug=True)
