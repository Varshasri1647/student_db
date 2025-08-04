from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    subject1 INTEGER,
                    subject2 INTEGER,
                    subject3 INTEGER
                )""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        s1 = int(request.form["subject1"])
        s2 = int(request.form["subject2"])
        s3 = int(request.form["subject3"])

        conn = sqlite3.connect("student.db")
        c = conn.cursor()
        c.execute("INSERT INTO students (name, subject1, subject2, subject3) VALUES (?, ?, ?, ?)", (name, s1, s2, s3))
        conn.commit()
        conn.close()
        return redirect('/results')
    return render_template("add_student.html")

@app.route('/results')
def view_results():
    conn = sqlite3.connect("student.db")
    c = conn.cursor()
    c.execute("SELECT *, (subject1+subject2+subject3) as total FROM students")
    data = c.fetchall()
    conn.close()
    return render_template("view_results.html", students=data)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)