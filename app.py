from flask import Flask, render_template
from db import db

app = Flask(__name__)

@app.route("/")
def homePage():
    return render_template("homePage.html")


app.run(debug=True)