from flask import Flask, render_template, url_for
from db import db 

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html", message='Ciao mondo!!')

@app.route("/users")
def user():
    return render_template('users.html', users=users)

@app.route("/user/<utente>")
def utente(utente):
    return render_template('profile.html', utente=utente)


app.run(debug=True)
