import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_CLIENT_URL = os.getenv('MONGO_CLIENT_URL')

app = Flask(__name__)
client = MongoClient(MONGO_CLIENT_URL,
                    tlsCAFile=certifi.where())
app.db = client.microblog
entries = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        entries.append((entry_content, formatted_date))
        app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

    entries_with_date = [
        (
            entry[0],
            entry[1],
            datetime.datetime.strptime(entry[1], "%Y-%m-%d").strftime("%b %d")
        )
        for entry in entries
    ]
    return render_template("home.html", entries=entries_with_date)

