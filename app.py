from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ---------------- LOGIN ----------------
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # ❌ SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return render_template("dashboard.html", user=user[1])
    else:
        return "Login Failed!"


# ---------------- DASHBOARD (BROKEN AUTH) ----------------
@app.route("/dashboard")
def dashboard():
    user = request.args.get("user")
    return render_template("dashboard.html", user=user)


# ---------------- MARKS (SQLi + DATA EXPOSURE) ----------------
@app.route("/marks")
def marks():
    user = request.args.get("user")

    # ❌ SQL Injection
    query = f"SELECT * FROM marks WHERE student_name='{user}'"

    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    return render_template("marks.html", marks=data, user=user)


# ---------------- DISCUSSION (STORED XSS) ----------------
@app.route("/discussion", methods=["GET", "POST"])
def discussion():
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()

    if request.method == "POST":
        username = request.form["username"]
        message = request.form["message"]

        # ❌ Stored XSS + SQL Injection
        cursor.execute(
            f"INSERT INTO comments (username, message) VALUES ('{username}', '{message}')"
        )
        conn.commit()

    cursor.execute("SELECT * FROM comments")
    comments = cursor.fetchall()
    conn.close()

    return render_template("discussion.html", comments=comments)


# ---------------- ADMIN (SECURITY MISCONFIGURATION) ----------------
@app.route("/admin")
def admin():
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()
    return render_template("admin.html", users=users)


@app.route("/reflected-xss")
def reflected_xss():
    msg = request.args.get("msg")
    return f"""
    <h2>Reflected XSS Lab</h2>
    <p>User input is reflected directly:</p>
    <div>{msg}</div>
    <p>Try payload:</p>
    <code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code>
    """

@app.route("/profile")
def profile():
    user_id = request.args.get("id")

    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE id={user_id}"
    cursor.execute(query)
    user = cursor.fetchone()

    conn.close()
    return f"<h2>User Profile</h2><pre>{user}</pre>"

@app.route("/debug")
def debug():
    return {
        "db_user": "admin",
        "db_password": "admin123",
        "api_key": "SECRET-API-KEY-12345"
    }

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
