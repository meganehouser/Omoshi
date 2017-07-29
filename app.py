# coding: utf-8

from flask import Flask, render_template, g, request, redirect, url_for
import sqlite3
from datetime import date, datetime, timedelta


app = Flask(__name__)
app.config.from_pyfile('app.cfg')

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    return conn

@app.before_request
def brfore_request():
    g.db = connect_db()

@app.after_request
def after_erquest(response):
    g.db.close()
    return response

@app.route('/')
def root():
    return redirect(url_for('show'))

@app.route('/show', methods=['GET', 'POST'])
def show():
    def parse_date(s):
        d = datetime.strptime(s, '%Y-%m-%d')
        return date(d.year, d.month, d.day)

    if request.method == 'GET':
        to_date = date.today()
        from_date = to_date - timedelta(30)
    else:
        to_date = parse_date(request.form['to_date'])
        from_date = parse_date(request.form['from_date'])


    result = g.db.execute("SELECT registered, weight, bodyfat FROM entries WHERE ? <= registered AND registered <= ?",
            [from_date, to_date])
    weights = {}
    bodyfats = {}
    for row in result:
        weights[row[0]] = row[1]
        bodyfats[row[0]] = row[2]

    timespan = (to_date - from_date).days
    days = [to_date - timedelta(n) for n in range(timespan, -1, -1)]
    labels = [ f"{n.year:04d}-{n.month:02d}-{n.day:02d}" for n in days]

    weight_data = []
    bodyfat_data = []
    for day in days:
        weight = weights.get(day)
        weight_data.append("null" if weight is None else str(weight))
        bodyfat = bodyfats.get(day)
        bodyfat_data.append("null" if bodyfat is None else str(bodyfat))

    return render_template('index.html', 
            from_date=from_date, to_date=to_date,
            labels=labels, weights=weight_data, bodyfats=bodyfat_data)    

@app.route('/register', methods=['GET'])
def show_add_form():
    today = f"{date.today():%Y-%m-%d}"
    return render_template('register.html', today=today)

@app.route('/register', methods=['POST'])
def register():
    temp = datetime.strptime(request.form['registered'], '%Y-%m-%d')
    registered = date(temp.year, temp.month, temp.day)
    weight = float(request.form['weight'])
    bodyfat = float(request.form['bodyfat'])
    g.db.execute('insert into entries (registered, weight, bodyfat) values (?, ?, ?)',
        [registered, weight, bodyfat])
    g.db.commit()
    return redirect(url_for('show'))

if __name__ == '__main__':
    app.run(host='127.0.0.1')
