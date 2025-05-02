from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'w3schools'

mysql = MySQL(app)

def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

@app.route('/drop_table')
def drop_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS Libri
DROP TABLE IF EXISTS Autori
DROP TABLE IF EXISTS Utenti
DROP TABLE IF EXISTS Prestiti
DROP TABLE IF EXISTS Scrive
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    return

@app.route('/create_table')
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE Libri(
    ISBNLibro char[13] PRIMARY KEY,
    Categoria varchar [15] NOT NULL,
    Titolo varchar [15] NOT NULL, 
    Prezzo float NOT NULL,
    Scaffale int NOT NULL,
    Anno int NOT NULL,
    CodAutore varchar [10] NOT NULL,

     FOREIGN KEY CodAutore REFERENCES Autore(CodAutore),
    )
CREATE TABLE Autore(
    CodAutore varchar [10] PRIMARY KEY,
    Nome varchar [10] NOT NULL,
    Cognome varchar [10] NOT NULL,
    DataNascita date,
    DataMorte date,
    )

CREATE TABLE Utente(
    CodUtente varchar [10] PRIMARY KEY,
    Nome varchar [10] NOT NULL,
    Cognome varchar [10] NOT NULL,
    Email varchar NOT NULL,
    )

CREATE TABLE PRESTITI(
    CodPrestito varchar [10] PRIMARY KEY,
    CodUtente varchar [10] PRIMARY KEY,
    DataPrestito date,
    DataRestituzione date,
    ISBNLibro varchar[13],

    FOREIGN KEY CodUtente REFERENCES Utente,
    FOREIGN KEY ISBNLibro REFERENCES Libri
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    return 

@app.route("/")
def index():

    return render_template('index.html', titolo="Home page")

@app.route("/profile")
def profile():

    return render_template('profile.html', titolo="Profile")

@app.route("/users")
def users():
    
    return render_template('users.html')

app.run(debug=True)
