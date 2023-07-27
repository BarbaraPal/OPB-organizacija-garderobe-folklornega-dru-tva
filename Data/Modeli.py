from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List
from datetime import date, datetime, timedelta

from enum import Enum
from decimal import Decimal

# Predlagam uporabo (vsaj) dataclass-ov

# Nahitro dataclass doda nekaj bližnjic za delo z razredi in omogoča tudi nekaj bolj naprednih funkcij,
# ki jih načeloma najdemo v bolj tipiziranih jezik kot so C#, Java, C++,..

# Knjižnjica dataclasses_json je nadgradnja za delo z dataclasses in omogoča predvsem
# preprosto serializacijo in deseralizacijo objektov. Poleg tega vsebuje tudi uporabno funkcijo
# to_dict() in from_dict(), ki dataclas pretvori v/iz slovarja.


@dataclass_json
@dataclass
class VrstaOblacila:
    id: int
    ime: str
    spol: str
    pokrajina: str = field(default='SLO') 
    omara: int = field(default=None)

@dataclass_json
@dataclass
class GlavnaOblacila:
    zaporednast: int
    idvrste: int
    slika: bytes = field(default=None)
    barva: str = field(default="")
    stanje: bool = field(default=True) # False = neuporabno, True = uporabno
    opombe: str = field(default="")

#@dataclass
#class GlavnaOblacilaDto:
#    ime: str
#    pokrajina: str
#    spol: str
#    zaporednast: int
#    barva: str
  
@dataclass_json
@dataclass
class ZgornjiDel:
    idvrste: int 
    zaporednast: int
    sirinaramen: Decimal = field(default=None)
    obsegprsi: Decimal = field(default=None)
    dolzinarokava: Decimal = field(default=None)

@dataclass_json
@dataclass
class SpodnjiDel:
    idvrste: int
    zaporednast: int
    dolzinaodpasunavzdol: Decimal = field(default=None)

@dataclass_json
@dataclass
class EnodelniKos:
    idvrste: int
    zaporednast: int
    dolzinatelesa: Decimal = field(default=None)
    

@dataclass_json
@dataclass
class DodatnaOblacila:
    idvrste: int
    slika: bytes = field(default=None)
    kolicina: int = field(default=0)
    opombe: str = field(default="")

@dataclass_json
@dataclass
class Plesalec:
    idplesalca: int
    ime: str
    priimek: str
    spolplesalca: str
    datumprikljucitve: date = field(default=date.today())
    sirinaramen: Decimal = field(default=None)
    obsegprsi: Decimal = field(default=None)
    dolzinarokava: Decimal = field(default=None)
    dolzinaodpasunavzdol: Decimal = field(default=None)
    dolzinatelesa: Decimal = field(default=None)
    stevilkanoge: Decimal = field(default=None)
    
@dataclass_json
@dataclass
class TipCevljev:
    idtipacevljev: int
    vrsta: str
    slika: bytes = field(default=None)

@dataclass_json
@dataclass
class Cevlji:
    idtipacevljev: int
    zapst: int
    velikost: int
    idlastnika: int = field(default=None)

@dataclass_json
@dataclass
class Delo:
    iddela: int
    idplesalca: int
    vrstadela: str
    trajanje: timedelta
    datumizvajanja: date = field(default=date.today())
    

@dataclass_json
@dataclass
class OpravaKostumskePodobe:
    imekostumskepodobe: str
    imeoprave: str
    idtipacevljev: int
    posebnosti: str = field(default="")

@dataclass_json
@dataclass
class ROpravaVrsta:
    id: int
    idvrsteoblacila: int
    imeoprave: str
    imekostumskepodobe: str
    moznost: int


@dataclass_json
@dataclass
class Uporabnik:
    uporabniskoime: str
    kodiranogeslo: str 
    zadnjaprijava: date
    idplesalca: int
    rola: bool = field(default=False)

@dataclass
class UporabnikDto:
    uporabniskoime: str
    rola: bool = field(default=False)

@dataclass
class PlesalecDto:
    uporabniskoime: str
    ime: str
    priimek: str
    spolplesalca: str
    datumprikljucitve: date = field(default=date.today())
    sirinaramen: Decimal = field(default=None)
    obsegprsi: Decimal = field(default=None)
    dolzinarokava: Decimal = field(default=None)
    dolzinaodpasunavzdol: Decimal = field(default=None)
    dolzinatelesa: Decimal = field(default=None)
    stevilkanoge: Decimal = field(default=None)
    rola: bool = field(default=False)

@dataclass
class CevljiDto:
    uporabniskoime: str
    vrsta: str
    velikost: int
    zapst: int

@dataclass
class DeloDto:
    uporabniskoime: str
    vrstadela: str
    skupno_trajanje: timedelta
