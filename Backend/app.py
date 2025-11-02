from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "ssssss@0910@",
    "database": "disaster_alerts"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS disaster_alerts")
        conn.database = DB_CONFIG["database"]
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message VARCHAR(255) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print("Error initializing database:", e)

@app.route("/")
def home():
    return "Flask connected successfully to MySQL!"

@app.route("/api/send_alert", methods=["POST"])
def send_alert():
    try:
        data = request.get_json()
        message = data.get("message")

        if not message:
            return jsonify({"success": False, "error": "Message required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO alerts (message) VALUES (%s)", (message,))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"success": True, "message": "Alert sent successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

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
# Main function run
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5030, debug=True)
