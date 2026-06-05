from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'monapp'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres')
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, nom TEXT, message TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/messages', methods=['GET'])
def get_messages():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT nom, message, date FROM messages ORDER BY date DESC')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'nom': r[0], 'message': r[1], 'date': str(r[2])} for r in rows])

@app.route('/messages', methods=['POST'])
def add_message():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO messages (nom, message) VALUES (%s, %s)', (data['nom'], data['message']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'ok'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
