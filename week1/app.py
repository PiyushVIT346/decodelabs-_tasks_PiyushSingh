"""
app.py
------
Flask entry point. Routes are intentionally thin: auth logic lives in
storage.py, chat logic lives in chain.py. This file just wires HTTP to them.
"""

import os
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

import chain
import storage

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32))

storage.init_db()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


# --------------------------------------------------------------------------
# Auth
# --------------------------------------------------------------------------

@app.route("/")
def index():
    return redirect(url_for("chat_page") if "username" in session else url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if storage.create_user(username, password):
            return redirect(url_for("login", registered="1"))
        return render_template("register.html", error="That username is already taken.")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if storage.verify_user(username, password):
            session["username"] = username.strip().lower()
            return redirect(url_for("chat_page"))
        return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html", just_registered=request.args.get("registered"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


# --------------------------------------------------------------------------
# Chat UI + API
# --------------------------------------------------------------------------

@app.route("/chat")
@login_required
def chat_page():
    return render_template("chat.html", username=session["username"])


@app.route("/api/history")
@login_required
def api_history():
    return jsonify(chain.load_history(_session_id()))


@app.route("/api/chat", methods=["POST"])
@login_required
def api_chat():
    user_input = (request.get_json(silent=True) or {}).get("message", "").strip()
    if not user_input:
        return jsonify({"error": "Message cannot be empty."}), 400

    reply = chain.chat(_session_id(), session["username"], user_input)
    return jsonify({"reply": reply, "storage": _storage_payload()})


@app.route("/api/storage")
@login_required
def api_storage():
    return jsonify(_storage_payload())


def _session_id() -> str:
    return f"session_default_user_{session['username']}"


def _storage_payload() -> dict:
    stats = storage.get_db_stats()
    stats["session_messages"] = storage.get_session_message_count(_session_id())
    stats["ledger"] = storage.recent_ledger(limit=20)
    return stats


if __name__ == "__main__":
    app.run(debug=True, port=5000)