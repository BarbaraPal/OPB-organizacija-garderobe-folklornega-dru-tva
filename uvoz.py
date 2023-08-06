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

def uvoz_slik(kos_oblacila, pot):
    slika = open(pot, 'rb').read()

    oblacilo = repo.dobi_gen_id(GlavnaOblacila, kos_oblacila, id_cols=("ime","pokrajina","spol","zaporednast"))
    oblacilo.slika = bytes(slika)
    repo.posodobi_gen(oblacilo, id_cols=("ime","pokrajina","spol","zaporednast"))

#uvoz_slik(('bluza', 'Štajerska', 'Ž', 9), "Data/podatki/slike_stajerska_bluza/modra_rjava_mala_kockasta.jpg")
#uvoz_slik(('bluza', 'Štajerska', 'Ž', 8), "Data/podatki/slike_stajerska_bluza/rdeca_modre_rozice.jpg")
#uvoz_slik(('bluza', 'Štajerska', 'Ž', 7), "Data/podatki/slike_stajerska_bluza/bez_rozice.jpg")
#uvoz_slik(('bluza', 'Štajerska', 'Ž', 5), "Data/podatki/slike_stajerska_bluza/oranzna_s_krizci.jpg")
#uvoz_slik(('bluza', 'Štajerska', 'Ž', 4), "Data/podatki/slike_stajerska_bluza/rdeca_modre_rozice.jpg")
#uvoz_slik(('bluza', 'Štajerska', 'Ž', 3), "Data/podatki/slike_stajerska_bluza/modra_bez_kockasta.jpg")
#uvoz_slik(('bluza', 'Štajerska', 'Ž', 2), "Data/podatki/slike_stajerska_bluza/modra_s_pikicami.jpg")
#uvoz_slik(('bluza', 'Štajerska', 'Ž', 1), "Data/podatki/slike_stajerska_bluza/modra_rjava_velika_kockasta.jpg")


#def dodajanje_slik_v_bazo():
#    oblacila = repo.dobi_gen_vse(GlavnaOblacila)
#    print(oblacila)

#dodajanje_slik_v_bazo()