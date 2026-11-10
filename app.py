import json
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo.errors import PyMongoError

from config import submissions_collection

app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# To-Do page
@app.route("/todo")
def todo():
    return render_template("todo.html")


# API route - Read JSON data
@app.route("/api")
def get_data():
    with open("data/data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    return jsonify(data)


# Existing contact form submission
@app.route("/submit", methods=["POST"])
def submit_form():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    form_data = {
        "name": name,
        "email": email,
        "message": message
    }

    if not all(form_data.values()):
        return render_template(
            "index.html",
            error="Please fill in all fields.",
            form_data=form_data
        ), 400

    try:
        submissions_collection.insert_one({
            **form_data,
            "created_at": datetime.now(timezone.utc)
        })

        return redirect(url_for("success"))

    except PyMongoError:
        app.logger.exception("MongoDB submission failed")

        return render_template(
            "index.html",
            error="Unable to submit your data. Please try again.",
            form_data=form_data
        ), 500


# New To-Do API - Save item to MongoDB
@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json(silent=True) or {}

    item_name = data.get("itemName", "").strip()
    item_description = data.get("itemDescription", "").strip()

    if not item_name or not item_description:
        return jsonify({
            "message": "Both fields are required"
        }), 400

    try:
        submissions_collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description,
            "created_at": datetime.now(timezone.utc)
        })

        return jsonify({
            "message": "To-Do item saved successfully!"
        }), 201

    except PyMongoError:
        app.logger.exception("To-Do submission failed")

        return jsonify({
            "message": "Unable to save To-Do item"
        }), 500


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)