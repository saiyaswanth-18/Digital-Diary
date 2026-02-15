import os
import sqlite3
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, send_file, abort, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'digitaldiary99'

UPLOAD_ROOT = "uploads"
os.makedirs(UPLOAD_ROOT, exist_ok=True)
app.config["UPLOAD_ROOT"] = UPLOAD_ROOT

def connect_db():
    return sqlite3.connect('DigitalDiary.db')


def init_db():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS USERS(
            USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USER_NAME TEXT UNIQUE,
            PASSWORD TEXT NOT NULL,
            EMAIL TEXT UNIQUE
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS ENTRIES(
            ENTRY_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USER_ID INTEGER,
            TITLE TEXT,
            CONTENT TEXT,
            ENTRY_DATE TEXT,
            FOREIGN KEY(USER_ID) REFERENCES USERS(USER_ID)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS MEDIA(
            MEDIA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ENTRY_ID INTEGER,
            USER_ID INTEGER,
            FILE_PATH TEXT,
            MIME_TYPE TEXT,
            FOREIGN KEY(ENTRY_ID) REFERENCES ENTRIES(ENTRY_ID),
            FOREIGN KEY(USER_ID) REFERENCES USERS(USER_ID)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_file(os.path.join(UPLOAD_ROOT, filename))

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register")
def register_user():
    return render_template('register.html')
@app.route("/register", methods=["POST"])
def register():
    user_name = request.form['user_name']
    user_mail = request.form['user_mail']
    user_password = request.form['user_password']
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''INSERT INTO USERS (USER_NAME, PASSWORD, EMAIL) VALUES (?, ?, ?)''',
            (user_name, user_password, user_mail)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    except sqlite3.IntegrityError:
        conn.close()
        return render_template('register.html', msg="Username or Email already exists!")


@app.route("/login")
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    user_name = request.form['u_name']
    user_password = request.form['u_password']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM USERS WHERE USER_NAME=? AND PASSWORD=?''', (user_name, user_password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['username'] = user_name
        session['user_id'] = user[0]
        return redirect(url_for("dashboard"))
    else:
        return render_template('login.html', message='invalid user credentials')


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", name=session['username'])

@app.route("/diary")
def diary_page():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("diary.html")

def user_upload_folder(user_id):
    folder = os.path.join(app.config["UPLOAD_ROOT"], f"user_{user_id}")
    os.makedirs(folder, exist_ok=True)
    return folder

@app.route("/submit_entry", methods=["POST"])
def submit_entry():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    date = request.form.get("date", "")

    if not content:
        flash("Diary content cannot be empty.")
        return redirect(url_for("diary_page"))

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO ENTRIES (USER_ID, TITLE, CONTENT, ENTRY_DATE) VALUES (?, ?, ?, ?)",
                (user_id, title, content, date))
    entry_id = cur.lastrowid

    files = request.files.getlist("media_files")

    if files:
        user_folder = user_upload_folder(user_id)

        for f in files:
            if not f or f.filename == "":
                continue

            filename = secure_filename(f.filename)
            unique_name = f"{uuid.uuid4().hex}_{filename}"

            relative_path = f"user_{user_id}/{unique_name}"
            save_path = os.path.join(UPLOAD_ROOT, relative_path)

            f.save(save_path)

            mime = f.mimetype or ""
            cur.execute("INSERT INTO MEDIA (ENTRY_ID, USER_ID, FILE_PATH, MIME_TYPE) VALUES (?, ?, ?, ?)",
                        (entry_id, user_id, relative_path, mime))

    conn.commit()
    conn.close()
    return redirect(url_for("entries_page"))

@app.route("/API/entries")
def past_entries_api():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT ENTRY_ID, TITLE, ENTRY_DATE 
        FROM ENTRIES
        WHERE USER_ID = ?
        ORDER BY ENTRY_DATE DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()

    entries = []
    for row in rows:
        entries.append({
            "ENTRY_ID": row[0],
            "TITLE": row[1],
            "ENTRY_DATE": row[2]
        })

    return jsonify(entries)

@app.route("/entries")
def entries_page():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("entries.html")

@app.route("/entry/<int:entry_id>")
def view_entry(entry_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT TITLE, CONTENT, ENTRY_DATE
        FROM ENTRIES
        WHERE ENTRY_ID = ? AND USER_ID = ?
    """, (entry_id, user_id))

    entry = cur.fetchone()

    if not entry:
        conn.close()
        abort(404)

    cur.execute("""
        SELECT FILE_PATH, MIME_TYPE
        FROM MEDIA
        WHERE ENTRY_ID = ? AND USER_ID = ?
    """, (entry_id, user_id))

    media_files = cur.fetchall()
    conn.close()
    return render_template("view_entry.html", entry_id=entry_id, entry=entry, media_files=media_files)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)