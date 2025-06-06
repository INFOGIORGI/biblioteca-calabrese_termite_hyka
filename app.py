from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)
app.secret_key = "daniel"
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


@app.route("/gestioneBiblioteca", methods=["GET", "POST"])
def gestioneBiblioteca():

    if "admin_logged_in" not in session:  # Controlla se l'admin è loggato
        flash("Devi effettuare il login per accedere alla pagina di gestione.")
        return redirect(url_for("loginAdmin"))

    ordinamento = request.args.get("ordinamento", "Titolo")
    categoria_selezionata = request.args.get("categoria", "Tutti")

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT Categoria FROM Libri")
    categorie = [row[0] for row in cursor.fetchall()]
    categorie.insert(0, "Tutti")

    query = "SELECT * FROM Libri"
    params = []
    if categoria_selezionata != "Tutti":
        query += " WHERE Categoria = %s"
        params.append(categoria_selezionata)

    if ordinamento == "Autore":
        query += " ORDER BY CodAutore"
    else:
        query += " ORDER BY Titolo"

    cursor.execute(query, params)
    listaLibri = cursor.fetchall()

    if request.method == 'GET':
        return render_template("gestioneBiblioteca.html", libri=listaLibri, ordinamento=ordinamento, categorie=categorie, categoria_selezionata=categoria_selezionata)
    
    else:
        tipoForm = request.form.get("form_type")

        if tipoForm == "presta":
            progressivoLibro = request.form.get("progressivoLibro")
            data_prestito = datetime.date.today()

            query = "UPDATE Libri SET PresoInPrestito = 1, DataInizioPrestito = %s WHERE Progressivo = %s AND PresoInPrestito = 0"
            cursor.execute(query, (data_prestito, progressivoLibro))
            mysql.connection.commit()
            flash("Libro prestato con successo.")
            
            return redirect(url_for("gestioneBiblioteca"))

        elif tipoForm == "rimuovi_prestito":
            progressivoLibro = request.form.get("progressivoLibro")

            query = "UPDATE Libri SET PresoInPrestito = 0, DataInizioPrestito = NULL WHERE Progressivo = %s AND PresoInPrestito = 1"
            cursor.execute(query, (progressivoLibro,))
            mysql.connection.commit()
            flash("Prestito rimosso con successo.")
            return redirect(url_for("gestioneBiblioteca"))
        
        elif tipoForm == "autore":

            codAutore = None
            nome = None
            cognome = None
            dataNascita = None

            codAutore = request.form.get("codAutore")
            nome = request.form.get("nome")
            cognome = request.form.get("cognome")
            dataNascita = request.form.get("dataNascita")
            dataMorte = request.form.get("dataMorte")

            if codAutore == None or nome == None or dataNascita == None:
                flash("Inserisci le informazioni obbligatorie.")
                return redirect(url_for("gestioneBiblioteca"))

            # Controllo se l'autore esiste già
            query = "SELECT * FROM Autori WHERE CodAutore=%s"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (codAutore,))
            tmp = cursor.fetchall()

            if len(tmp) > 0:
                flash("Autore con stesso codice già esistente.")
                return redirect(url_for("gestioneBiblioteca"))
            else: 
                # Se dataMorte è vuota, passiamo NULL
                if not dataMorte:
                    query = "INSERT INTO Autori (CodAutore, Nome, Cognome, DataNascita, DataMorte) VALUES (%s,%s,%s,%s,NULL)"
                    cursor.execute(query, (codAutore, nome, cognome, dataNascita))
                else:
                    query = "INSERT INTO Autori (CodAutore, Nome, Cognome, DataNascita, DataMorte) VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(query, (codAutore, nome, cognome, dataNascita, dataMorte))
                
                mysql.connection.commit()

                flash("Autore inserito correttamente")
                return redirect(url_for("gestioneBiblioteca"))
        elif tipoForm == "libro":
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
                query = "INSERT INTO Libri (ISBNLibro, Titolo, CodAutore, Anno, Categoria, PresoInPrestito) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, (isbn, titolo, codAutore, anno_int, categoria, False))
                mysql.connection.commit()
                flash("Libro aggiunto correttamente.")
                return redirect(url_for('gestioneBiblioteca'))
            else:
                flash("Codice autore non esistente.")
                return redirect(url_for('gestioneBiblioteca'))
        elif tipoForm == "eliminaAutore":
            codAutore = request.form.get("codAutore")

            #Controllo che il codAutore esista
            query = "SELECT * FROM Autori WHERE CodAutore=%s"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (codAutore,))
            tmp = cursor.fetchall()

            if len(tmp) > 0: #codAutore esiste
                query = "DELETE FROM Autori WHERE CodAutore=%s"
                cursor.execute(query, (codAutore,))
                mysql.connection.commit()
                flash("Autore rimosso correttamente.")
                return redirect(url_for('gestioneBiblioteca'))
            else:
                flash("Autore non esistente.")
                return redirect(url_for('gestioneBiblioteca'))
        elif tipoForm == "eliminaLibro":
            progressivoLibro = request.form.get("progressivoLibro")

            #Controllo che il progressivo esista
            query = "SELECT * FROM Libri WHERE Progressivo=%s"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (progressivoLibro,))
            tmp = cursor.fetchall()

            if len(tmp) > 0: #progressivo esiste
                query = "DELETE FROM Libri WHERE Progressivo=%s"
                cursor.execute(query, (progressivoLibro,))
                mysql.connection.commit()
                flash("Libro rimosso correttamente.")
                return redirect(url_for('gestioneBiblioteca'))
            else:
                flash("Progressivo non esistente.")
                return redirect(url_for('gestioneBiblioteca'))

        return redirect(url_for("gestioneBiblioteca"))

@app.route("/loginAdmin", methods=["GET", "POST"])
def loginAdmin():
    if request.method == "GET":
        return render_template("loginAdmin.html")
    else:
        username = request.form.get("email")
        password = request.form.get("password")

        query = "SELECT * FROM Admin WHERE email=%s AND password=%s"
        cursor = mysql.connection.cursor()
        cursor.execute(query, (username, password))

        tmp = cursor.fetchall()

        if tmp:
            session["admin_logged_in"] = True  # Imposta la sessione
            return redirect(url_for("gestioneBiblioteca"))
        else:
            flash("Credenziali errate. Riprova.")
            return redirect(url_for("loginAdmin"))
        
@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)  # Elimina la sessione
    return redirect(url_for("homePage"))

app.run(debug=True)