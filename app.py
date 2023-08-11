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
import io
import base64
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

def pretvori_v_bytes(slika):
    try:
        return bytes(slika)
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

@get('/odjava/')
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
    emso_plesalca = request.forms.getunicode('emso')
    repo.izbrisi_gen(Plesalec, (emso_plesalca,), id_cols=('emso',))
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
    repo.izbrisi_gen(Uporabnik, (uporabnik,), id_cols=('uporabniskoime',))
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
    odziv = request.query.getunicode('odziv')
    napaka_get = request.query.getunicode('napaka')
    napaka = napaka_get if napaka_get != "None" else None
    vrste_oblacil = repo.vrste_oblacil()
    seznam_pokrajin = list(set([vrsta.pokrajina for vrsta in vrste_oblacil]))
    seznam_imen = list(set([vrsta.ime for vrsta in vrste_oblacil]))
    tipi_cevljev = repo.tipi_cevljev()
    seznam_tipov_cevljev = [tip.vrsta for tip in tipi_cevljev]
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
    return template('kostumske_podobe.html', uporabnisko_ime = uporabnisko_ime, 
                    rola = rola, odziv = odziv, napaka = napaka, podatek = podatek, 
                    seznam = slovar, slovar_kostumskih_podob = slovar_kostumskih_podob, 
                    kostumska_podoba = kostumska_podoba, imeoprave = imeoprave, slovar_oprave = slovar_oprave, 
                    seznam_imen = seznam_imen, seznam_pokrajin = seznam_pokrajin, seznam_tipov_cevljev = seznam_tipov_cevljev)

@post('/dodaj_kostumsko_podobo/')
@rola_required
def dodaj_kostumsko_podobo():
    kostumska_podoba = request.forms.getunicode('kostumska_podoba')
    ime_oprave = request.forms.getunicode('oprava')
    spol_oprave = request.forms.getunicode('spol_oprave')
    oprava = OpravaKostumskePodobe(kostumska_podoba, ime_oprave, spol_oprave)
    try:
        repo.dodaj_gen(oprava, serial_col=None)
    except:
        redirect(url('kostumske_podobe', kostumska_podoba = 'osnovna', imeoprave = 'stran', odziv = 'Ta oprava kostumske podobe že obstaja.'))
    redirect(url('kostumske_podobe', kostumska_podoba = kostumska_podoba, imeoprave = ime_oprave))

@post('/dodaj_oblacila_k_kostumski_podobi/')
@rola_required
def dodaj_oblacila_k_kostumski_podobi():
    kostumska_podoba = request.forms.getunicode('kostumska_podoba')
    ime_oprave = request.forms.getunicode('oprava')
    moznost = int(request.forms.getunicode('moznost'))
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    povezava = ROpravaVrsta(pokrajina, spol, ime, ime_oprave, kostumska_podoba, moznost)
    try:
        napaka = None
        repo.dodaj_gen(povezava, serial_col=None)
    except:
        napaka = 'Napaka! Dodali ste vrsto oblačila, ki ne obstaja ali je že v tej opravi.'
    
    redirect(url('kostumske_podobe', kostumska_podoba = kostumska_podoba, imeoprave = ime_oprave, napaka = napaka))

@post('/odstrani_povezavo_oblacilo_KP/')
@rola_required
def odstrani_povezavo_oblacilo_KP():
    kostumska_podoba = request.forms.getunicode('kostumska_podoba')
    ime_oprave = request.forms.getunicode('oprava')
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    repo.izbrisi_gen(ROpravaVrsta, (kostumska_podoba, ime_oprave, ime, pokrajina, spol), ('imekostumskepodobe', 'imeoprave', 'imevrste', 'pokrajinavrste', 'spolvrste'))
    redirect(url('kostumske_podobe', kostumska_podoba = kostumska_podoba, imeoprave = ime_oprave))

@post('/spremeni_cevlje_oprave/')
@rola_required
def spremeni_čevlje_oprave():
    kostumska_podoba = request.forms.getunicode('kostumska_podoba')
    ime_oprave = request.forms.getunicode('oprava')
    tip_cevljev_get = request.forms.getunicode('cevlji')
    tip_cevljev = tip_cevljev_get if tip_cevljev_get != '' else None
    oprava = repo.dobi_gen_id(OpravaKostumskePodobe, (kostumska_podoba, ime_oprave), ('imekostumskepodobe', 'imeoprave'))
    oprava.vrstacevljev = tip_cevljev
    repo.posodobi_gen(oprava, id_cols=('imekostumskepodobe', 'imeoprave'))
    redirect(url('kostumske_podobe', kostumska_podoba = kostumska_podoba, imeoprave = ime_oprave))

@post('/dodaj_posebnosti_oprave/')
@rola_required
def dodaj_posebnosti_oprave():
    kostumska_podoba = request.forms.getunicode('kostumska_podoba')
    ime_oprave = request.forms.getunicode('oprava')
    posebnost = request.forms.getunicode('posebnost')
    oprava = repo.dobi_gen_id(OpravaKostumskePodobe, (kostumska_podoba, ime_oprave), ('imekostumskepodobe', 'imeoprave'))
    if oprava.posebnosti == None or oprava.posebnosti == '':
        oprava.posebnosti = f'{posebnost}'
    else:
        oprava.posebnosti = f'{oprava.posebnosti}; {posebnost}'
    repo.posodobi_gen(oprava, id_cols=('imekostumskepodobe', 'imeoprave'))
    redirect(url('kostumske_podobe', kostumska_podoba = kostumska_podoba, imeoprave = ime_oprave))

@post('/odstrani_posebnosti_oprave/')
@rola_required
def odstrani_posebnosti_oprave():
    kostumska_podoba = request.forms.getunicode('kostumska_podoba')
    ime_oprave = request.forms.getunicode('oprava')
    oprava = repo.dobi_gen_id(OpravaKostumskePodobe, (kostumska_podoba, ime_oprave), ('imekostumskepodobe', 'imeoprave'))
    oprava.posebnosti = None
    repo.posodobi_gen(oprava, id_cols=('imekostumskepodobe', 'imeoprave'))
    redirect(url('kostumske_podobe', kostumska_podoba = kostumska_podoba, imeoprave = ime_oprave))


@get('/oblacila/<stran>/')
@cookie_required
def oblacila(stran):
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    rola = bottle.request.get_cookie('rola')
    vrste_oblacil = repo.vrste_oblacil()
    if stran == 'vrste_oblacil':
        odziv = request.query.getunicode('odziv')
        return template('vse_vrste_oblacil.html', uporabnisko_ime = uporabnisko_ime, rola = rola, vrste_oblacil = vrste_oblacil, napaka = False, odziv = odziv)
    else:
        ime_vrste = bottle.request.query.getunicode('ime_vrste')
        spol_vrste = bottle.request.query.getunicode('spol_vrste')
        pokrajina_vrste = bottle.request.query.getunicode('pokrajina_vrste')
        vrsta = repo.dobi_gen_id(VrstaOblacila, (ime_vrste, spol_vrste, pokrajina_vrste), ('ime','spol', 'pokrajina'))
    
        try:
            oblacila = repo.poisci_oblacila((pokrajina_vrste, ime_vrste, spol_vrste))
            if oblacila == []:
                return template('vse_vrste_oblacil.html', uporabnisko_ime = uporabnisko_ime, rola = rola, vrste_oblacil = vrste_oblacil, napaka = 'Oblačil te vrste še/več ni!', odziv = False)    
        except Exception:
            return template('vse_vrste_oblacil.html', uporabnisko_ime = uporabnisko_ime, rola = rola, vrste_oblacil = vrste_oblacil, napaka = 'Neznana napaka!', odziv = False)
        return template('konkretna_vrsta.html', uporabnisko_ime = uporabnisko_ime, rola = rola, oblacila = oblacila, vrsta = vrsta)

@get('/dodaj_oblacilo/')
@rola_required
def dodaj_oblacilo():
    uporabnisko_ime = bottle.request.get_cookie('uporabniskoime')
    rola = bottle.request.get_cookie("rola")
    potrdilo = request.query.getunicode('potrdilo')
    napaka = request.query.getunicode('napaka')
    nova_vrsta_json = request.query.getunicode('nova_vrsta')
    nova_vrsta = json.loads(nova_vrsta_json) if nova_vrsta_json is not None else None
    vrste_oblacil = repo.vrste_oblacil()
    slovar_imen_tipov = repo.imena_po_tipih()
    seznam_pokrajin = list(set([vrsta.pokrajina for vrsta in vrste_oblacil]))
    seznam_imen = list(set([vrsta.ime for vrsta in vrste_oblacil]))
    slovar_nezazeljenih ={tip: [ime for ime in seznam_imen if ime not in seznam] for tip, seznam in slovar_imen_tipov.items()}
    return template('dodajanje_oblacil.html', uporabnisko_ime = uporabnisko_ime, rola = rola, vrste_oblacil = vrste_oblacil, slovar_imen_tipov = slovar_imen_tipov, pokrajina = seznam_pokrajin, slovar_nezazeljenih = slovar_nezazeljenih, napaka = napaka, potrdilo = potrdilo, nova_vrsta = nova_vrsta)

@post('/dodaj_oblacilo/')
@rola_required
def dodaj_oblacilo():
    tip_oblacila = request.forms.getunicode('tip')
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    slika_get = bytes(request.files.get('slika').file.read())
    slika = slika_get if slika_get != b'' else None
    opombe_get = request.forms.getunicode('opombe')
    opombe = opombe_get if opombe_get != '' else None
    nova_vrsta = None
    try:
        repo.dobi_gen_id(VrstaOblacila, (ime, pokrajina, spol), ('ime', 'pokrajina', 'spol'))
    except:
        tip_imena = TipImena(ime, tip_oblacila)
        try:
            repo.dodaj_gen(tip_imena, serial_col=None)
        except:
            pass
        
        vrsta = VrstaOblacila(ime, spol, pokrajina) 
        repo.dodaj_gen(vrsta, serial_col=None)
        nova_vrsta = (True, ime, pokrajina, spol , tip_oblacila)
    
    if tip_oblacila != 'DodatnaOblacila':
        zaporedna_st = int(request.forms.getunicode('zaporedna_st'))
        barva_get = request.forms.getunicode('barva')
        barva = barva_get if barva_get != '' else None
        stanje = bool(int(request.forms.getunicode('stanje')))
        oblacilo = GlavnaOblacila(pokrajina, spol, ime, zaporedna_st, slika, barva, stanje, opombe)
        try:
            repo.dodaj_gen(oblacilo, serial_col=None)
            
        except:
            odziv = f'Glavno oblačilo z ime:{ime}, pokrajina:{pokrajina}, spol:{spol}, zaporedna številka:{zaporedna_st} že obstaja.'
            redirect(url('dodaj_oblacilo', napaka = odziv))

        if tip_oblacila == 'ZgornjiDel':
            sirina_ramen = pretvori_v_decimal(request.forms.getunicode('sirina_ramen'))
            obseg_prsi = pretvori_v_decimal(request.forms.getunicode('obseg_prsi'))
            dolzina_rokava = pretvori_v_decimal(request.forms.getunicode('dolzina_rokava'))
            mere = ZgornjiDel(pokrajina, spol, ime, zaporedna_st, sirina_ramen, obseg_prsi, dolzina_rokava)
            repo.dodaj_gen(mere, serial_col=None)
        elif tip_oblacila == 'SpodnjiDel':
            dolzina_od_pasu_navzdol = pretvori_v_decimal(request.forms.getunicode('dolzina_od_pasu_navzdol'))
            mere = SpodnjiDel(pokrajina, spol, ime, zaporedna_st, dolzina_od_pasu_navzdol)
            repo.dodaj_gen(mere, serial_col=None)
        else:
            dolzina_telesa = pretvori_v_decimal(request.forms.getunicode('dolzina_telesa'))
            mere = EnodelniKos(pokrajina, spol, ime, zaporedna_st, dolzina_telesa)
            repo.dodaj_gen(mere, serial_col=None)
    else:
        kolicina = int(request.forms.getunicode('kolicina'))
        dodatna = DodatnaOblacila(pokrajina, spol, ime, slika, kolicina, opombe)
        try:
            repo.dodaj_gen(dodatna, serial_col=None)
        except:
            odziv = f'Dodatno blačilo z ime:{ime}, pokrajina:{pokrajina}, spol:{spol} že obstaja.'
            redirect(url('dodaj_oblacilo', napaka = odziv))
    redirect(url('dodaj_oblacilo', potrdilo = 'Oblačilo je bilo uspešno dodano.', nova_vrsta = json.dumps(nova_vrsta)))

@post('/dodaj_omaro/')
@rola_required
def dodaj_omaro():
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    omara = int(request.forms.getunicode('omara_vrste'))
    posodobitev = VrstaOblacila(ime, spol, pokrajina, omara)
    repo.posodobi_gen(posodobitev, id_cols=('ime', 'pokrajina', 'spol'))
    redirect(url('dodaj_oblacilo', potrdilo = 'Podatek je bil uspešno posodobljen.'))
    
@post('/spremeni_omaro/')
@rola_required
def spremeni_omaro():
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    omara_get = request.forms.getunicode('omara_vrste')
    omara = int(omara_get) if omara_get != '/' else None
    posodobitev = VrstaOblacila(ime, spol, pokrajina, omara)
    repo.posodobi_gen(posodobitev, id_cols=('ime', 'pokrajina', 'spol'))
    redirect(url('oblacila', stran = 'oblacilo', ime_vrste = ime, pokrajina_vrste = pokrajina, spol_vrste = spol))
    

@post('/posodobi_podatke_glavna_oblacila/')
@   rola_required
def posodobi_podatke_glavna_oblacila():
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    zaporedna_st = int(request.forms.getunicode('zaporedna_st'))
    tip = request.forms.getunicode('tip_vrste')
    stanje = bool(int(request.forms.getunicode('stanje')))
    opombe_get = request.forms.getunicode('opombe')
    opombe = opombe_get if opombe_get != '' else None
    oblacilo = repo.dobi_gen_id(GlavnaOblacila, (ime, pokrajina, spol, zaporedna_st), ('ime', 'pokrajina', 'spol', 'zaporednast'))
    oblacilo.stanje = stanje
    oblacilo.opombe = opombe
    repo.posodobi_gen(oblacilo, id_cols=('ime', 'pokrajina', 'spol', 'zaporednast'))
    if tip == "ZgornjiDel":
        sirina_ramen = pretvori_v_decimal(request.forms.get('sirina_ramen'))
        obseg_prsi = pretvori_v_decimal(request.forms.get('obseg_prsi'))
        dolzina_rokava = pretvori_v_decimal(request.forms.get('dolzina_rokava'))
        mere = ZgornjiDel(pokrajina, spol, ime, zaporedna_st, sirina_ramen, obseg_prsi, dolzina_rokava)
    elif tip == "SpodnjiDel":
        dolzina_od_pasu_navzdol = pretvori_v_decimal(request.forms.get('dolzina_od_pasu_navzdol'))
        mere = SpodnjiDel(pokrajina, spol, ime, zaporedna_st, dolzina_od_pasu_navzdol)
    else:
        dolzina_telesa = pretvori_v_decimal(request.forms.get('dolzina_telesa'))
        mere = EnodelniKos(pokrajina, spol, ime, zaporedna_st, dolzina_telesa)
    
    repo.posodobi_gen(mere, id_cols=('ime', 'pokrajina', 'spol', 'zaporednast'))
    redirect(url('oblacila', stran = 'oblacilo', ime_vrste = ime, pokrajina_vrste = pokrajina, spol_vrste = spol))

@post('/odstrani_glavno_oblacilo/')
@rola_required
def odstrani_glavno_oblacilo():
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    zaporedna_st = int(request.forms.getunicode('zaporedna_st'))
    repo.izbrisi_gen(GlavnaOblacila, (ime, pokrajina, spol, zaporedna_st), id_cols=('ime', 'pokrajina', 'spol', 'zaporednast'))
    redirect(url('oblacila', stran = 'oblacilo', ime_vrste = ime, pokrajina_vrste = pokrajina, spol_vrste = spol))

@post('/spremeni_sliko_glavna/')
@rola_required
def spremeni_sliko_glavna():
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    zaporedna_st = int(request.forms.getunicode('zaporedna_st'))
    slika_get = bytes(request.files.get('slika').file.read())
    slika = slika_get if slika_get != b'' else None
    oblacilo = repo.dobi_gen_id(GlavnaOblacila, (ime, pokrajina, spol, zaporedna_st), id_cols=("ime","pokrajina","spol","zaporednast"))
    oblacilo.slika = slika
    repo.posodobi_gen(oblacilo, id_cols=("ime","pokrajina","spol","zaporednast"))
    redirect(url('oblacila', stran = 'oblacilo', ime_vrste = ime, pokrajina_vrste = pokrajina, spol_vrste = spol))

@post('/posodobi_podatke_dodatna_oblacila/')
@   rola_required
def posodobi_podatke_dodatna_oblacila():
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    kolicina = int(request.forms.getunicode('kolicina'))
    opombe_get = request.forms.getunicode('opombe')
    opombe = opombe_get if opombe_get != '' else None
    oblacilo = repo.dobi_gen_id(DodatnaOblacila, (ime, pokrajina, spol), ('ime', 'pokrajina', 'spol'))
    oblacilo.kolicina = kolicina
    oblacilo.opombe = opombe
    repo.posodobi_gen(oblacilo, id_cols=('ime', 'pokrajina', 'spol'))
    redirect(url('oblacila', stran = 'oblacilo', ime_vrste = ime, pokrajina_vrste = pokrajina, spol_vrste = spol))

@post('/odstrani_dodatno_oblacilo/')
@rola_required
def odstrani_dodatno_oblacilo():
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    repo.izbrisi_gen(DodatnaOblacila, (ime, pokrajina, spol), id_cols=('ime', 'pokrajina', 'spol'))
    redirect(url('oblacila', stran = 'oblacilo', ime_vrste = ime, pokrajina_vrste = pokrajina, spol_vrste = spol))

@post('/spremeni_sliko_dodatna/')
@rola_required
def spremeni_sliko_dodatna():
    ime = request.forms.getunicode('ime_vrste')
    pokrajina = request.forms.getunicode('pokrajina_vrste')
    spol = request.forms.getunicode('spol_vrste')
    slika_get = bytes(request.files.get('slika').file.read())
    slika = slika_get if slika_get != b'' else None
    oblacilo = repo.dobi_gen_id(DodatnaOblacila, (ime, pokrajina, spol), id_cols=("ime","pokrajina","spol"))
    oblacilo.slika = slika
    repo.posodobi_gen(oblacilo, id_cols=("ime","pokrajina","spol"))
    redirect(url('oblacila', stran = 'oblacilo', ime_vrste = ime, pokrajina_vrste = pokrajina, spol_vrste = spol))

@post('/odstrani_vrsto/')
@rola_required
def odstrani_vrsto():
    ime = request.forms.getunicode('ime')
    pokrajina = request.forms.getunicode('pokrajina')
    spol = request.forms.getunicode('spol')
    repo.izbrisi_gen(VrstaOblacila, (ime,pokrajina, spol), id_cols=('ime','pokrajina', 'spol'))
    redirect(url('oblacila', stran = 'vrste_oblacil', odziv = 'Uspešno izbrisana vrsta oblačil!'))


@get('/vsi_cevlji/')
@cookie_required
def vsi_cevlji():
    uporabnisko_ime = request.get_cookie('uporabniskoime')
    rola = request.get_cookie("rola")
    cevlji = repo.vsi_cevlji()
    plesalci = repo.plesalci()
    odziv = request.query.getunicode('odziv')
    return template('vsi_cevlji.html', uporabnisko_ime = uporabnisko_ime, rola = rola, cevlji = cevlji, plesalci = plesalci, odziv = odziv)


@get('/dodajanje_cevljev/')
@rola_required
def dodajanje_cevljev():
    uporabnisko_ime = request.get_cookie('uporabniskoime')
    rola = request.get_cookie("rola")
    plesalci = repo.plesalci()
    vrste_cevljev = repo.tipi_cevljev()
    potrdilo = request.query.getunicode('potrdilo')
    potrdilo1 = request.query.getunicode('potrdilo1')
    napaka = request.query.getunicode('napaka')
    zahteva = request.query.getunicode('zahteva')
    tip = request.query.getunicode('tip')
    return template('dodajanje_cevljev.html', uporabnisko_ime = uporabnisko_ime, rola = rola, seznam_vrst_cevljev = vrste_cevljev, plesalci = plesalci, potrdilo = potrdilo, napaka = napaka, zahteva = zahteva, tip = tip, potrdilo1 = potrdilo1)

@post('/dodaj_cevlje/')
@rola_required
def dodaj_cevlje():
    vrste_cevljev = repo.tipi_cevljev()
    tip = request.forms.getunicode('tip')
    velikost = request.forms.getunicode('velikost')
    zaporednast = request.forms.getunicode('zaporednast')
    emsolastnika = request.forms.getunicode('lastnik')
    lastnik = emsolastnika if emsolastnika != '' else None
    if lastnik is not None:
        try:
            repo.dobi_gen_id(Plesalec, (lastnik,), ('emso',))
        except:
            odziv = f'Plesalec z EMŠO: {lastnik} ne obstaja. Izberite obstoječega plesalca ali pustite polje prazno.'
            redirect(url('dodajanje_cevljev', napaka = odziv))
    
    cevlji = Cevlji(tip, zaporednast, velikost, lastnik)
    seznam_vrst_cevljev = []
    for i in vrste_cevljev: 
        seznam_vrst_cevljev.append(i.vrsta[0])
    if tip not in seznam_vrst_cevljev:
        tip_cevlja = TipCevljev(tip, slika=None)
        repo.dodaj_gen(tip_cevlja, serial_col=None)
        repo.dodaj_gen(cevlji, serial_col=None)
        redirect(url('dodajanje_cevljev', zahteva = 'dodaj sliko', tip = tip))
    else:
        try:
            repo.dodaj_gen(cevlji, serial_col=None)
        except:
            odziv = f'Čevlji vrste {tip}, velikosti {velikost} z zaporedno številko {zaporednast} že obstajajo.'
            redirect(url('dodajanje_cevljev', napaka = odziv)) 
    redirect(url('dodajanje_cevljev', potrdilo= 'Uspešno dodani čevlji!'))

@post('/dodaj_sliko_cevljev/')
@rola_required
def dodaj_sliko_cevljev():
    tip = request.forms.getunicode('tip')
    slika_get = bytes(request.files.get('slika').file.read())
    slika = slika_get if slika_get != b'' else None
    preusmeritev = request.forms.get('preusmeritev')
    if slika:
        posodobitev = TipCevljev(tip, slika)
        repo.posodobi_gen(posodobitev, id_cols=('vrsta',))
        if preusmeritev:
            redirect(url('slika_cevljev', id = tip))
        else:
            redirect(url('dodajanje_cevljev', potrdilo = 'Slika je bila uspešno dodana.'))
    else:
        if preusmeritev:
            redirect(url('slika_cevljev', id = tip))
        else:
            redirect(url('dodajanje_cevljev', potrdilo = 'Uspešno dodani čevlji. Sliko lahko kadarkoli dodate.'))

@post('/odstrani_cevlje/')
@rola_required
def odstrani_cevlje():
    vrsta = request.forms.getunicode('vrsta')
    velikost = int(request.forms.getunicode('velikost'))
    zapst = int(request.forms.getunicode('zapst'))
    repo.izbrisi_gen(Cevlji, (vrsta, zapst, velikost), id_cols=('vrsta', 'zapst', 'velikost'))
    redirect(url('vsi_cevlji'))

@get('/slika_cevljev/<id>/')
@cookie_required
def slika_cevljev(id):
    slike = repo.vrste_cevljev_in_slike()
    uporabnisko_ime = request.get_cookie('uporabniskoime')
    rola = request.get_cookie("rola")
    return template('slika_cevljev.html', slike = slike, uporabnisko_ime = uporabnisko_ime, rola = rola, id = id)

@post('/odstrani_tip_cevljev/')
@rola_required
def odstrani_tip_cevljev():
    vrsta = request.forms.getunicode('vrsta')
    repo.izbrisi_gen(TipCevljev, (vrsta,), ('vrsta',))
    redirect(url('dodajanje_cevljev', potrdilo1 = f'Vrsta čevljev: {vrsta} uspešno izbrisana.'))

@post('/urejanje_lastnika_cevljev/')
@rola_required
def urejanje_lastnika_cevljev():
    vrsta = request.forms.getunicode('vrsta')
    velikost = int(request.forms.getunicode('velikost'))
    zapst = int(request.forms.getunicode('zapst'))
    lastnik_get = request.forms.get('emso')
    emso_lastnika = lastnik_get if lastnik_get != '/' else None
    if emso_lastnika is not None:
        try:
            repo.dobi_gen_id(Plesalec, (emso_lastnika,), ('emso',))
        except:
            odziv = f'Plesalec z EMŠO: {emso_lastnika} ne obstaja. Izberite obstoječega plesalca ali izberite možnost "ni lastnika".'
            redirect(url('vsi_cevlji', odziv = odziv))
    
    cevelj = Cevlji(vrsta, zapst, velikost, emso_lastnika)
    repo. posodobi_gen(cevelj, id_cols=('vrsta', 'velikost', 'zapst'))
    redirect(url('vsi_cevlji'))
    

@error(404)
def error_404(error):
    return "Ta stran ne obstaja!"

######################################################################
# Glavni program


# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)
