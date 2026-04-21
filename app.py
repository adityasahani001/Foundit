from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ========================
# DATABASE CONNECTION
# ========================

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ========================
# HOME ROUTE
# ========================

@app.route('/')
def home():
    return render_template('index.html')

# ========================
# REGISTER
# ========================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        conn = get_db()
        conn.execute("INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)",
                     (name, email, phone, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# ========================
# LOGIN
# ========================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                            (email, password)).fetchone()
        conn.close()

        if user:
            return redirect('/')
        else:
            return "Invalid credentials"

    return render_template('login.html')

# ========================
# REPORT LOST
# ========================

@app.route('/report-lost', methods=['GET', 'POST'])
def report_lost():
    if request.method == 'POST':
        itemname = request.form['itemname']
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']
        location = request.form['location']

        conn = get_db()
        conn.execute("INSERT INTO items (name, category, description, date, location, status) VALUES (?, ?, ?, ?, ?, ?)",
                     (itemname, category, description, date, location, "Lost"))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('report-lost.html')

# ========================
# REPORT FOUND
# ========================

@app.route('/report-found', methods=['GET', 'POST'])
def report_found():
    if request.method == 'POST':
        itemname = request.form['itemname']
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']
        location = request.form['location']

        conn = get_db()
        conn.execute("INSERT INTO items (name, category, description, date, location, status) VALUES (?, ?, ?, ?, ?, ?)",
                     (itemname, category, description, date, location, "Found"))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('report-found.html')

# ========================
# SEARCH
# ========================

@app.route('/search')
def search():
    conn = get_db()
    items = conn.execute("SELECT * FROM items").fetchall()
    conn.close()

    return render_template('search.html', items=items)

# ========================
# RUN APP
# ========================

if __name__ == '__main__':
    app.run(debug=True)