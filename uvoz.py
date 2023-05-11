import pandas as pd
from pandas import DataFrame
from Data.Database import Repo
from Data.Modeli import *
from typing import Dict
from re import sub
import dataclasses


# Vse kar delamo z bazo se nahaja v razredu Repo.
repo = Repo()

def uvoz_podatkov(pot):
    excel_file = pd.ExcelFile(pot)
    sheet_names = excel_file.sheet_names
    dfs = {}
    for sheet_name in sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        dfs.update({sheet_name: df})
    return dfs

pot_podatkov = "Data\podatki\garderoba.xlsx"

slovar_podatkov = uvoz_podatkov(pot_podatkov)

def dodaj_vrsto_oblacil(tabela):
    df_vrsta = tabela.drop('Id', axis=1)
    df_vrsta['Omara'] = df_vrsta['Omara'].astype(int)
    repo.df_to_sql_insert(df_vrsta,'VrstaOblacila')

# dodaj_vrsto_oblacil(slovar_podatkov['VrstaOblacila'])

def dodaj_zgornje_dele(tabela_zgornji, tabela_vrsta):
    df_zgornji = pd.merge(tabela_vrsta,tabela_zgornji, left_on='Id', right_on='IdVrste').drop(['Id','IdVrste'], axis=1)
    df_zgornji.columns = df_zgornji.columns.str.lower()
    vrste_oblacil = repo.dobi_gen_vse(VrstaOblacila)
    list_vrst = [vars(item) for item in vrste_oblacil]
    df_vrst = pd.DataFrame(list_vrst).drop('omara', axis=1)
    df_vse = pd.merge(df_zgornji, df_vrst, on=['pokrajina', 'ime', 'spol'])
    df_vse.rename(columns={'zapst': 'ZaporednaSt', 'id': 'IdVrste'}, inplace=True)
    
    df_vse['stanje'] = df_vse['stanje'].astype(bool)

    df_glavna_oblacila = df_vse.drop(['slika', 'pokrajina', 'ime', 'omara', 'spol', 'sirinaramen', 'obsegprsi', 'dolzinarokava'], axis=1)
    df_glavna_zgornji = df_vse.drop(['slika','pokrajina', 'ime', 'omara', 'spol', 'barva', 'stanje', 'opombe', 'slika'], axis=1)
    repo.df_to_sql_insert(df_glavna_oblacila,'GlavnaOblacila')
    repo.df_to_sql_insert(df_glavna_zgornji,'ZgornjiDel')

# dodaj_zgornje_dele(slovar_podatkov['ZgornjiDel'], slovar_podatkov['VrstaOblacila'])

def dodaj_spodnje_dele(tabela_spodnji, tabela_vrsta):
    df_spodnji = pd.merge(tabela_vrsta,tabela_spodnji, left_on='Id', right_on='IdVrste').drop(['Id','IdVrste'], axis=1)
    df_spodnji.columns = df_spodnji.columns.str.lower()
    vrste_oblacil = repo.dobi_gen_vse(VrstaOblacila)
    list_vrst = [vars(item) for item in vrste_oblacil]
    df_vrst = pd.DataFrame(list_vrst).drop('omara', axis=1)
    df_vse = pd.merge(df_spodnji, df_vrst, on=['pokrajina', 'ime', 'spol'])
    df_vse.rename(columns={'zapst': 'ZaporednaSt', 'id': 'IdVrste'}, inplace=True)
    
    df_vse['stanje'] = df_vse['stanje'].astype(bool)

    df_glavna_oblacila = df_vse.drop(['slika', 'pokrajina', 'ime', 'omara', 'spol' , 'dolzinaodpasunavzdol'], axis=1)
    df_glavna_spodnji = df_vse.drop(['slika','pokrajina', 'ime', 'omara', 'spol', 'barva', 'stanje', 'opombe', 'slika'], axis=1)
    repo.df_to_sql_insert(df_glavna_oblacila,'GlavnaOblacila')
    repo.df_to_sql_insert(df_glavna_spodnji,'SpodnjiDel')
    
#dodaj_spodnje_dele(slovar_podatkov['SpodnjiDel'], slovar_podatkov['VrstaOblacila'])

def dodaj_enodelne_dele(tabela_enodelni, tabela_vrsta):
    df_enodelni = pd.merge(tabela_vrsta,tabela_enodelni, left_on='Id', right_on='IdVrste').drop(['Id','IdVrste'], axis=1)
    df_enodelni.columns = df_enodelni.columns.str.lower()
    vrste_oblacil = repo.dobi_gen_vse(VrstaOblacila)
    list_vrst = [vars(item) for item in vrste_oblacil]
    df_vrst = pd.DataFrame(list_vrst).drop('omara', axis=1)
    df_vse = pd.merge(df_enodelni, df_vrst, on=['pokrajina', 'ime', 'spol'])
    df_vse.rename(columns={'zapst': 'ZaporednaSt', 'id': 'IdVrste'}, inplace=True)
    
    df_vse['stanje'] = df_vse['stanje'].astype(bool)

    df_glavna_oblacila = df_vse.drop(['slika', 'pokrajina', 'ime', 'omara', 'spol', 'dolzinatelesa'], axis=1)
    df_glavna_enodelni = df_vse.drop(['slika','pokrajina', 'ime', 'omara', 'spol', 'barva', 'stanje', 'opombe', 'slika'], axis=1)
    repo.df_to_sql_insert(df_glavna_oblacila,'GlavnaOblacila')
    repo.df_to_sql_insert(df_glavna_enodelni,'EnodelniKos')
    

#dodaj_enodelne_dele(slovar_podatkov['EnodelniKos'], slovar_podatkov['VrstaOblacila'])

def dodaj_dodatna_oblacila(tabela_dodatni, tabela_vrsta):
    df_dodatni = pd.merge(tabela_vrsta,tabela_dodatni, left_on='Id', right_on='IdVrste').drop(['Id','IdVrste'], axis=1)
    df_dodatni.columns = df_dodatni.columns.str.lower()
    vrste_oblacil = repo.dobi_gen_vse(VrstaOblacila)
    list_vrst = [vars(item) for item in vrste_oblacil]
    df_vrst = pd.DataFrame(list_vrst).drop('omara', axis=1)
    df_vse = pd.merge(df_dodatni, df_vrst, on=['pokrajina', 'ime', 'spol'])
    df_vse.rename(columns={'id': 'IdVrste'}, inplace=True)
    
    df_dodatna_oblacila = df_vse.drop(['pokrajina', 'ime', 'omara', 'spol', 'slika'], axis=1)
    repo.df_to_sql_insert(df_dodatna_oblacila,'DodatnaOblacila')

#dodaj_dodatna_oblacila(slovar_podatkov['DodatnaOblacila'], slovar_podatkov['VrstaOblacila'])

def dodaj_plesalec(tabela):
    df_vrsta = tabela.drop('IdPlesalca', axis=1)
    df_plesalec = df_vrsta.drop(['SirinaRamen', 'ObsegPrsi', 'DolzinaRokava', 'DolzinaOdPasuNavzdol', 'DolzinaTelesa', 'StevilkaNoge'], axis = 1)
    df_plesalec.columns = df_plesalec.columns.str.lower()
    df_plesalec.rename(columns ={'spol':'spolplesalca'}, inplace=True)
    df_plesalec['dodatnafunkcija'] = df_plesalec['dodatnafunkcija'].astype(str)

    repo.df_to_sql_insert(df_plesalec,'Plesalec')

#dodaj_plesalec(slovar_podatkov['Plesalec'])


def dodaj_velikost(tabela):
    df_velikosti = tabela.drop('IdPlesalca', axis=1)
    df_velikosti.columns = df_velikosti.columns.str.lower()
    df_velikosti.rename(columns ={'spol':'spolplesalca'}, inplace=True)

    plesalci = repo.dobi_gen_vse(Plesalec)
    list_plesalcev = [vars(item) for item in plesalci]
    df_plesalci = pd.DataFrame(list_plesalcev)
    df_vse = pd.merge(df_velikosti, df_plesalci, on=['ime', 'priimek', 'spolplesalca'])
    df_vse = df_vse.drop(['ime', 'priimek', 'spolplesalca', 'datumprikljucitve_x','dodatnafunkcija_x', 'datumprikljucitve_y', 'dodatnafunkcija_y'],axis = 1)
    repo.df_to_sql_insert(df_vse,'Velikost')

#dodaj_velikost(slovar_podatkov['Plesalec'])    

def dodaj_delo(tabela_delo):
    
    plesalci = repo.dobi_gen_vse(Plesalec)
    list_plesalcev = [vars(item) for item in plesalci]
    df_plesalci = pd.DataFrame(list_plesalcev).drop(['spolplesalca', 'datumprikljucitve','dodatnafunkcija'], axis = 1)
    df_delo = tabela_delo
    df_delo.columns = df_delo.columns.str.lower()
    df_vse = pd.merge(df_delo, df_plesalci, on=['ime', 'priimek']).drop(['ime', 'priimek'], axis=1)
    repo.df_to_sql_insert(df_vse,'Delo')

#dodaj_delo(slovar_podatkov['Delo'])

def dodaj_tip_cevljev(tabela):
    df_tip = tabela.drop(['Id', 'Slika'], axis=1)
    df_tip.columns = df_tip.columns.str.lower()
    repo.df_to_sql_insert(df_tip,'TipCevljev')

#dodaj_tip_cevljev(slovar_podatkov['TipCevljev'])

def dodaj_cevlje(tabela_cevljev, tabela_plesalcev):
    tip = repo.dobi_gen_vse(TipCevljev)
    list_tipov = [vars(item) for item in tip]
    df_tip = pd.DataFrame(list_tipov).drop('slika',axis=1)
    
    plesalci = repo.dobi_gen_vse(Plesalec)
    list_plesalcev = [vars(item) for item in plesalci]
    df_plesalci = pd.DataFrame(list_plesalcev).drop(['spolplesalca', 'datumprikljucitve','dodatnafunkcija'], axis = 1)
    
    df_cevlji = pd.merge(df_tip,tabela_cevljev, left_on='vrsta', right_on='TipCevljev').drop(['vrsta', 'TipCevljev'], axis=1)
    df_cevlji.columns = df_cevlji.columns.str.lower()
    
    tabela_plesalcev = tabela_plesalcev[['IdPlesalca', 'Ime', 'Priimek']]
    df_cevlji_plesalci = pd.merge(df_cevlji, tabela_plesalcev, left_on='idlastnika', right_on='IdPlesalca', how='left').drop(['idlastnika', 'IdPlesalca'], axis=1)
    df_cevlji_plesalci.columns = df_cevlji_plesalci.columns.str.lower()
    df_vse = pd.merge(df_cevlji_plesalci, df_plesalci, on=['ime', 'priimek'], how='left').drop(['ime', 'priimek'], axis=1)
    df_vse.rename(columns={'idplesalca': 'idlastnika'}, inplace=True)

    cevlji_z_lastnikom = df_vse[df_vse['idlastnika'].notna()]
    cevlji_brez_lastnika = df_vse[df_vse['idlastnika'].isna()].drop('idlastnika', axis=1)

    repo.df_to_sql_insert(cevlji_z_lastnikom,'Cevlji')
    repo.df_to_sql_insert(cevlji_brez_lastnika,'Cevlji')

#dodaj_cevlje(slovar_podatkov['Cevlji'], slovar_podatkov['Plesalec'])

def dodaj_opravo_kostumske_podobe(tabela):
       tabela.columns = tabela.columns.str.lower()
       tabela.rename(columns={'zapst': 'ZaporednaSt', 'spoloprave': 'spol'}, inplace=True)
       try:
           repo.df_to_sql_insert(tabela,'OpravaKostumskePodobe')
           print('Uspešno dodano!')
       finally:
           print('Vrednosti so že dodane!')


#dodaj_opravo_kostumske_podobe(slovar_podatkov['OpravaKostumskePodobe'])