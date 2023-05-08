import pandas as pd
from pandas import DataFrame
from Database import Repo
from Modeli import *
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
    

dodaj_enodelne_dele(slovar_podatkov['EnodelniKos'], slovar_podatkov['VrstaOblacila'])