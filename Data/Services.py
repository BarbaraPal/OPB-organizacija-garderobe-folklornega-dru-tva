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
            uporabnik = self.repo.dobi_gen_id(Uporabnik, uporabnik, id_col="uporabniskoime")
            return True
        except:
            return False

    def prijavi_uporabnika(self, uporabnik : str, geslo: str) -> UporabnikDto | bool :

        # Najprej dobimo uporabnika iz baze
        user = self.repo.dobi_gen_id(Uporabnik, uporabnik, id_col="uporabniskoime")
        geslo_bytes = geslo.encode('utf-8')
        # Ustvarimo hash iz gesla, ki ga je vnesel uporabnik
        succ = bcrypt.checkpw(geslo_bytes, user.kodiranogeslo.encode('utf-8'))

        if succ:
            # popravimo last login time
            user.zadnjaprijava = date.today().isoformat()
            self.repo.posodobi_gen(user, id_col="uporabniskoime")
            return UporabnikDto(uporabniskoime=user.uporabniskoime, rola=user.rola)
        
        return False

    def dodaj_uporabnika(self, uporabnik: str, role: bool, geslo: str) -> UporabnikDto:

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
            kodiranogeslo=kodiranogeslo.decode(),
            zadnjaprijava= date.today().isoformat()
        )

        self.repo.dodaj_gen(uporabnik, serial_col=None)

        return UporabnikDto(uporabniskoime=uporabnik, rola=role)