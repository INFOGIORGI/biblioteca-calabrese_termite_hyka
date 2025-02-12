from flask import Flask, render_template, url_for
from db import db 

app = Flask(__name__)

users = ['Alice', 'Bob', 'Charlie'] 

@app.route("/")
def hello():
    return render_template("index.html", message='Ciao mondo!!')


app.run(debug=True)
