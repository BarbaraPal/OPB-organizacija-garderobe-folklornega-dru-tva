-- Active: 1691238531235@@baza.fmf.uni-lj.si@5432@sem2023_majaa@public
CREATE TYPE spol12 AS ENUM ('M', 'Ž');
CREATE TYPE delo1234 AS ENUM ('šivanje', 'pranje', 'likanje', 'drugo');
CREATE TYPE tip1234 AS ENUM ('ZgornjiDel', 'SpodnjiDel', 'EnodelniKos', 'DodatnaOblacila');
CREATE TYPE spol123 AS ENUM ('M', 'Ž', 'UNI');

CREATE TABLE TipImena(
    Ime TEXT PRIMARY KEY,
    Tip tip1234 NOT NULL
);

CREATE TABLE VrstaOblacila(
    Pokrajina TEXT DEFAULT 'SLO',
    Spol spol12 NOT NULL, 
    Omara INTEGER,
    Ime TEXT NOT NULL,
    FOREIGN KEY (Ime) REFERENCES TipImena(Ime), 
    PRIMARY KEY (Pokrajina, Ime, Spol)
);

CREATE TABLE DodatnaOblacila (
    Pokrajina TEXT,
    Spol spol12,
    Ime TEXT, 
    Kolicina INT DEFAULT 0,
    Opombe TEXT,
    Slika BYTEA,
    FOREIGN KEY (Ime, Pokrajina, Spol) REFERENCES VrstaOblacila(Ime, Pokrajina, Spol) ON DELETE CASCADE,
    PRIMARY KEY (Ime, Pokrajina, Spol)
);

CREATE TABLE GlavnaOblacila (
    ZaporednaSt INT,
    Barva TEXT, 
    Stanje BOOLEAN DEFAULT TRUE,
    Opombe TEXT, 
    Slika BYTEA DEFAULT NULL,
    Ime TEXT,
    Pokrajina TEXT,
    Spol spol12,
    FOREIGN KEY (Ime, Pokrajina, Spol) REFERENCES VrstaOblacila(Ime, Pokrajina, Spol) ON DELETE CASCADE,
    PRIMARY KEY(Ime, Pokrajina, Spol, ZaporednaSt)
);

CREATE TABLE ZgornjiDel (
    Ime TEXT,
    Pokrajina TEXT,
    Spol spol12,
    ZaporednaSt INT,
    SirinaRamen DECIMAL,
    ObsegPrsi DECIMAL,
    DolzinaRokava DECIMAL,
    FOREIGN KEY (Ime, Pokrajina, Spol, ZaporednaSt) REFERENCES GlavnaOblacila(Ime, Pokrajina, Spol, ZaporednaSt) ON DELETE CASCADE,
    PRIMARY KEY (Ime, Pokrajina, Spol, ZaporednaSt)
);

CREATE TABLE SpodnjiDel (
    Ime TEXT,
    Pokrajina TEXT,
    Spol spol12,
    ZaporednaSt INT,
    DolzinaOdPasuNavzdol DECIMAL,
    FOREIGN KEY (Ime, Pokrajina, Spol, ZaporednaSt) REFERENCES GlavnaOblacila(Ime, Pokrajina, Spol, ZaporednaSt) ON DELETE CASCADE,
    PRIMARY KEY (Ime, Pokrajina, Spol, ZaporednaSt)
    );


CREATE TABLE EnodelniKos (
    Ime TEXT,
    Pokrajina TEXT,
    Spol spol12,
    ZaporednaSt INT,
    DolzinaTelesa DECIMAL,
    FOREIGN KEY (Ime, Pokrajina, Spol, ZaporednaSt) REFERENCES GlavnaOblacila(Ime, Pokrajina, Spol, ZaporednaSt) ON DELETE CASCADE,
    PRIMARY KEY (Ime, Pokrajina, Spol, ZaporednaSt)
    );

CREATE TABLE Plesalec (
    Emso TEXT PRIMARY KEY,
    Ime TEXT NOT NULL,
    Priimek TEXT NOT NULL,
    SpolPlesalca spol12 NOT NULL,
    DatumPrikljucitve DATE DEFAULT now(),
    SirinaRamen DECIMAL,
    ObsegPrsi DECIMAL,
    DolzinaRokava DECIMAL,
    DolzinaOdPasuNavzdol DECIMAL,
    DolzinaTelesa DECIMAL,
    StevilkaNoge DECIMAL
);

CREATE TABLE TipCevljev (
    Vrsta TEXT PRIMARY KEY,
    Slika BYTEA
);

CREATE TABLE Cevlji (
    Vrsta TEXT,
    ZapSt INT NOT NULL,
    Velikost INTEGER NOT NULL,
    EmsoLastnika TEXT,
    FOREIGN KEY (EmsoLastnika) REFERENCES Plesalec(Emso) ON DELETE SET NULL,
    FOREIGN KEY (Vrsta) REFERENCES TipCevljev(Vrsta) ON DELETE CASCADE,
    PRIMARY KEY (Vrsta, Velikost, ZapSt)
);

CREATE TABLE Delo (
    IdDela SERIAL PRIMARY KEY,
    VrstaDela delo1234 NOT NULL, 
    DatumIzvajanja DATE DEFAULT now(),
    Trajanje INTERVAL MINUTE NOT NULL,
    Emso TEXT NOT NULL,
    FOREIGN KEY (Emso) REFERENCES Plesalec(Emso) ON DELETE CASCADE
);

CREATE TABLE OpravaKostumskePodobe (
    ImeKostumskePodobe TEXT NOT NULL, 
    ImeOprave TEXT NOT NULL,
    SpolOprave spol123 NOT NULL,
    Posebnosti TEXT,
    VrstaCevljev TEXT,
    FOREIGN KEY (VrstaCevljev) REFERENCES TipCevljev(Vrsta) ON DELETE SET NULL, 
    PRIMARY KEY (ImeKostumskePodobe, ImeOprave) 
);

CREATE TABLE ROpravaVrsta (
    PokrajinaVrste TEXT,
    SpolVrste spol12, 
    ImeVrste TEXT,
    ImeOprave TEXT,
    ImeKostumskePodobe TEXT,
    Moznost INT DEFAULT 0,
    FOREIGN KEY (PokrajinaVrste, ImeVrste, SpolVrste) REFERENCES VrstaOblacila(Pokrajina, Ime, Spol) ON DELETE CASCADE,
    FOREIGN KEY (ImeOprave,ImeKostumskePodobe) REFERENCES OpravaKostumskePodobe(ImeOprave,ImeKostumskePodobe) ON DELETE CASCADE,
    PRIMARY KEY (ImeOprave, ImeKostumskePodobe, PokrajinaVrste, ImeVrste, SpolVrste) 
);

CREATE TABLE Uporabnik (
    uporabniskoime TEXT PRIMARY KEY,
    kodiranogeslo TEXT NOT NULL,
    zadnjaprijava DATE,
    rola BOOLEAN DEFAULT FALSE,
    Emso TEXT, 
    FOREIGN KEY (Emso) REFERENCES Plesalec(Emso) ON DELETE CASCADE
);

GRANT ALL PRIVILEGES ON DATABASE sem2023_majaa TO barbarap WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON SCHEMA public TO barbarap WITH GRANT OPTION;
GRANT ALL ON ALL TABLES IN SCHEMA public TO barbarap WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO barbarap WITH GRANT OPTION;

GRANT CONNECT ON DATABASE sem2023_majaa TO javnost;
GRANT USAGE ON SCHEMA public TO javnost;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO javnost;
GRANT ALL PRIVILEGES ON SCHEMA PUBLIC to javnost;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO javnost;
                