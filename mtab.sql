CREATE DATABASE mtab_db;

USE mtab_db;

/* część o pracownikach */
CREATE TABLE Pracownik(
	id_pracownika INT NOT NULL AUTO_INCREMENT,
	imie varchar(60) NOT NULL,
	nazwisko varchar(60) NOT NULL,
	telefon varchar(9),
	mail varchar(30),
	PRIMARY KEY (id_pracownika)
);

CREATE TABLE Stanowisko(
	id_stanowiska INT NOT NULL AUTO_INCREMENT,
	opis_stanowiska varchar(60) NOT NULL,
	PRIMARY KEY(id_stanowiska)
);

CREATE TABLE Etat(
	id_etatu INT NOT NULL AUTO_INCREMENT,
	od varchar(8) NOT NULL,
	do varchar(8),
	pensja INT NOT NULL,
	id_stanowiska INT NOT NULL,
	id_pracownika INT NOT NULL,
	PRIMARY KEY (id_etatu),
	FOREIGN KEY (id_stanowiska) REFERENCES Stanowisko(id_stanowiska),
	FOREIGN KEY (id_pracownika) REFERENCES Pracownik(id_pracownika) 
);

/*część o magazynie i sklepie */

CREATE TABLE Kategoria(
	id_kategorii INT NOT NULL AUTO_INCREMENT,
	opis_kategorii varchar(60) NOT NULL,
	PRIMARY KEY (id_kategorii)
);
	
CREATE TABLE Firma(
	id_firmy INT NOT NULL AUTO_INCREMENT,
	rodzaj_firmy varchar(20) NOT NULL,
	nazwa_firmy varchar(20) NOT NULL,	
	adres varchar(60),
	telefon varchar(9),
	PRIMARY KEY (id_firmy)
);

CREATE TABLE Produkt(
	id_produktu INT NOT NULL AUTO_INCREMENT,
	id_kategorii INT NOT NULL,
	id_firmy INT,
	nazwa varchar(20) NOT NULL,
	opis varchar(60),
	cena_sugerowana INT NOT NULL,
	PRIMARY KEY (id_produktu),
	FOREIGN KEY (id_kategorii) REFERENCES Kategoria (id_kategorii),
	FOREIGN KEY (id_firmy) REFERENCES Firma (id_firmy)
);

CREATE TABLE Magazyn(
	id_towaru INT NOT NULL AUTO_INCREMENT,
	id_produktu INT NOT NULL,
	ilosc INT NOT NULL,
	komentarz varchar(60),
	PRIMARY KEY (id_towaru),
	FOREIGN KEY (id_produktu) REFERENCES Produkt (id_produktu)
);

CREATE TABLE Sklep_detaliczny(
	id_towaru INT NOT NULL AUTO_INCREMENT,
	id_produktu INT NOT NULL,
	cena_produktu INT NOT NULL,
	ilosc_na_stanie INT,
	komentarz varchar(60),
	PRIMARY KEY (id_towaru),
	FOREIGN KEY (id_produktu) REFERENCES Produkt (id_produktu)
);

CREATE TABLE Transakcje_detaliczne(
	id_transakcji_det INT NOT NULL AUTO_INCREMENT,
	id_produktu INT NOT NULL,
	cena INT NOT NULL,
	ilosc INT NOT NULL,
	data varchar(8) NOT NULL,
	PRIMARY KEY (id_transakcji_det),
	FOREIGN KEY (id_produktu) REFERENCES Produkt (id_produktu)
);

CREATE TABLE Zamowienie(
	id_zamowienia INT NOT NULL AUTO_INCREMENT,
	id_produktu INT NOT NULL,
	cena_produktu INT NOT NULL,
	ilosc_produktu INT NOT NULL,
	PRIMARY KEY (id_zamowienia),
	FOREIGN KEY (id_produktu) REFERENCES Produkt (id_produktu)
);

CREATE TABLE Transakcja_hurtowa(
	id_transakcji INT NOT NULL AUTO_INCREMENT,
	id_firmy INT NOT NULL,
	data varchar(8),
	rodzaj_transakcji varchar(20),
	id_zamowienia INT NOT NULL,
	PRIMARY KEY (id_transakcji),
	FOREIGN KEY (id_firmy) REFERENCES Firma (id_firmy),
	FOREIGN KEY (id_zamowienia) REFERENCES Zamowienie (id_zamowienia)
);


/* troche insertów do testowania bazy */
USE mtab_db;

/*pracownicy i etaty*/
INSERT INTO Pracownik (imie, nazwisko)
VALUES ('Jan', 'Kowalski');

INSERT INTO Pracownik (imie, nazwisko, telefon)
VALUES ('Janusz', 'Kowalczyk','123456789');

INSERT INTO Pracownik (imie, nazwisko, telefon, mail)
VALUES ('Janina', 'Nowak','123987654','janina.nowak@gmail.com');

INSERT INTO Pracownik (imie, nazwisko, telefon, mail)
VALUES ('Angus', 'Mlody','987666321','high@voltage.com');

INSERT INTO Stanowisko (opis_stanowiska)
VALUES ('Magazynier');

INSERT INTO Stanowisko (opis_stanowiska)
VALUES ('Sprzedawca');

INSERT INTO Stanowisko (opis_stanowiska)
VALUES ('Szef wszystkich szefow');

INSERT INTO Etat (od, do, pensja, id_stanowiska, id_pracownika)
VALUES ('02022015','06122015','3000','1','1');

INSERT INTO Etat (od, pensja, id_stanowiska, id_pracownika)
VALUES ('04122015','3000','1','2');

INSERT INTO Etat (od, pensja, id_stanowiska, id_pracownika)
VALUES ('06012015','3000','2','3');

INSERT INTO Etat (od, pensja, id_stanowiska, id_pracownika)
VALUES ('01012015','20000','3','4');

/*magazyn i sklep*/
INSERT INTO Kategoria(opis_kategorii)
VALUES ('Gitara elektryczna');

INSERT INTO Kategoria(opis_kategorii)
VALUES ('Gitara basowa');

INSERT INTO Kategoria(opis_kategorii)
VALUES ('Struny');

INSERT INTO Firma (rodzaj_firmy, nazwa_firmy)
VALUES ('Producent','Fender');

INSERT INTO Firma (rodzaj_firmy, nazwa_firmy)
VALUES ('Producent','Ernie Ball');

INSERT INTO Produkt (id_kategorii, id_firmy, nazwa, cena_sugerowana)
VALUES ('1','1','Stratocaster','3500');

INSERT INTO Produkt (id_kategorii, id_firmy, nazwa, cena_sugerowana)
VALUES ('1','1','Telecaster','3500');

INSERT INTO Produkt (id_kategorii, id_firmy, nazwa, opis, cena_sugerowana)
VALUES ('3','2','Regular Slinky','10-46','18');

INSERT INTO Magazyn (id_produktu, ilosc)
VALUES ('1','3');

INSERT INTO Magazyn (id_produktu, ilosc)
VALUES ('2','2');

INSERT INTO Magazyn (id_produktu, ilosc)
VALUES ('3','10');

INSERT INTO Sklep_detaliczny (id_produktu, cena_produktu, ilosc_na_stanie)
VALUES ('1','3000','1');

INSERT INTO Sklep_detaliczny (id_produktu, cena_produktu, ilosc_na_stanie, komentarz)
VALUES ('1','2500','1','Po ekspozycji');

INSERT INTO Sklep_detaliczny (id_produktu, cena_produktu, ilosc_na_stanie)
VALUES ('2','3500','1');

INSERT INTO Sklep_detaliczny (id_produktu, cena_produktu, ilosc_na_stanie)
VALUES ('3','25','5');

INSERT INTO Transakcje_detaliczne (id_produktu, cena, ilosc, data)
VALUES ('3','25','2','02042015');

INSERT INTO Zamowienie (id_produktu, cena_produktu, ilosc_produktu)
VALUES ('3','13','10');

INSERT INTO Transakcja_hurtowa (id_firmy, data, rodzaj_transakcji, id_zamowienia)
VALUES ('2','03042015','kupno','1');

