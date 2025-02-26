from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "AudiS3"
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
    ordinamento = request.args.get("ordinamento", "Titolo")
    categoria_selezionata = request.args.get("categoria", "Tutti")

    # Recupero le categorie disponibili
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT Categoria FROM Libri")
    categorie = [row[0] for row in cursor.fetchall()]
    categorie.insert(0, "Tutti")  # Aggiungo l'opzione per visualizzare tutti i libri

    # Costruisco la query principale con filtro categoria
    query = "SELECT * FROM Libri"
    params = []
    if categoria_selezionata != "Tutti":
        query += " WHERE Categoria = %s"
        params.append(categoria_selezionata)

    # Aggiungo l'ordinamento
    if ordinamento == "Autore":
        query += " ORDER BY CodAutore"
    else:
        query += " ORDER BY Titolo"

    cursor.execute(query, params)
    listaLibri = cursor.fetchall()

    return render_template("libri.html", libri=listaLibri, ordinamento=ordinamento, categorie=categorie, categoria_selezionata=categoria_selezionata)

@app.route("/aggiungiLibro", methods=["GET", "POST"])
def aggiungiLibro():
    if request.method == 'GET':
        return render_template("aggiungiLibro.html")
    else:
        isbn = request.form.get("isbn")
        titolo = request.form.get("titolo")
        codAutore = request.form.get("codAutore")
        anno = request.form.get("anno")
        categoria = request.form.get("categoria")

        anno_int = int(anno)


        print(codAutore)

        #Controllo che il codAutore esista
        query = "SELECT * FROM Autori WHERE CodAutore=%s"
        cursor = mysql.connection.cursor()
        cursor.execute(query, (codAutore,))
        tmp = cursor.fetchall()

        if len(tmp) > 0: #codAutore esiste
            query = "INSERT INTO Libri (ISBNLibro, Titolo, CodAutore, Anno, Categoria) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(query, (isbn, titolo, codAutore, anno_int, categoria))
            mysql.connection.commit()
            flash("Libro aggiunto correttamente.")
            return redirect(url_for('aggiungiLibro'))
        else:
            flash("Codice autore non esistente.")
            return redirect(url_for('aggiungiLibro'))

app.run(debug=True)