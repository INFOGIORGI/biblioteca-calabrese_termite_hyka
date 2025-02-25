DROP TABLE IF EXISTS Prestiti;
DROP TABLE IF EXISTS Libri;
DROP TABLE IF EXISTS Autori;
DROP TABLE IF EXISTS Utenti;


CREATE TABLE IF NOT EXISTS Autori(
    CodAutore varchar(10) PRIMARY KEY,
    Nome varchar(255) NOT NULL,
    Cognome varchar(255) NOT NULL,
    DataNascita date NOT NULL,
    DataMorte date
);

CREATE TABLE IF NOT EXISTS Libri(
    ISBNLibro char(13) PRIMARY KEY,
    Titolo varchar(255) NOT NULL, 
    CodAutore varchar(10) NOT NULL,
    Anno int NOT NULL,
    Categoria varchar(255) NOT NULL,
    Prezzo float NOT NULL,

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
    
    PRIMARY KEY(CodPrestito),
    FOREIGN KEY (CodUtente) REFERENCES Utenti(CodUtente),
    FOREIGN KEY (ISBNLibro) REFERENCES Libri(ISBNLibro)
);


INSERT INTO Autori (CodAutore, Nome, Cognome, DataNascita, DataMorte) VALUES
('Hawk001', 'Stephen', 'Hawking', '1942-01-08', '2018-03-14'),
('Darw001', 'Charles', 'Darwin', '1809-02-12', '1882-04-19'),
('Sagan001', 'Carl', 'Sagan', '1934-11-09', '1996-12-20');

INSERT INTO Libri (ISBNLibro, Titolo, CodAutore, Anno, Categoria, Prezzo) VALUES
('9780553380163', 'A Brief History of Time', 'Hawk001', 1988, 'Physics', 15.99),
('9781509852826', 'On the Origin of Species', 'Darw001', 1859, 'Biology', 12.50),
('9780345331359', 'Cosmos', 'Sagan001', 1980, 'Astronomy', 14.99);

INSERT INTO Autori (CodAutore, Nome, Cognome, DataNascita, DataMorte) VALUES
('Ein001', 'Albert', 'Einstein', '1879-03-14', '1955-04-18');