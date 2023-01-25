import certifi
import datetime
import os

from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_CLIENT_URL = os.getenv('MONGO_CLIENT_URL')

def create_app():
    app = Flask(__name__)
    client = MongoClient(MONGO_CLIENT_URL,
                        tlsCAFile=certifi.where())
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries = app.db.entries.find( {} )
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in entries
        ]

        return render_template("home.html", entries=entries_with_date)
    
    return app
