import os

import mysql.connector
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

MAX_MESSAGE_LENGTH = 255


def get_connection():
    """Open a new MySQL connection using settings from environment variables."""
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "mysql-db"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DB", "devops"),
        connection_timeout=5,
    )


def save_message(text):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (message) VALUES (%s)", (text,))
        conn.commit()
    finally:
        conn.close()


def load_messages():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, message, created_at FROM messages ORDER BY id DESC LIMIT 50"
        )
        return cursor.fetchall()
    finally:
        conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        text = request.form.get("message", "").strip()[:MAX_MESSAGE_LENGTH]
        if text:
            try:
                save_message(text)
            except mysql.connector.Error:
                app.logger.exception("Could not save message")
                error = "Your message could not be saved. Try again in a moment."
            else:
                return redirect(url_for("index"))

    try:
        messages = load_messages()
    except mysql.connector.Error:
        app.logger.exception("Could not load messages")
        messages = []
        error = error or "Messages could not be loaded. The database may still be starting."

    status = 503 if error and not messages else 200
    return (
        render_template("index.html", messages=messages, error=error, max_length=MAX_MESSAGE_LENGTH),
        status,
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
