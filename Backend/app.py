import os
import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# DATABASE CONFIG (read from environment variables)
DB_CONFIG = {
    "host": os.getenv("MYSQLHOST") or os.getenv("DB_HOST"),
    "user": os.getenv("MYSQLUSER") or os.getenv("DB_USER"),
    "password": os.getenv("MYSQLPASSWORD") or os.getenv("DB_PASSWORD"),
    "database": os.getenv("MYSQLDATABASE") or os.getenv("DB_NAME"),
    "port": int(os.getenv("MYSQLPORT") or os.getenv("DB_PORT") or 3306)
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    # create database and table if not exists (safe to call on startup)
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"]
    )
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(DB_CONFIG["database"]))
    conn.database = DB_CONFIG["database"]
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message VARCHAR(255),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ DB initialized")

@app.route("/")
def home():
    return jsonify({"message": "Backend running"})

@app.route("/api/send_alert", methods=["POST"])
def send_alert():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"success": False, "error": "Message required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO alerts (message) VALUES (%s)", (message,))
    conn.commit()
    cur.close()
    conn.close()

    # (Optionally) emit websocket or send push here
    return jsonify({"success": True, "message": "Alert saved"})

@app.route("/api/alerts", methods=["GET"])
def get_all_alerts():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM alerts ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route("/api/client_alerts", methods=["GET"])
def get_recent_alerts():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 5")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
