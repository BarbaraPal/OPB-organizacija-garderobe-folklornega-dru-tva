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

#@get('/vrste/')
#def odpri_vrsto_oblacila():
#    vrste = repo.vrste()
#    return template('vrste.html', vrste = vrste)
#
#@get('/oblacila/')
#def odpri_oblacila():
#    oblacila = repo.oblacila()
#    return template('oblacila.html', oblacila = oblacila)

#@get('/dodaj_izdelek')
#def dodaj_izdelek():
#    
#    return template('dodaj_izdelek.html', izdelek = CenaIzdelkaDto())
#

######################################################################
# Glavni program


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
    username = request.forms.get('uporabniskoime')
    password = request.forms.get('geslo')

    if not auth.obstaja_uporabnik(username):
        return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja.")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabniskoime", username, path="/")
        response.set_cookie("rola", f'{prijava.rola}', path="/" )
        redirect(url('index'))

    else:
        return template("prijava.html", napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")

@get('/odjava/')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """

    response.delete_cookie("uporabniskoime", path='/')
    response.delete_cookie("rola", path='/')

    redirect(url('index'))

# ?sprememba=True
@get('/profil/')
@cookie_required
def podatki_o_profilu():
    """
    Prikaže podatke o uporabniku in še kaj.
    """
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    uporabnik = repo.profil(uporabnisko_ime)
    cevlji = repo.cevlji_posameznika(uporabnisko_ime)
    delo = repo.delo_posameznika(uporabnisko_ime)
    for d in delo:
        d.skupno_trajanje = f'{d.skupno_trajanje.total_seconds() // 60} minut'
    sprememba = bottle.request.query.get('sprememba')
    return template('profil.html', uporabnisko_ime = uporabnisko_ime, plesalecdto = uporabnik, cevljidto = cevlji, delodto = delo, sprememba = sprememba)
    
@post('/spremeni_geslo/')
@cookie_required
def spremeni_geslo():
    """
    Spremeni geslo trenutnega uporabnika
    """
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    staro_geslo = request.forms.get('staro_geslo')
    novo_geslo = request.forms.get('novo_geslo')
    sprememba = auth.sprememba_gesla(uporabnisko_ime, staro_geslo,novo_geslo)
    redirect(url('podatki_o_profilu', sprememba = sprememba))

@get('/domov/')
@cookie_required
def osnovna_stran():
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    return template('domov.html', uporabnisko_ime = uporabnisko_ime)

@get('/plesalci/<id>/')
@cookie_required
@rola_required
def plesalci(id):
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    plesalci = repo.plesalci()
    seznam_imen = [plesalci[id_plesalca].uporabniskoime for id_plesalca in plesalci.keys() if plesalci[id_plesalca].uporabniskoime is not None]
    if id == 'vsi_plesalci':
        return template('plesalci.html', uporabnisko_ime = uporabnisko_ime, plesalci = plesalci)
    else:
        napaka = bottle.request.query.getunicode('napaka')
        plesalec = plesalci[int(id)]
        return template('podatki_plesalca.html', uporabnisko_ime = uporabnisko_ime, plesalecdto = plesalec, seznam_imen = seznam_imen, napaka = napaka)

@post('/dodaj_uporabnika/')
@cookie_required
@rola_required
def dodaj_uporabnika():
    uporabnisko_ime = request.forms.get('uporabnisko_ime')
    geslo = request.forms.get('geslo')
    funkcija = True if request.forms.get('funkcija') == 'True' else False
    id_plesalca = int(request.forms.get('id_plesalca'))
    obstojeca_imena = eval(request.forms.get('obstojeca_imena'))
    if uporabnisko_ime in obstojeca_imena:
        redirect(url('plesalci', id = id_plesalca, napaka = 'Uporabniško ime že obstaja!'))
    else:
        auth.dodaj_uporabnika(uporabnisko_ime, funkcija, geslo, id_plesalca)
        redirect(url('plesalci', id = id_plesalca))

@post('/spremeni_podatke_uporabnika/<podatek>/')
@rola_required
def spremeni_podatke_uporabnika(podatek):
    pass
#    uporabnik = request.forms.get('uporabnik')
#    uporabnik_tabela = repo.dobi_gen_id(Uporabnik, (uporabnik,), id_cols=("uporabniskoime",))
#    if podatek == 'izbrisi_uporabnika':
#        pass
#    else:
#        sprememba = request.forms.get(podatek)
#        setattr(uporabnik_tabela, podatek, sprememba)
#        #uporabnik_tabela.podatek = sprememba
#        repo.posodobi_gen(uporabnik_tabela, id_cols=("uporabniskoime",))



@get('/kostumske_podobe/<kostumska_podoba>/<imeoprave>/')
@cookie_required
def kostumske_podobe(kostumska_podoba, imeoprave):
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    uporabnik = repo.profil(uporabnisko_ime)
    podatek = repo.kostumske_podobe(uporabnik)
    slovar_oprave = {}
    slovar_kostumskih_podob = {}
    slovar = {}
    for oprava in podatek:
        podatki_oprave = repo.oprava_kostumske_podobe(oprava.imekostumskepodobe, oprava.imeoprave)
        slovar[(oprava.imekostumskepodobe, oprava.imeoprave)] = podatki_oprave
        posebnosti = oprava.posebnosti.replace(';', ', ;').split(';')
        slovar_oprave[(oprava.imekostumskepodobe,oprava.imeoprave)] = (oprava.vrsta_cevljev, posebnosti)
        if oprava.imekostumskepodobe not in slovar_kostumskih_podob.keys():
            slovar_kostumskih_podob[oprava.imekostumskepodobe] = [oprava.imeoprave]
        else:
            slovar_kostumskih_podob[oprava.imekostumskepodobe].append(oprava.imeoprave)
    return template('kostumske_podobe.html', uporabnisko_ime = uporabnisko_ime, podatek = podatek, seznam = slovar, slovar_kostumskih_podob = slovar_kostumskih_podob, kostumska_podoba = kostumska_podoba, imeoprave = imeoprave, slovar_oprave = slovar_oprave)


@error(404)
def error_404(error):
    return "Ta stran ne obstaja!"

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
