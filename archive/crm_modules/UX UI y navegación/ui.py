from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/clients')
def clients():
    return render_template('clients.html')

@app.route('/sales')
def sales():
    return render_template('sales.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')
