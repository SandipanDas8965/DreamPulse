from flask import Flask, render_template, request, jsonify
from model.emotion_utils import analyze_entry
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('data/entries.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            emotion TEXT,
            confidence REAL,
            symbols TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    text = data.get('text', '')

    if not text.strip():
        return jsonify({"error": "Empty entry"}), 400

    result = analyze_entry(text)

    conn = sqlite3.connect('data/entries.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO entries (text, emotion, confidence, symbols, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        text,
        result['emotion'],
        result['confidence'],
        ",".join(result['symbols']),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

    return jsonify(result)

@app.route('/entries')
def get_entries():
    conn = sqlite3.connect('data/entries.db')
    cursor = conn.cursor()
    cursor.execute('SELECT text, emotion, confidence, symbols, timestamp FROM entries ORDER BY timestamp')
    rows = cursor.fetchall()
    conn.close()

    entries = []
    for row in rows:
        entries.append({
            "text": row[0],
            "emotion": row[1],
            "confidence": row[2],
            "symbols": row[3].split(",") if row[3] else [],
            "timestamp": row[4]
        })

    return jsonify(entries)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)