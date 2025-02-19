from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'calabrese-termite-hyka'

mysql = MySQL(app)

def getUtenti():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM UTENTI')
        utenti = cursor.fetchall()
        cursor.close()
        return utenti
    except Exception as e:
        print(f"Errore durante il recupero degli utenti: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True)
