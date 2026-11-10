
import json
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo.errors import PyMongoError

from config import submissions_collection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def get_data():
    with open("data/data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    return jsonify(data)


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


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
