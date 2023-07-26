import pandas as pd
from Data.Database import Repo
from Data.Modeli import *
from Data.Services import AuthService 
from typing import Dict
from re import sub
import dataclasses
import numpy as np

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
             
def dodaj_vrsto_oblacil(df):
    df['Omara'] = df['Omara'].astype(int)
    df['Pokrajina'] = df['Pokrajina'].fillna('SLO')
    poskusaj_dodati_v_bazo(df,'VrstaOblacila')

#dodaj_vrsto_oblacil(slovar_podatkov['VrstaOblacila'])

def dobi_vrste():
    vrste = repo.dobi_gen_vse(VrstaOblacila)
    seznam_vrst = [vars(item) for item in vrste]
    df_vrst = pd.DataFrame(seznam_vrst).drop('omara', axis=1)
    return df_vrst

def pripravi_dele(df, vrste):
    df['Pokrajina'] = df['Pokrajina'].fillna('SLO')
    df.columns = df.columns.str.lower()
    df_vse = pd.merge(df, vrste, on=['pokrajina', 'ime', 'spol'])
    df_vse.rename(columns={'id': 'idvrste'}, inplace=True)
    if 'stanje' in df_vse.columns:
        df_vse['stanje'] = df_vse['stanje'].astype(bool)
    df_vse = df_vse.drop(['pokrajina', 'ime', 'spol'], axis=1)
    return df_vse

def dodajanje_oblacil_v_bazo(df_vse, prvi_seznam, tabela_baza):
    df_glavna_oblacila = df_vse.drop(prvi_seznam, axis=1)
    df2 = df_vse.drop(['slika', 'barva', 'stanje', 'opombe'], axis=1)
    poskusaj_dodati_v_bazo(df_glavna_oblacila,'GlavnaOblacila')
    poskusaj_dodati_v_bazo(df2,tabela_baza)

def dodaj_glavna_oblacila(zgornji, spodnji, enodelni, dodatni):
    vrste = dobi_vrste()
    
    df_zgornji = pripravi_dele(zgornji, vrste)
    df_spodnji = pripravi_dele(spodnji, vrste)
    df_enodelni = pripravi_dele(enodelni, vrste)
    df_dodatni = pripravi_dele(dodatni, vrste)

    dodajanje_oblacil_v_bazo(df_zgornji, ['sirinaramen', 'obsegprsi', 'dolzinarokava'], 'ZgornjiDel')
    dodajanje_oblacil_v_bazo(df_spodnji, ['dolzinaodpasunavzdol'], 'SpodnjiDel')
    dodajanje_oblacil_v_bazo(df_enodelni, ['dolzinatelesa'], 'EnodelniKos')
    poskusaj_dodati_v_bazo(df_dodatni,'DodatnaOblacila')

#dodaj_glavna_oblacila(slovar_podatkov['ZgornjiDel'],slovar_podatkov['SpodnjiDel'],slovar_podatkov['EnodelniKos'],slovar_podatkov['DodatnaOblacila'])


def dodaj_plesalce(df):
    df.columns = df.columns.str.lower()
    df.rename(columns ={'spol':'spolplesalca'}, inplace=True)
    df = df.drop(['dodatnafunkcija'], axis = 1)
    poskusaj_dodati_v_bazo(df,'Plesalec')

#dodaj_plesalce(slovar_podatkov['Plesalec'])

def dobi_plesalce():
    plesalci = repo.dobi_gen_vse(Plesalec)
    list_plesalcev = [vars(item) for item in plesalci]
    df_plesalci = pd.DataFrame(list_plesalcev).filter(['ime', 'priimek', 'idplesalca'], axis = 1)
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
    tip = repo.dobi_gen_vse(TipCevljev)
    list_tipov = [vars(item) for item in tip]
    df_tip = pd.DataFrame(list_tipov).drop('slika',axis=1)

    df_cevlji = pd.merge(df_tip,df, left_on='vrsta', right_on='TipCevljev').drop(['vrsta', 'TipCevljev'], axis=1)
    df_cevlji.columns = df_cevlji.columns.str.lower()
    df_plesalci = dobi_plesalce()
   
   
    df_cevlji_plesalci = pd.merge(df_cevlji, df_plesalci, on=['ime', 'priimek'], how='left').drop(['ime', 'priimek', 'spol', 'datumprikljucitve'], axis=1)
    df_cevlji_plesalci.rename(columns={'idplesalca': 'idlastnika'}, inplace=True)

    poskusaj_dodati_v_bazo(df_cevlji_plesalci,'Cevlji')
    
#dodaj_cevlje(slovar_podatkov['Cevlji'])

def dodaj_opravo_kostumske_podobe(df):
    df.columns = df.columns.str.lower()
    tip = repo.dobi_gen_vse(TipCevljev)
    list_tipov = [vars(item) for item in tip]
    df_tip = pd.DataFrame(list_tipov).drop('slika',axis=1)
    df_oprava = pd.merge(df, df_tip, left_on= 'tipcevljev', right_on='vrsta', how='left').drop(['tipcevljev', 'vrsta'], axis=1)
    poskusaj_dodati_v_bazo(df_oprava,'OpravaKostumskePodobe')

#dodaj_opravo_kostumske_podobe(slovar_podatkov['OpravaKostumskePodobe'])

def dodaj_relacijo_oprava_vrsta(df):
    vrste = dobi_vrste()
    df['Pokrajina'] = df['Pokrajina'].fillna('SLO')
    df.columns = df.columns.str.lower()
    df_vse = pd.merge(df, vrste, on=['pokrajina', 'ime', 'spol']).drop(['pokrajina', 'ime', 'spol'], axis=1)
    df_vse.rename(columns={'id': 'idvrsteoblacila'}, inplace=True)
    poskusaj_dodati_v_bazo(df_vse,'ROpravaVrsta')

#dodaj_relacijo_oprava_vrsta(slovar_podatkov['ROpravaVrsta'])

# primer ročnega dodajanja uporabnikov

uporabnik1 = auth.dodaj_uporabnika("maja", True, "maja",101)
uporabnik2 = auth.dodaj_uporabnika("navaden plesalec", False, "12345678", 100)
#
##uporabnik = auth.dodaj_uporabnika("admin", "2", "admin")
#
##uporabnik = auth.dodaj_uporabnika("garderober", "1", "garderober")
#
##uporabniki = repo.dobi_gen_id(Uporabnik, ('maja',), id_cols=("username",))
##print(uporabniki)
#
##uporabnik3 = auth.dodaj_uporabnika("javnost", "1", "javnogeslo")
#
#