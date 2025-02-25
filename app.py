from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = '5di'
app.config['MYSQL_PASSWORD'] = 'colazzo'
app.config['MYSQL_DB'] = 'termite_calabrese_hyka'

mysql = MySQL(app)

@app.route("/")
def homePage():
    return render_template("homePage.html")

@app.route("/libri")
def libri():
    query = "SELECT * FROM Libri"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    listaLibri = cursor.fetchall()

    return render_template("libri.html", libri=listaLibri)

@app.route("/aggiungiLibro")
def aggiungiLibro():
    return render_template("aggiungiLibro.html")


app.run(debug=True)