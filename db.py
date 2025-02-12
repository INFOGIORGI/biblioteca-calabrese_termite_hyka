from flask import Flask, render_template
from flask_mysqldb import MySQL
class db

def_init_(self):
    try


app = Flask(__name__)
app.config["MYSQL_HOST"]="138.41.20.102"
app.config["MYSQL_PORT"]= 53306
app.config["MYSQL_DB"]= "calabrese-termite-hyka"
app.config["MYSQL_USER"]="ospite"
app.config["MYSQL_PASSWORD"]="ospite"

def getUtenti():
    query='SELECT * FROM UTENTI'
    cursor