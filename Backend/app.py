from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MySQL Database Configuration

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ssssss@0910@',  
    'database': 'disaster_alerts'
}

# Database Setup (auto-create table)

def init_db():
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS disaster_alerts")
    conn.database = DB_CONFIG['database']
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

# API: Send Alert\
@app.route('/api/send_alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'success': False, 'error': 'Message required'}), 400

    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO alerts (message) VALUES (%s)", (message,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'success': True, 'message': 'Alert sent successfully'})

# API: Get All Alerts (Admin)
@app.route('/api/alerts', methods=['GET'])
def get_all_alerts():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM alerts ORDER BY id DESC")
    alerts = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(alerts)

# API: Get Recent Alerts (Client View)
@app.route('/api/client_alerts', methods=['GET'])
def get_recent_alerts():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 5")
    alerts = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(alerts)

# Now Starting the Server
if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5030, debug=True)
