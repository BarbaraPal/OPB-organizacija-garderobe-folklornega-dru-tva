import pandas as pd
from Data.Database import Repo
from Data.Modeli import *
from Data.Services import AuthService 
from typing import Dict
from re import sub
import dataclasses
import numpy as np
import os

# Vse kar delamo z bazo se nahaja v razredu Repo.
repo = Repo()
auth = AuthService(repo)

def uvoz_podatkov(pot):
    excel_dat = pd.ExcelFile(pot)
    zavihki = excel_dat.sheet_names
    dfs = {}
    for zavihek in zavihki:
        df = pd.read_excel(excel_dat, sheet_name=zavihek)
        dfs.update({zavihek: df})
    return dfs

pot_podatkov = "Data\podatki\garderoba.xlsx"

slovar_podatkov = uvoz_podatkov(pot_podatkov)


def poskusaj_dodati_v_bazo(df,tabela_v_bazi):
    try:
        repo.df_to_sql_insert(df,tabela_v_bazi)
        print(f"Tabela {tabela_v_bazi} je uspešno dodana.")
    except:
        print(f"Vrednosti tabele {tabela_v_bazi} so že dodane!")
             
def dodaj_vrsto_oblacil_in_tipe(df):
    df2 = df.drop(['Omara','Pokrajina','Spol'], axis = 1)
    df2 = df2.drop_duplicates(subset='Ime', keep='first')

    df['Omara'] = df['Omara'].astype(int)
    df['Pokrajina'] = df['Pokrajina'].fillna('SLO')
    df = df.drop(['Tip'], axis = 1)
    poskusaj_dodati_v_bazo(df2,'TipImena')
    poskusaj_dodati_v_bazo(df,'VrstaOblacila')
    
#dodaj_vrsto_oblacil_in_tipe(slovar_podatkov['VrstaOblacila'])


def pripravi_dele(df):
    df['Pokrajina'] = df['Pokrajina'].fillna('SLO')
    df.columns = df.columns.str.lower()
    if 'stanje' in df.columns:
        df['stanje'] = df['stanje'].astype(bool)
    return df

def dodajanje_oblacil_v_bazo(df_vse, prvi_seznam, tabela_baza):
    df_glavna_oblacila = df_vse.drop(prvi_seznam, axis=1)
    df2 = df_vse.drop(['slika', 'barva', 'stanje', 'opombe'], axis=1)
    poskusaj_dodati_v_bazo(df_glavna_oblacila,'GlavnaOblacila')
    poskusaj_dodati_v_bazo(df2,tabela_baza)

def dodaj_glavna_oblacila(zgornji, spodnji, enodelni, dodatni):
    
    df_zgornji = pripravi_dele(zgornji)
    df_spodnji = pripravi_dele(spodnji)
    df_enodelni = pripravi_dele(enodelni)
    df_dodatni = pripravi_dele(dodatni)

    dodajanje_oblacil_v_bazo(df_zgornji, ['sirinaramen', 'obsegprsi', 'dolzinarokava'], 'ZgornjiDel')
    dodajanje_oblacil_v_bazo(df_spodnji, ['dolzinaodpasunavzdol'], 'SpodnjiDel')
    dodajanje_oblacil_v_bazo(df_enodelni, ['dolzinatelesa'], 'EnodelniKos')
    poskusaj_dodati_v_bazo(df_dodatni,'DodatnaOblacila')

#dodaj_glavna_oblacila(slovar_podatkov['ZgornjiDel'],slovar_podatkov['SpodnjiDel'],slovar_podatkov['EnodelniKos'],slovar_podatkov['DodatnaOblacila'])

def dodaj_plesalce(df):
    df.columns = df.columns.str.lower()
    df.rename(columns ={'spol':'spolplesalca'}, inplace=True)
    poskusaj_dodati_v_bazo(df,'Plesalec')
#dodaj_plesalce(slovar_podatkov['Plesalec'])

def dobi_plesalce():
    plesalci = repo.dobi_gen_vse(Plesalec)
    list_plesalcev = [vars(item) for item in plesalci]
    df_plesalci = pd.DataFrame(list_plesalcev).filter(['ime', 'priimek', 'emso'], axis = 1)
    return df_plesalci

def dodaj_delo(df):
    df_plesalci = dobi_plesalce()
    df.columns = df.columns.str.lower()
    df_vse = pd.merge(df, df_plesalci, on=['ime', 'priimek']).drop(['ime', 'priimek', 'datumprikljucitve','spol'], axis=1)
    poskusaj_dodati_v_bazo(df_vse,'Delo')

#dodaj_delo(slovar_podatkov['Delo'])

def dodaj_tip_cevljev(df):
    df.columns = df.columns.str.lower()
    poskusaj_dodati_v_bazo(df,'TipCevljev')

#dodaj_tip_cevljev(slovar_podatkov['TipCevljev'])

def dodaj_cevlje(df):
    df.rename(columns ={'TipCevljev':'vrsta'}, inplace=True)
    df.columns = df.columns.str.lower()
    
    df_plesalci = dobi_plesalce()
    df_cevlji_plesalci = pd.merge(df, df_plesalci, on=['ime', 'priimek'], how='left').drop(['ime', 'priimek', 'spol', 'datumprikljucitve'], axis=1)
    df_cevlji_plesalci.rename(columns={'emso': 'emsolastnika'}, inplace=True)

    poskusaj_dodati_v_bazo(df_cevlji_plesalci,'Cevlji')
    
#dodaj_cevlje(slovar_podatkov['Cevlji'])

def dodaj_opravo_kostumske_podobe(df):
    df.rename(columns ={'TipCevljev':'vrsta'}, inplace=True)
    df.columns = df.columns.str.lower()
    
    poskusaj_dodati_v_bazo(df,'OpravaKostumskePodobe')

# dodaj_opravo_kostumske_podobe(slovar_podatkov['OpravaKostumskePodobe'])

def dodaj_relacijo_oprava_vrsta(df):
    df['PokrajinaVrste'] = df['PokrajinaVrste'].fillna('SLO')
    df.columns = df.columns.str.lower()
    poskusaj_dodati_v_bazo(df,'ROpravaVrsta')

#dodaj_relacijo_oprava_vrsta(slovar_podatkov['ROpravaVrsta'])

# primer ročnega dodajanja uporabnikov

#uporabnik1 = auth.dodaj_uporabnika("maja", True, "novogeslo","1111111111111")
#uporabnik2 = auth.dodaj_uporabnika("navaden plesalec", False, "11111111", "1111111111112")
#uporabnik3 = auth.dodaj_uporabnika("garderober2", True, "12345678", "1111111111113")
#uporabnik4 = auth.dodaj_uporabnika("navaden", False, "12345678", "1111111111124")

def uvoz_slik(tabela, id_cols, id, pot):
    slika = open(pot, 'rb').read()
    objekt = repo.dobi_gen_slike(tabela, id, id_cols=id_cols)
    objekt.slika = slika
    repo.posodobi_gen(objekt, id_cols=id_cols)

#uvoz_slik(GlavnaOblacila, ("ime","pokrajina","spol","zaporednast"),('bluza', 'Štajerska', 'Ž', 9), "Data/podatki/slike_stajerska_bluza/modra_rjava_mala_kockasta.jpg")
#uvoz_slik(GlavnaOblacila, ("ime","pokrajina","spol","zaporednast"),('bluza', 'Štajerska', 'Ž', 8), "Data/podatki/slike_stajerska_bluza/rdeca_modre_rozice.jpg")
#uvoz_slik(GlavnaOblacila, ("ime","pokrajina","spol","zaporednast"),('bluza', 'Štajerska', 'Ž', 7), "Data/podatki/slike_stajerska_bluza/bez_rozice.jpg")
#uvoz_slik(GlavnaOblacila, ("ime","pokrajina","spol","zaporednast"),('bluza', 'Štajerska', 'Ž', 5), "Data/podatki/slike_stajerska_bluza/oranzna_s_krizci.jpg")
#uvoz_slik(GlavnaOblacila, ("ime","pokrajina","spol","zaporednast"),('bluza', 'Štajerska', 'Ž', 4), "Data/podatki/slike_stajerska_bluza/rdeca_modre_rozice.jpg")
#uvoz_slik(GlavnaOblacila, ("ime","pokrajina","spol","zaporednast"),('bluza', 'Štajerska', 'Ž', 3), "Data/podatki/slike_stajerska_bluza/modra_bez_kockasta.jpg")
#uvoz_slik(GlavnaOblacila, ("ime","pokrajina","spol","zaporednast"),('bluza', 'Štajerska', 'Ž', 2), "Data/podatki/slike_stajerska_bluza/modra_s_pikicami.jpg")
#uvoz_slik(GlavnaOblacila, ("ime","pokrajina","spol","zaporednast"),('bluza', 'Štajerska', 'Ž', 1), "Data/podatki/slike_stajerska_bluza/modra_rjava_velika_kockasta.jpg")

#uvoz_slik(TipCevljev, ('vrsta',),('škorenjci',), "slike/logom.jpg")
#uvoz_slik(TipCevljev, ('vrsta',),('mežiški nizki čeveljci',), "slike/logom.jpg")


#def dodajanje_slik_v_bazo():
#    oblacila = repo.dobi_gen_vse(GlavnaOblacila)
#    print(oblacila)

#dodajanje_slik_v_bazo()
slovar_plesalcev = {'plesalec1': MerePlesalcaDto(50, 70, 40, 100, 170), 
                    'plesalec2': MerePlesalcaDto(53, 73, 43, 68, 168), 
                    'plesalec3': MerePlesalcaDto(52, 72, 41, 69, 169)}
slovar_oblacil = {('ime1', 'pokrajina1', 'spol1', 'zaporednast1'): MereEnodelniKosDto(170), ('ime2', 'pokrajina2', 'spol2', 'zaporednast2'): MereEnodelniKosDto(170), ('ime3', 'pokrajina3', 'spol3', 'zaporednast3'): MereEnodelniKosDto(172), ('ime4', 'pokrajina4', 'spol4', 'zaporednast4'): MereEnodelniKosDto(174), ('ime5','pokrajina5', 'spol5', 'zaporednast5'): MereEnodelniKosDto(167)}
slovar_oblacil1 = {('ime1', 'pokrajina1', 'spol1', 'zaporednast1'): MereZgornjiDelDto(50, 72, 40), 
                   ('ime2', 'pokrajina2', 'spol2', 'zaporednast2'): MereZgornjiDelDto(53, 72, 42), 
                   ('ime3', 'pokrajina3', 'spol3', 'zaporednast3'): MereZgornjiDelDto(52, 72, 42), 
                   ('ime4', 'pokrajina4', 'spol4', 'zaporednast4'): MereZgornjiDelDto(54, 74, 44), 
                   ('ime5', 'pokrajina5', 'spol5', 'zaporednast5'): MereZgornjiDelDto(54, 73, 43)} 

from itertools import permutations

def find_all_combinations(plesalci, oblacila):
    all_combinations = list(permutations(oblacila, len(plesalci)))
    return all_combinations


def najdi_optimum(slovar_plesalcev, slovar_oblacil, tip_oblacil):
    oblacila = [primary for primary in slovar_oblacil.keys()]
    plesalci = [emso for emso in slovar_plesalcev.keys()]
    combinations = find_all_combinations(plesalci, oblacila)
    minimum = 1000000
    kombinacija = 0

    for i in combinations:
        minimum_primer = 0
        for j in plesalci:
            index = plesalci.index(j)
            oblacilo = i[index]
            if tip_oblacil == 'ZgornjiDel':
                mere_za_plesalca = [slovar_plesalcev[j].sirinaramen, slovar_plesalcev[j].obsegprsi, slovar_plesalcev[j].dolzinarokava]
                mere_oblacila = [slovar_oblacil[oblacilo].sirinaramen, slovar_oblacil[oblacilo].obsegprsi, slovar_oblacil[oblacilo].dolzinarokava]
            elif tip_oblacil == 'SpodnjiDel':
                mere_za_plesalca = [slovar_plesalcev[j].dolzinaodpasunavzdol]
                mere_oblacila = [slovar_oblacil[oblacilo].dolzinaodpasunavzdol]
            else:
                mere_za_plesalca = [slovar_plesalcev[j].dolzinatelesa]
                mere_oblacila = [slovar_oblacil[oblacilo].dolzinatelesa]

            if all(mera_za_plesalca <= mera_oblacila for mera_za_plesalca, mera_oblacila in zip(mere_za_plesalca, mere_oblacila)):
                minimum_primer += sum((mera_za_plesalca - mera_oblacila) ** 2 for mera_za_plesalca, mera_oblacila in zip(mere_za_plesalca, mere_oblacila))
            else:
                minimum_primer = 100000000
                break

        if minimum_primer < minimum:
            minimum = minimum_primer
            kombinacija = i

    return kombinacija, minimum if kombinacija != 0 else False



#najdi_optimum_zgornji_del(slovar_plesalcev, slovar_oblacil1)

slovar_oblacil_repo_zgornji = repo.mere_zgornji_del(ZgornjiDel, [('bluza', 'Štajerska', 'Ž'),('bluza', 'Prekmurje', 'Ž')])
slovar_plesalcev_repo_zgornji = repo.mere_plesalci(ZgornjiDel, ['1111111111111', '1111111111113', '1111111111114', '1111111111115'])
slovar_oblacil_repo_spodnji = repo.mere_spodnji_del(SpodnjiDel, [('krilo', 'Štajerska', 'Ž'),('krilo', 'Prekmurje', 'Ž')] )
slovar_oblacil_repo_enodelni = repo.mere_enodelni_kos(EnodelniKos, [('krilo z životkom', 'Mežica', 'Ž')] )
slovar_plesalcev_repo_spodnji = repo.mere_plesalci(SpodnjiDel, ['1111111111111', '1111111111113', '1111111111114', '1111111111115'])
slovar_plesalcev_repo_enodelni = repo.mere_plesalci(EnodelniKos, ['1111111111111', '1111111111113', '1111111111114', '1111111111115'])


#najdi_optimum(slovar_plesalcev_repo_enodelni, slovar_oblacil_repo_enodelni, 'EnodelniKos')
#najdi_optimum(slovar_plesalcev_repo_spodnji, slovar_oblacil_repo_zgornji, 'ZgornjiDel')
#najdi_optimum(slovar_plesalcev_repo_spodnji, slovar_oblacil_repo_spodnji, 'SpodnjiDel')