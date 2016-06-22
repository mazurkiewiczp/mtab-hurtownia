CREATE DATABASE mtab_db;

USE mtab_db

/* część o pracownikach */
CREATE TABLE Pracownik(
	id_pracownika INT NOT NULL,
	imie varchar(60),
	nazwisko varchar(60),
	telefon varchar(9),
	mail varchar(30),
	PRIMARY KEY (id_pracownika)
);

CREATE TABLE Stanowisko(
	id_stanowiska INT NOT NULL,
	opis_stanowiska varchar(60),
	PRIMARY KEY(id_stanowiska)
);

CREATE TABLE Etat(
	id_etatu INT NOT NULL,
	od varchar(8) NOT NULL,
	do varchar(8),
	pensja INT NOT NULL,
	id_stanowiska INT,
	id_pracownika INT,
	PRIMARY KEY (id_etatu),
	FOREIGN KEY (id_stanowiska) REFERENCES Stanowisko(id_stanowiska),
	FOREIGN KEY (id_pracownika) REFERENCES Pracownik(id_pracownika) 
);

/*część o magazynie i sklepie */

CREATE TABLE Kategoria(
	id_kategorii INT NOT NULL,
	opis_kategorii varchar(60),
	PRIMARY KEY (id_kategorii)
);
	
CREATE TABLE Klient(
	id_klienta INT NOT NULL,
	rodzaj_klienta varchar(20),
	adres varchar(60),
	telefon varchar(9),
	PRIMARY KEY (id_klienta)
);

CREATE TABLE Produkt(
	id_produktu INT NOT NULL,
	id_kategorii INT,
	id_klienta INT,
	nazwa varchar(20),
	opis varchar(60),
	PRIMARY KEY (id_produktu),
	FOREIGN KEY (id_kategorii) REFERENCES Kategoria (id_kategorii),
	FOREIGN KEY (id_klienta) REFERENCES Klient (id_klienta)
);

CREATE TABLE Magazyn(
	id_produktu INT NOT NULL,
	ilosc INT,
	lokalizacja varchar(60),
	FOREIGN KEY (id_produktu) REFERENCES Produkt (id_produktu)
);

CREATE TABLE Sklep_detaliczny(
	id_produktu INT NOT NULL,
	cena_produktu INT NOT NULL,
	ilosc_na_stanie INT,
	FOREIGN KEY (id_produktu) REFERENCES Produkt (id_produktu)
);

CREATE TABLE Transakcje_detaliczne(
	id_transakcji_det INT NOT NULL,
	id_produktu INT,
	cena INT,
	ilosc INT,
	data varchar(8),
	PRIMARY KEY (id_transakcji_det),
	FOREIGN KEY (id_produktu) REFERENCES Produkt (id_produktu)
);

CREATE TABLE Zamowienie(
	id_zamowienia INT NOT NULL,
	id_produktu INT,
	cena_produktu INT,
	ilosc_produktu INT,
	PRIMARY KEY (id_zamowienia),
	FOREIGN KEY (id_produktu) REFERENCES Produkt (id_produktu)
);

CREATE TABLE Transakcja_hurtowa(
	id_transakcji INT NOT NULL,
	id_klienta INT,
	data varchar(8),
	rodzaj_transakcji varchar(20),
	id_zamowienia INT,
	PRIMARY KEY (id_transakcji),
	FOREIGN KEY (id_klienta) REFERENCES Klient (id_klienta),
	FOREIGN KEY (id_zamowienia) REFERENCES Zamowienie (id_zamowienia)
);
