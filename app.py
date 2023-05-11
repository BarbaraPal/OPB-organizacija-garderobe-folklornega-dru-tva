#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottleext import get, post, run, request, template, redirect, static_file, url, error, response, template_user

# uvozimo ustrezne podatke za povezavo

from Data.Database import Repo
from Data.Modeli import *

from Data.Services import AuthService
from functools import wraps

import os

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


        cookie = request.get_cookie("uporabnik")
        if cookie:
            return f(*args, **kwargs)

        return template("prijava.html", napaka="Potrebna je prijava!")




    return decorated



@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/')
def index():
    plesalci = repo.plesalci()
    return template('izdelki.html', plesalci=plesalci)



#@get('/dodaj_izdelek')
#def dodaj_izdelek():
#    
#    return template('dodaj_izdelek.html', izdelek = CenaIzdelkaDto())
#

######################################################################
# Glavni program



@post('/prijava')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovi roli.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
        return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)
        response.set_cookie("rola", prijava.role)

        redirect(url('index'))

    else:
        return template("prijava.html", napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")

@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """

    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")

    return template('prijava.html', napaka=None)




@error(404)
def error_404(error):
    return "Ta stran ne obstaja!"

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
