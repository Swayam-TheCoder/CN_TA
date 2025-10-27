import os
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", ""),
    "port": int(os.getenv("DB_PORT", 3306))
}

# Connect to Database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Connected to MySQL successfully!")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        raise

# Initialize the database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message VARCHAR(255),
            location VARCHAR(100),
            severity VARCHAR(50)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database initialized successfully.")

@app.route("/")
def home():
    return jsonify({"message": "Backend running successfully!"})

# Endpoint to add data
@app.route("/add", methods=["POST"])
def add_alert():
    data = request.get_json()
    message = data.get("message")
    location = data.get("location")
    severity = data.get("severity")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO alerts (message, location, severity) VALUES (%s, %s, %s)",
        (message, location, severity)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success", "message": "Alert added successfully!"})

# Endpoint to get all data
@app.route("/alerts", methods=["GET"])
def get_alerts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alerts")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
