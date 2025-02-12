from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'calabrese-termite-hyka'

mysql = MySQL(app)

<<<<<<< HEAD
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
=======
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

@app.route('/create_table')
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utenti (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            email VARCHAR(100)
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
>>>>>>> 43e1105 (zaibev)
