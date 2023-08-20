# Organizacija garderobe folklornega društva
Projekt pri predmetu Osnove podatkovnih baz

* [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/BarbaraPal/OPB-organizacija-garderobe-folklornega-dru-tva/master?labpath=proxy%2F8080)

## Opis
Aplikacija je v prvi vrsti namenjena garderoberjem folklornega društva, je pa uporabna tudi za navadne plesalce.

Pogled garderoberjev:
- svoj profil
- aktivni plesalci, dodajanje in brisanje plesalcev, pregled njihovih podatkov in možnost spreminjanja teh podatkov ter možnost dodajanja uporabniških računov plesalcem
- pregled nad vrstami oblačil in kosi oblačil, možnost dodajanja novih kosov, brisanja kosov ali cele vrste oblačil, možnost urejanja že vnešenih kosov
- pregled nad vsemi pari čevljev in njihovimi lastniki, možnost spreminjanja lastništva čevljev, dodajanje čevljev in pregled nad obstoječimi tipi čevljev ter možnost brisanja le teh
- pregled nad opravami kostumskih podob in možnost njihovega urejanja
- dodeljevanje oblačil za nastop: garderober izbere plesalce in kose oblačil, aplikacija pa vrne plesalce z dodeljenimi kosi oblačil, tako da so oblačila plesalcem čibolj prav 
- možnost dodajanja dela za kateregakoli plesalca in pregled statistike dela za posameznega plesalca

Pogled navadnega uporabnika:
- svoj profil
- pregled vseh vrst oblačil in kosov teh oblačil s slikami
- pregled nad vsemi pari čevljev in njihovimi lastniki ter slike tipov čevljev
- pregled nad opravami kostumskih podob
- možnost dodajanja svojega dela in pogled na svojo statistiko dela

## ER diagram

![ER diagram](ERdiagram.png)

<!-- 
## Aplikacija

Aplikacijo zaženemo tako, da poženemo program [`primer.py`](primer.py), npr.
```bash
python primer.py
```
Za delovanje je potrebno še sledeče:
* [`auth_public.py`](auth_public.py) - podatki za prijavo na bazo
* [`bottle.py`](bottle.py) - knjižnica za spletni strežnik
* [`bottleext.py`](bottleext.py) - dopolnitve knjižnice `bottle.py` za lažje delo
* [`static/`](static/) - mapa s statičnimi datotekami
* [`views/`](views/) - mapa s predlogami


## Binder

Aplikacijo je mogoče poganjati tudi na spletu z orodjem [Binder](https://mybinder.org/). V ta namen so v mapi [`binder/`](binder/) še sledeče datoteke:
* [`requirements.txt`](binder/requirements.txt) - seznam potrebnih Pythonovih paketov za namestitev s [`pip`](https://pypi.org/project/pip/)
* [`postBuild`](binder/postBuild) - skripta, ki se požene po namestitvi paketov in poskrbi za nastavitev posrednika za spletni strežnik
* [`start`](binder/start) - skripta za zagon aplikacije (spremenljivka `BOTTLE_RUNTIME` poda ime glavnega programa)

Zaradi omejitev javne storitve [Binder](https://mybinder.org/) se povezava z bazo vzpostavi na vratih 443 (namesto običajnih 5432), za kar je bila potrebna posebna nastavitev strežnika.

Zgornje skripte je možno prilagoditi tudi za druga ogrodja, kot npr. [Flask](https://palletsprojects.com/p/flask/) ali [Django](https://www.djangoproject.com/).

 -->
