DROP TABLE IF EXISTS Prestiti;
DROP TABLE IF EXISTS Libri;
DROP TABLE IF EXISTS Autori;
DROP TABLE IF EXISTS Utenti;


CREATE TABLE IF NOT EXISTS Autori(
    CodAutore varchar(10) PRIMARY KEY,
    Nome varchar(255) NOT NULL,
    Cognome varchar(255) NOT NULL,
    DataNascita date,
    DataMorte date
);

CREATE TABLE IF NOT EXISTS Libri(
    ISBNLibro char(13) PRIMARY KEY,
    Categoria varchar(255) NOT NULL,
    Titolo varchar(255) NOT NULL, 
    Prezzo float NOT NULL,
    Scaffale int NOT NULL,
    Anno int NOT NULL,
    CodAutore varchar(10) NOT NULL,

    FOREIGN KEY (CodAutore) REFERENCES Autori(CodAutore)
);

CREATE TABLE IF NOT EXISTS Utenti(
    CodUtente varchar(10) PRIMARY KEY,
    Nome varchar(255) NOT NULL,
    Cognome varchar(255) NOT NULL,
    Email varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Prestiti(
    CodPrestito varchar(10),
    CodUtente varchar(10),
    DataPrestito date,
    DataRestituzione date,
    ISBNLibro varchar(13),
    
    PRIMARY KEY(CodPrestito, CodUtente),
    FOREIGN KEY (CodUtente) REFERENCES Utenti(CodUtente),
    FOREIGN KEY (ISBNLibro) REFERENCES Libri(ISBNLibro)
);