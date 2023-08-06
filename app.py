#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
#from bottleext import get, post, run, request, template, redirect, static_file, url, error, response, template_user
from bottleext import *
# uvozimo ustrezne podatke za povezavo

from Data.Database import Repo
from Data.Modeli import *

from Data.Services import AuthService
from functools import wraps

import os
import json

#import tracemalloc
#tracemalloc.start()

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# odkomentiraj, če želiš sporočila o napakah
#debug(True)

repo = Repo()

auth = AuthService(repo)

def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):

        cookie = request.get_cookie("uporabniskoime")
        if cookie:
            return f(*args, **kwargs)
        
        redirect(url('prijava'))

    return decorated

def rola_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):

        cookie_rola = request.get_cookie("rola")
        if cookie_rola == 'True':
            return f(*args, **kwargs)
        
        redirect(url('osnovna_stran'))

    return decorated

def pretvori_v_decimal(vrednost):
    try:
        return Decimal(vrednost)
    except:
        return None



@get('/static/<filename:path>')
def static(filename):
    path = './slike'
    return static_file(filename, root=path)

@get('/static_style/<filename:path>')
def static_style(filename):
    return static_file(filename, root='static')

@get('/static_js/<filename:path>')
def static_js(filename):
    return static_file(filename, root='static')

@get('/')
def index(): 
    redirect('/domov/')

@get('/prijava/') 
def prijava_get():
    """
    Prikaže prijavno stran.
    """
    cookie = request.get_cookie("uporabniskoime")
    if cookie:
        redirect(url('osnovna_stran'))
    return template("prijava.html", napaka=None)

@post('/prijava/')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovi roli.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.getunicode('uporabniskoime')
    password = request.forms.getunicode('geslo')

    if not auth.obstaja_uporabnik(username):
        return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja.")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabniskoime", username, path="/")
        response.set_cookie("rola", f'{prijava.rola}', path="/" )
        redirect(url('index'))

    else:
        return template("prijava.html", napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")

@post('/odjava/')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """

    response.delete_cookie("uporabniskoime", path='/')
    response.delete_cookie("rola", path='/')

    redirect(url('index'))

@get('/profil/')
@cookie_required
def podatki_o_profilu():
    """
    Prikaže podatke o uporabniku in še kaj.
    """
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    rola = bottle.request.get_cookie("rola")
    uporabnik = repo.profil(uporabnisko_ime)
    cevlji = repo.cevlji_posameznika(uporabnisko_ime)
    delo = repo.delo_posameznika(uporabnik.emso)
    for d in delo:
        d.skupno_trajanje = f'{d.skupno_trajanje.total_seconds() // 60} min'
    sprememba = bottle.request.query.get('sprememba')
    return template('profil.html', uporabnisko_ime = uporabnisko_ime, rola = rola, plesalecdto = uporabnik, cevljidto = cevlji, delodto = delo, sprememba = sprememba)
    
@post('/spremeni_geslo/')
@cookie_required
def spremeni_geslo():
    """
    Spremeni geslo trenutnega uporabnika
    """
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    staro_geslo = request.forms.getunicode('staro_geslo')
    novo_geslo = request.forms.getunicode('novo_geslo')
    sprememba = auth.sprememba_gesla(uporabnisko_ime, staro_geslo,novo_geslo)
    redirect(url('podatki_o_profilu', sprememba = sprememba))

@get('/domov/')
@cookie_required
def osnovna_stran():
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    rola = bottle.request.get_cookie("rola")
    return template('domov.html', uporabnisko_ime = uporabnisko_ime, rola = rola)

@get('/plesalci/<id>/')
@rola_required
def plesalci(id):
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    rola = bottle.request.get_cookie("rola")
    plesalci = repo.plesalci()
    seznam_imen = [plesalci[emso].uporabniskoime for emso in plesalci.keys() if plesalci[emso].uporabniskoime is not None]
    if id == 'vsi_plesalci':
        odziv = bottle.request.query.getunicode('odziv')
        return template('plesalci.html', uporabnisko_ime = uporabnisko_ime, rola =rola, plesalci = plesalci, odziv = odziv)
    else:
        napaka = bottle.request.query.getunicode('napaka')
        potrdilo = bottle.request.query.getunicode('potrdilo')
        potrdilo_mere = bottle.request.query.getunicode('potrdilo_mere')
        plesalec = plesalci[id]
        cevlji = repo.cevlji_posameznika(plesalec.emso)
        delo = repo.delo_posameznika(plesalec.emso)
        return template('podatki_plesalca.html', uporabnisko_ime = uporabnisko_ime, rola = rola, plesalecdto = plesalec, seznam_imen = seznam_imen, napaka = napaka, potrdilo = potrdilo, cevljidto = cevlji, delodto = delo, potrdilo_mere = potrdilo_mere)

@post('/dodaj_plesalca/')
@rola_required
def dodaj_plesalca():
    emso = request.forms.getunicode('emsonovega') 
    ime = request.forms.getunicode('ime')
    priimek = request.forms.getunicode('priimek')
    spol_plesalca = request.forms.getunicode('spol')
    datum_prikljucitve = datetime.strptime(request.forms.get('datum_prikljucitve'), '%Y-%m-%d').date()
    try:
        repo.dobi_gen_id(Plesalec, (emso,), id_cols=("emso",))
        odziv = 'Plesalec s temi podatki že obstaja!'
    except: 
        plesalec = Plesalec(emso,ime,priimek,spol_plesalca, datumprikljucitve=datum_prikljucitve)
        repo.dodaj_gen(plesalec, serial_col=None)
        odziv = 'Plesalec uspešno dodan!'
    redirect(url('plesalci', id = 'vsi_plesalci', odziv = odziv))

@post('/izbrisi_plesalca/')
@rola_required
def izbrisi_plesalca():
    emso_plesalca = request.forms.getunicode('emso_plesalca')
    repo.izbrisi_gen(Plesalec, emso_plesalca, id_col='emso')
    redirect(url('plesalci', id = 'vsi_plesalci', odziv = 'Uspešno izbrisan plesalec!'))

@post('/dodaj_uporabnika/')
@rola_required
def dodaj_uporabnika():
    uporabnisko_ime = request.forms.getunicode('uporabnisko_ime')
    geslo = request.forms.getunicode('geslo')
    funkcija = True if request.forms.getunicode('funkcija') == 'True' else False
    emso_plesalca = request.forms.getunicode('id_plesalca')
    obstojeca_imena = eval(request.forms.get('obstojeca_imena'))
    if uporabnisko_ime in obstojeca_imena:
        redirect(url('plesalci', id = emso_plesalca, napaka = 'Uporabniško ime že obstaja!'))
    else:
        auth.dodaj_uporabnika(uporabnisko_ime, funkcija, geslo, emso_plesalca)
        redirect(url('plesalci', id = emso_plesalca))

@post('/spremeni_geslo_uporabnika/')
@rola_required
def spremeni_geslo_uporabnika():
    uporabnik = request.forms.get('uporabnik')
    uporabnik_tabela = repo.dobi_gen_id(Uporabnik, (uporabnik,), id_cols=("uporabniskoime",))
    novo_geslo = request.forms.get('geslo')
    kodirano_geslo = auth.kodiraj_geslo(novo_geslo)
    uporabnik_tabela.kodiranogeslo = kodirano_geslo
    repo.posodobi_gen(uporabnik_tabela, id_cols=("uporabniskoime",))
    redirect(url('plesalci', id = uporabnik_tabela.emso, potrdilo = 'Uspešno posodobljeno geslo!'))

@post('/spremeni_funkcijo_uporabnika/')
@rola_required
def spremeni_funkcijo_uporabnika():
    uporabnik = request.forms.get('uporabnik')
    uporabnik_tabela = repo.dobi_gen_id(Uporabnik, (uporabnik,), id_cols=("uporabniskoime",))
    nova_funkcija = request.forms.get('funkcija')
    uporabnik_tabela.rola = bool(int(nova_funkcija))
    repo.posodobi_gen(uporabnik_tabela, id_cols=("uporabniskoime",))
    redirect(url('plesalci', id = uporabnik_tabela.emso, potrdilo = 'Uspešno posodobljena funkcija!'))

@post('/odstrani_uporabnika/')
@rola_required
def odstrani_uporabnika():
    uporabnik = request.forms.getunicode('uporabnik')
    uporabnik_tabela = repo.dobi_gen_id(Uporabnik, (uporabnik,), id_cols=("uporabniskoime",))
    repo.izbrisi_gen(Uporabnik, uporabnik, id_col='uporabniskoime')
    redirect(url('plesalci', id = uporabnik_tabela.emso))

@post('/posodobi_mere/')
@rola_required
def posodobi_mere():
    emso_plesalca = request.forms.getunicode('id_plesalca')
    plesalec = repo.dobi_gen_id(Plesalec, (emso_plesalca,), id_cols=("emso",))

    sirina_ramen = pretvori_v_decimal(request.forms.get('sirinaramen'))
    obseg_prsi = pretvori_v_decimal(request.forms.get('obsegprsi'))
    dolzina_rokava = pretvori_v_decimal(request.forms.get('dolzinarokava'))
    dolzina_od_pasu_navzdol = pretvori_v_decimal(request.forms.get('dolzinaodpasunavzdol'))
    dolzina_telesa = pretvori_v_decimal(request.forms.get('dolzinatelesa'))
    stevilka_noge = pretvori_v_decimal(request.forms.get('stevilkanoge'))

    plesalec.sirinaramen = sirina_ramen
    plesalec.obsegprsi =obseg_prsi
    plesalec.dolzinarokava = dolzina_rokava
    plesalec.dolzinaodpasunavzdol = dolzina_od_pasu_navzdol
    plesalec.dolzinatelesa = dolzina_telesa
    plesalec.stevilkanoge = stevilka_noge

    repo.posodobi_gen(plesalec, id_cols=("emso",))
    redirect(url('plesalci', id = emso_plesalca, potrdilo_mere = 'Uspešno posodobljene mere!'))

@get('/delo/')
@cookie_required
def delo():
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    rola = bottle.request.get_cookie('rola')
    potrdilo = bottle.request.query.getunicode('potrdilo')
    plesalci = repo.plesalci()
    emso = [emso for emso, plesalec in plesalci.items() if plesalec.uporabniskoime == uporabnisko_ime][0]
    seznam_plesalcev = [f'{plesalci[emso].ime} {plesalci[emso].priimek}: {emso}' for emso in plesalci.keys()]
    return template('dodajanje_dela.html', uporabnisko_ime = uporabnisko_ime, rola = rola, seznam_plesalcev = seznam_plesalcev, potrdilo = potrdilo, emso = emso)

@post('/dodaj_delo/')
@cookie_required
def dodaj_delo():
    vrsta_dela = request.forms.getunicode('vrsta_dela')
    datum_izvajanja = datetime.strptime(request.forms.get('datum_izvajanja'), '%Y-%m-%d').date()
    trajanje = timedelta(minutes = int(request.forms.get('trajanje')))
    ime_plesalca = request.forms.getunicode('plesalec')
    print(ime_plesalca)
    if ':' in ime_plesalca:
        emso_plesalca = ime_plesalca.split(': ')[1]
    else:
        emso_plesalca = ime_plesalca
    delo = Delo(emso_plesalca, vrsta_dela, trajanje, datumizvajanja=datum_izvajanja)
    repo.dodaj_gen(delo, serial_col="iddela")
    redirect(url('delo', potrdilo= 'Uspešno dodano delo!'))

@get('/kostumske_podobe/<kostumska_podoba>/<imeoprave>/')
@cookie_required
def kostumske_podobe(kostumska_podoba, imeoprave):
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    rola = bottle.request.get_cookie("rola")
    uporabnik = repo.profil(uporabnisko_ime)
    podatek = repo.kostumske_podobe(uporabnik)
    slovar_oprave = {}
    slovar_kostumskih_podob = {}
    slovar = {}
    for oprava in podatek:
        podatki_oprave = repo.oprava_kostumske_podobe(oprava.imekostumskepodobe, oprava.imeoprave)
        slovar[(oprava.imekostumskepodobe, oprava.imeoprave)] = podatki_oprave
        posebnosti = oprava.posebnosti.replace(';', ', ;').split(';') if oprava.posebnosti else '/'
        slovar_oprave[(oprava.imekostumskepodobe,oprava.imeoprave)] = (oprava.vrstacevljev, posebnosti)
        if oprava.imekostumskepodobe not in slovar_kostumskih_podob.keys():
            slovar_kostumskih_podob[oprava.imekostumskepodobe] = [oprava.imeoprave]
        else:
            slovar_kostumskih_podob[oprava.imekostumskepodobe].append(oprava.imeoprave)
    return template('kostumske_podobe.html', uporabnisko_ime = uporabnisko_ime, rola = rola, podatek = podatek, seznam = slovar, slovar_kostumskih_podob = slovar_kostumskih_podob, kostumska_podoba = kostumska_podoba, imeoprave = imeoprave, slovar_oprave = slovar_oprave)

@get('/oblacila/<stran>/')
@cookie_required
def oblacila(stran):
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    rola = bottle.request.get_cookie('rola')
    vrste_oblacil = repo.vrste_oblacil()
    if stran == 'vrste_oblacil':
        return template('vse_vrste_oblacil.html', uporabnisko_ime = uporabnisko_ime, rola = rola, vrste_oblacil = vrste_oblacil, napaka = False)
    else:
        ime_vrste = bottle.request.query.getunicode('ime_vrste')
        spol_vrste = bottle.request.query.getunicode('spol_vrste')
        pokrajina_vrste = bottle.request.query.getunicode('pokrajina_vrste')
        vrsta = repo.dobi_gen_id(VrstaOblacila, (ime_vrste, spol_vrste, pokrajina_vrste), ('ime','spol', 'pokrajina'))
        try:
            oblacila = repo.poisci_oblacila((pokrajina_vrste, ime_vrste, spol_vrste))
        except Exception:
            return template('vse_vrste_oblacil.html', uporabnisko_ime = uporabnisko_ime, rola = rola, vrste_oblacil = vrste_oblacil, napaka = 'Oblačil te vrste še ni!')
        return template('konkretna_vrsta.html', uporabnisko_ime = uporabnisko_ime, rola = rola, oblacila = oblacila, vrsta = vrsta)

@get('/dodaj_oblacilo/')
@rola_required
def dodaj_oblacilo():
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    rola = bottle.request.get_cookie("rola")
    vrste_oblacil = repo.vrste_oblacil()
    slovar_imen_tipov = repo.imena_po_tipih()
    seznam_pokrajin = list(set([vrsta.pokrajina for vrsta in vrste_oblacil]))
    seznam_imen = list(set([vrsta.ime for vrsta in vrste_oblacil]))
    slovar_nezazeljenih ={tip: [ime for ime in seznam_imen if ime not in seznam] for tip, seznam in slovar_imen_tipov.items()}
    return template('dodajanje_oblacil.html', uporabnisko_ime = uporabnisko_ime, rola = rola, vrste_oblacil = vrste_oblacil, slovar_imen_tipov = slovar_imen_tipov, pokrajina = seznam_pokrajin, slovar_nezazeljenih = slovar_nezazeljenih)

@post('/dodaj_oblacilo/')
@rola_required
def dodaj_oblacilo():
    tip_oblacila = request.forms.getunicode('tip')

@error(404)
def error_404(error):
    return "Ta stran ne obstaja!"

######################################################################
# Glavni program


# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
