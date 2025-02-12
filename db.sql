DROP TABLE IF EXISTS Libri
DROP TABLE IF EXISTS Autori
DROP TABLE IF EXISTS Utenti
DROP TABLE IF EXISTS Prestiti
DROP TABLE IF EXISTS Scrive

CREATE TABLE Libri{
    ISBNLibro char[13] PRIMARY KEY,
    Categoria varchar [15] NOT NULL,
    Titolo varchar [15] NOT NULL, 
    Prezzo float NOT NULL,
    Scaffale int NOT NULL,
    Anno int NOT NULL,
    CodAutore varchar [10] NOT NULL,

     FOREIGN KEY CodAutore REFERENCES Autore(CodAutore),
}

CREATE TABLE Autore{
    CodAutore varchar [10] PRIMARY KEY,
    Nome varchar [10] NOT NULL,
    Cognome varchar [10] NOT NULL,
    DataNascita date,
    DataMorte date,
}

CREATE TABLE Utente{
    CodUtente varchar [10] PRIMARY KEY,
    Nome varchar [10] NOT NULL,
    Cognome varchar [10] NOT NULL,
    Email varchar NOT NULL,
}

CREATE TABLE PRESTITI{
    CodPrestito varchar [10] PRIMARY KEY,
    CodUtente varchar [10] PRIMARY KEY,
    DataPrestito date,
    DataRestituzione date,
    ISBNLibro varchar[13],

    FOREIGN KEY CodUtente REFERENCES Utente,
    FOREIGN KEY ISBNLibro REFERENCES Libri
}