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

#import tracemalloc
#tracemalloc.start()

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8083)
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
    path = './slike'
    return static_file(filename, root=path)

@get('/static_style/<filename:path>')
def static_style(filename):
    return static_file(filename, root='static')


@get('/')
def index(): 
    redirect('/domov/')

@get('/domov/')
#@cookie_required
def osnovna_stran():
    plesalci = repo.plesalci()
    return template('domov.html', plesalci=plesalci)

@get('/vrste/')
def odpri_vrsto_oblacila():
    vrste = repo.vrste()
    return template('vrste.html', vrste = vrste)

@get('/oblacila/')
def odpri_oblacila():
    oblacila = repo.oblacila()
    return template('oblacila.html', oblacila = oblacila)

#@get('/dodaj_izdelek')
#def dodaj_izdelek():
#    
#    return template('dodaj_izdelek.html', izdelek = CenaIzdelkaDto())
#

######################################################################
# Glavni program


#@get('/prijava/') 
#def prijava_get():
#    return template("prijava.html")

@post('/prijava/')
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
    print(prijava)
    if prijava:
        response.set_cookie("uporabnik", username, expires=None)
        response.set_cookie("role", prijava.role)
        #plesalci = repo.plesalci()
        #return template('domov.html', plesalci=plesalci)
        redirect(url('index'))

    else:
        return template("prijava.html", napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")

@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """

    response.delete_cookie("uporabnik")
    response.delete_cookie("role")

    return template('prijava.html', napaka=None)




@error(404)
def error_404(error):
    return "Ta stran ne obstaja!"

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
