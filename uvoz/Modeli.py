from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List
from datetime import date

# Predlagam uporabo (vsaj) dataclass-ov

# Nahitro dataclass doda nekaj bližnjic za delo z razredi in omogoča tudi nekaj bolj naprednih funkcij,
# ki jih načeloma najdemo v bolj tipiziranih jezik kot so C#, Java, C++,..

# Knjižnjica dataclasses_json je nadgradnja za delo z dataclasses in omogoča predvsem
# preprosto serializacijo in deseralizacijo objektov. Poleg tega vsebuje tudi uporabno funkcijo
# to_dict() in from_dict(), ki dataclas pretvori v/iz slovarja.
@dataclass_json
@dataclass
class OpravaKostumskePodobe:
    Ime: str = field(default="")
    ZaporednaSt: int = field(default=0)
    KraticaKP: str = field(default="")
    SpolOprave: bool = field(default=False) # False = M, True = Ž
    Posebnosti: str = field(default="")

@dataclass_json
@dataclass
class VrstaOblacila:
    Id: str = field(default="0000")
    Pokrajina: str = field(default="SLO")
    Ime: str = field(default="")
    SpolOprave: bool = field(default=False) # False = M, True = Ž
    Omara: int = field(default=None)

@dataclass_json
@dataclass
class ZgornjiDel:
    IdVrste: str = field(default="0000")
    ZaporednaSt: int = field(default=0)
    Barva: str = field(default="")
    SirinaRamen: float = field(default=0)
    ObsegPrsi: float = field(default=0)
    DolzinaRokava: float = field(default=0)
    Stanje: bool = field(default=True) # False = neuporabno, True = uporabno
    Opombe: str = field(default="")
    Slika: List[str] = field(default_factory=list)

@dataclass_json
@dataclass
class SpodnjiDel:
    IdVrste: str = field(default="0000")
    ZaporednaSt: int = field(default=0)
    Barva: str = field(default="")
    DolzinaOdPasuNavzdol: float = field(default=0)
    Stanje: bool = field(default=True) # False = neuporabno, True = uporabno
    Opombe: str = field(default="")
    Slika: List[str] = field(default_factory=list)

@dataclass_json
@dataclass
class EnodelniKos:
    IdVrste: str = field(default="0000")
    ZaporednaSt: int = field(default=0)
    Barva: str = field(default="")
    DolzinaOdPasuNavzdol: float = field(default=0)
    Stanje: bool = field(default=True) # False = neuporabno, True = uporabno
    Opombe: str = field(default="")
    Slika: List[str] = field(default_factory=list)

@dataclass_json
@dataclass
class DodatnaOblacila:
    IdVrste: str = field(default="0000")
    Kolicina: int = field(default=0)
    Opombe: str = field(default="")
    Slika: List[str] = field(default_factory=list)

@dataclass_json
@dataclass
class Plesalec:
    IdPlesalca: int = field(default=100)
    Ime: str = field(default="")
    Priimek: str = field(default="")
    SpolPlesalca: bool = field(default=False)   # False = M, True = Ž
    DatumPrikljucitve: date = field(default=date.today())
    DodatnaFunkcija: bool = field(default=False)

@dataclass_json
@dataclass
class Velikost:
    IdVelikosti: int = field(default=0)
    SirinaRamen: float = field(default=0)
    ObsegPrsi: float = field(default=0)
    DolzinaRokava: float = field(default=0)
    DolzinaOdPasuNavzdol: float = field(default=0)
    DolzinaTelesa: float = field(default=0)
    StevilkaNoge: int = field(default=0)

@dataclass_json
@dataclass
class TipCevljev:
    IdTipaCevljev: str = field(default="00")
    Vrsta: str = field(default="")
    Slika: List[str] = field(default_factory=list)

@dataclass_json
@dataclass
class Cevlji:
    IdCevljev: int = field(default=0)
    ZapSt: int = field(default=0)
    TipCevljev: str = field(default="")
    IdLastnika: int = field(default=None)

@dataclass_json
@dataclass
class Delo:
    IdDela: int = field(default=0)
    VrstaDela: str = field(default="")
    DatumIzvajanja: date = field(default=date.today())
    Trajanje: int = field(default=0)
