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
class TipImena:
    ime: str
    tip: str

@dataclass_json
@dataclass
class VrstaOblacila:
    ime: str
    spol: str
    pokrajina: str = field(default='SLO') 
    omara: int = field(default=None)

@dataclass
class VrstaOblacilaDto:
    ime: str
    spol: str
    pokrajina: str
    omara: int
    tip: str

@dataclass_json
@dataclass
class DodatnaOblacila:
    pokrajina: str
    spol: str
    ime: str
    slika: bytes = field(default=None)
    kolicina: int = field(default=0)
    opombe: str = field(default="")

@dataclass
class DodatnaOblacilaDto:
    kolicina: int
    opombe: str
    slika: bytes

# Apply the custom decoder configuration
@dataclass_json
@dataclass
class GlavnaOblacila:
    pokrajina: str
    spol: str
    ime: str
    zaporednast: int
    slika: bytes = field(default=None)
    barva: str = field(default="")
    stanje: bool = field(default=True) # False = neuporabno, True = uporabno
    opombe: str = field(default="")

@dataclass
class GlavnaOblacilaDto:
    pokrajina: str
    spol: str
    ime: str
    zaporednast: int
    stanje: bool

@dataclass_json
@dataclass
class ZgornjiDel:
    pokrajina: str
    spol: str
    ime: str
    zaporednast: int
    sirinaramen: Decimal = field(default=None)
    obsegprsi: Decimal = field(default=None)
    dolzinarokava: Decimal = field(default=None)

@dataclass
class ZgornjiDelDto: 
    zaporednast: int
    barva: str
    stanje: bool
    opombe: str
    slika: bytes
    sirinaramen: Decimal
    obsegprsi: Decimal
    dolzinarokava: Decimal

@dataclass
class MereZgornjiDelDto:
    sirinaramen: Decimal
    obsegprsi: Decimal
    dolzinarokava: Decimal

@dataclass_json
@dataclass
class SpodnjiDel:
    pokrajina: str
    spol: str
    ime: str
    zaporednast: int
    dolzinaodpasunavzdol: Decimal = field(default=None)

@dataclass
class SpodnjiDelDto: 
    zaporednast: int
    barva: str
    stanje: bool
    opombe: str
    slika: bytes
    dolzinaodpasunavzdol: Decimal

@dataclass
class MereSpodnjiDelDto:
    dolzinaodpasunavzdol: Decimal

@dataclass_json
@dataclass
class EnodelniKos:
    pokrajina: str
    spol: str
    ime: str
    zaporednast: int
    dolzinatelesa: Decimal = field(default=None)

@dataclass
class EnodelniKosDto: 
    zaporednast: int
    barva: str
    stanje: bool
    opombe: str
    slika: bytes
    dolzinatelesa: Decimal

@dataclass
class MereEnodelniKosDto:
    dolzinatelesa: Decimal

@dataclass_json
@dataclass
class Plesalec:
    emso: str
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
    vrsta: str
    slika: bytes = field(default=None)

@dataclass_json
@dataclass
class Cevlji:
    vrsta: str
    zapst: int
    velikost: int
    emsolastnika: str = field(default=None)

@dataclass_json
@dataclass
class Delo:
    emso: str
    vrstadela: str
    trajanje: timedelta
    datumizvajanja: date = field(default=date.today())
    iddela: int = field(default=None)


@dataclass_json
@dataclass
class OpravaKostumskePodobe:
    imekostumskepodobe: str
    imeoprave: str
    spoloprave: str
    vrstacevljev: str = field(default=None)
    posebnosti: str = field(default="")

@dataclass_json
@dataclass
class ROpravaVrsta:
    pokrajinavrste: str
    spolvrste: str 
    imevrste: str
    imeoprave: str
    imekostumskepodobe: str
    moznost: int

@dataclass
class OpravaDto:
    ime: str
    spol: str
    moznost: int
    pokrajina: str = field(default='SLO') 
    omara: int = field(default=None)


@dataclass_json
@dataclass
class Uporabnik:
    uporabniskoime: str
    kodiranogeslo: str 
    zadnjaprijava: date
    emso: str
    rola: bool = field(default=False)

@dataclass
class UporabnikDto:
    uporabniskoime: str
    rola: bool = field(default=False)

@dataclass
class PlesalecDto:
    emso: str
    uporabniskoime: str
    ime: str
    priimek: str
    spolplesalca: str
    datumprikljucitve: str = field(default="")
    sirinaramen: Decimal = field(default=None)
    obsegprsi: Decimal = field(default=None)
    dolzinarokava: Decimal = field(default=None)
    dolzinaodpasunavzdol: Decimal = field(default=None)
    dolzinatelesa: Decimal = field(default=None)
    stevilkanoge: Decimal = field(default=None)
    rola: bool = field(default=False)

@dataclass
class MerePlesalcaDto:
    sirinaramen: Decimal
    obsegprsi: Decimal
    dolzinarokava: Decimal
    dolzinaodpasunavzdol: Decimal
    dolzinatelesa: Decimal

@dataclass
class CevljiDto:
    emsolastnika: str
    vrsta: str
    velikost: int
    zapst: int

@dataclass
class CevljiDto2:
    emsolastnika: str
    vrsta: str
    velikost: int
    zapst: int
    ime: str
    priimek: str

@dataclass
class TipiCevljevDto:
    vrsta: str

@dataclass
class SlikeCevljevDto:
    vrsta: str
    slika: bytes = field(default=None) 

@dataclass
class DeloDto:
    emso: str
    vrstadela: str
    skupno_trajanje: timedelta

@dataclass
class OpravaKostumskePodobeDto:
    imekostumskepodobe: str
    imeoprave: str
    spoloprave: str
    vrstacevljev: str
    posebnosti: str = field(default="")
