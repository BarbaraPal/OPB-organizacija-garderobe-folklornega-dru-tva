from Data.Database import Repo
from Data.Modeli import *
from typing import Dict
from re import sub
import dataclasses
import bcrypt
from typing import Type
from datetime import date

class AuthService:

    repo : Repo
    def __init__(self, repo : Repo):
        
        self.repo = repo

    def obstaja_uporabnik(self, uporabnik: str) -> bool:
        try:
            uporabnik = self.repo.dobi_gen_id(Uporabnik, (uporabnik,), id_cols=("uporabniskoime",))
            return True
        except:
            return False

    def prijavi_uporabnika(self, uporabnik : str, geslo: str) -> UporabnikDto | bool :

        # Najprej dobimo uporabnika iz baze
        user = self.repo.dobi_gen_id(Uporabnik, (uporabnik,), id_cols=("uporabniskoime",))
        geslo_bytes = geslo.encode('utf-8')
        # Ustvarimo hash iz gesla, ki ga je vnesel uporabnik
        succ = bcrypt.checkpw(geslo_bytes, user.kodiranogeslo.encode('utf-8'))

        if succ:
            # popravimo last login time
            user.zadnjaprijava = date.today().isoformat()
            self.repo.posodobi_gen(user, id_cols=("uporabniskoime",))
            return UporabnikDto(uporabniskoime=user.uporabniskoime, rola=user.rola)
        
        return False

    def dodaj_uporabnika(self, uporabnik: str, role: bool, geslo: str, idplesalca: int) -> UporabnikDto:

        # zgradimo hash za geslo od uporabnika

        # Najprej geslo zakodiramo kot seznam bajtov
        bytes = geslo.encode('utf-8')
  
        # Nato ustvarimo salt
        salt = bcrypt.gensalt()
        
        # In na koncu ustvarimo hash gesla
        kodiranogeslo = bcrypt.hashpw(bytes, salt)

        # Sedaj ustvarimo objekt Uporabnik in ga zapišemo bazo

        uporabnik = Uporabnik(
            uporabniskoime=uporabnik,
            rola=role,
            idplesalca=idplesalca,
            kodiranogeslo=kodiranogeslo.decode(),
            zadnjaprijava= date.today().isoformat()
        )

        self.repo.dodaj_gen(uporabnik, serial_col=None)

        return UporabnikDto(uporabniskoime=uporabnik, rola=role)

    def sprememba_gesla(self, uporabnisko_ime: str, staro_geslo: str, novo_geslo: str):
        uporabnik = self.repo.dobi_gen_id(Uporabnik, (uporabnisko_ime,), id_cols=("uporabniskoime",))
        
        staro_geslo_bytes = staro_geslo.encode('utf-8')
        succ = bcrypt.checkpw(staro_geslo_bytes, uporabnik.kodiranogeslo.encode('utf-8'))
        if succ:
            bytes = novo_geslo.encode('utf-8')
            salt = bcrypt.gensalt()
            novo_kodirano_geslo = bcrypt.hashpw(bytes, salt)
            uporabnik.kodiranogeslo = novo_kodirano_geslo.decode('utf-8')
            self.repo.posodobi_gen(uporabnik, id_cols=("uporabniskoime",))
            return True
        return False        

