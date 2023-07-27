# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import numpy as np
from typing import List, TypeVar, Type, Callable, Tuple, Any
from Data.Modeli import *
from pandas import DataFrame
from re import sub
import Data.auth_public as auth
from datetime import date
from dataclasses_json import dataclass_json

import dataclasses
# Ustvarimo generično TypeVar spremenljivko. Dovolimo le naše entitene, ki jih imamo tudi v bazi
# kot njene vrednosti. Ko dodamo novo entiteno, jo moramo dodati tudi v to spremenljivko.

T = TypeVar(
    "T",
    OpravaKostumskePodobe,
    VrstaOblacila,
    GlavnaOblacila,
    ZgornjiDel,
    SpodnjiDel,
    EnodelniKos,
    DodatnaOblacila,
    Plesalec,
    TipCevljev,
    Cevlji,
    Delo,
    Uporabnik,
    ROpravaVrsta
    )

class Repo:

    def __init__(self):
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=5432)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def camel_case(self, s):
        """
        Pomožna funkcija, ki podan niz spremeni v camel case zapis.
        """
        
        s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
        return ''.join(s) 
    
    def df_to_sql_insert(self, df:DataFrame, name:str, use_camel_case=True):
        """
        Vnese DataFrame v postgresql bazo. Paziti je treba pri velikosti dataframa,
        saj je sql stavek omejen glede na dolžino. Če je dataframe prevelik, ga je potrebno naložit
        po delih (recimo po 100 vrstic naenkrat), ali pa uporabit bulk_insert.
        df: DataFrame, ki ga želimo prenesti v bazo
        name: Ime tabele kamor želimo shranit podatke
        use_camel_case: ali pretovrimo stolpce v camel case zapis
        """
        df = df.replace({np.nan: None})
        cols = list(df.columns)

        # po potrebi pretvorimo imena stolpcev
        if use_camel_case: cols = [self.camel_case(c) for c in cols]

        # ustvarimo sql stavek, ki vnese več vrstic naenkrat
        sql_cmd = f'''INSERT INTO {name} ({',' .join([f'{c}' for c in cols])})
            VALUES 
            {','.join(
                self.cur.mogrify(f'({",".join(["%s"]*len(cols))})', i).decode('utf-8')
                for i in df.itertuples(index=False)
                )}
        '''

        # izvedemo ukaz
        self.cur.execute(sql_cmd)
        self.conn.commit()

    def dobi_gen_vse(self, typ: Type[T], skip=0) -> List[T]:
        """ 
        Generična metoda, ki za podan vhodni dataclass vrne seznam teh objektov iz baze.
        Predpostavljamo, da je tabeli ime natanko tako kot je ime posameznemu dataclassu.
        """
        # ustvarimo sql select stavek, kjer je ime tabele typ.__name__ oz. ime razreda
        tbl_name = typ.__name__
        sql_cmd = f'''SELECT * FROM {tbl_name} OFFSET {skip};'''
        self.cur.execute(sql_cmd)
        return [typ.from_dict(d) for d in self.cur.fetchall()]

    def dobi_gen_id(self, typ: Type[T], id: int | str, id_col = "id") -> T:
        """
        Generična metoda, ki vrne dataclass objekt pridobljen iz baze na podlagi njegovega idja.
        """
        tbl_name = typ.__name__
        sql_cmd = f'SELECT * FROM {tbl_name} WHERE {id_col} = %s';
        self.cur.execute(sql_cmd, (id,))

        d = self.cur.fetchone()

        if d is None:
            raise Exception(f'Vrstica z id-jem {id} ne obstaja v {tbl_name}');
    
        return typ.from_dict(d)
    

    def posodobi_gen(self, typ: T, id_col = "id", auto_commit=True):
        """
        Generična metoda, ki posodobi objekt v bazi. Predpostavljamo, da je ime pripadajoče tabele
        enako imenu objekta, ter da so atributi objekta direktno vezani na ime stolpcev v tabeli.
        """

        tbl_name = type(typ).__name__
        
        id = getattr(typ, id_col)
        # dobimo vse atribute objekta razen id stolpca
        fields = [c.name for c in dataclasses.fields(typ) if c.name != id_col]

        sql_cmd = f'UPDATE {tbl_name} SET \n ' + \
                    ", \n".join([f'{field} = %s' for field in fields]) +\
                    f'\nWHERE {id_col} = %s'
        
        # iz objekta naredimo slovar (deluje samo za dataclasses_json)
        d = typ.to_dict()

        # sestavimo seznam parametrov, ki jih potem vsatvimo v sql ukaz
        parameters = [d[field] for field in fields]
        parameters.append(id)

        # izvedemo sql
        self.cur.execute(sql_cmd, parameters)
        if auto_commit: self.conn.commit()
        
    
    def dodaj_gen(self, typ: T, serial_col="id", auto_commit=True):
        """
        Generična metoda, ki v bazo doda entiteto/objekt. V kolikor imamo definiram serial
        stolpec, objektu to vrednost tudi nastavimo.
        """

        tbl_name = type(typ).__name__

        cols =[c.name for c in dataclasses.fields(typ) if c.name != serial_col]
        

        sql_cmd = f'''
        INSERT INTO {tbl_name} ({", ".join(cols)})
        VALUES
        ({self.cur.mogrify(",".join(['%s']*len(cols)), [getattr(typ, c) for c in cols]).decode('utf-8')})
        '''

        if serial_col != None:
            sql_cmd += f'RETURNING {serial_col}'

        self.cur.execute(sql_cmd)

        if serial_col != None:
            serial_val = self.cur.fetchone()[0]

            # Nastavimo vrednost serial stolpca
            setattr(typ, serial_col, serial_val)

        if auto_commit: self.conn.commit()

        # Dobro se je zavedati, da tukaj sam dataclass dejansko
        # "mutiramo" in ne ustvarimo nove reference. Return tukaj ni niti potreben.

    def profil(self, uporabnisko_ime) -> List[PlesalecDto]:
        self.cur.execute(
            """
            SELECT v.ime, v.priimek, v.spolplesalca, v.datumprikljucitve, v.sirinaramen, v.obsegprsi, v.dolzinarokava, v.dolzinaodpasunavzdol, v.dolzinatelesa, v.stevilkanoge, g.uporabniskoime, g.rola 
            FROM Uporabnik g 
            LEFT JOIN Plesalec v ON g.idplesalca = v.idplesalca
            WHERE g.uporabniskoime = %s;
            """, (uporabnisko_ime,))

        podatki_uporabnika = self.cur.fetchall()
        ime, priimek, spolplesalca, datumprikljucitve, sirinaramen, obsegprsi, dolzinarokava, dolzinaodpasunavzdol, dolzinatelesa, stevilkanoge, uporabniskoime, rola = podatki_uporabnika[0]
        return PlesalecDto(uporabniskoime, ime, priimek, spolplesalca, datumprikljucitve, sirinaramen, obsegprsi, dolzinarokava, dolzinaodpasunavzdol, dolzinatelesa, stevilkanoge, rola)
   
    def cevlji_posameznika(self, uporabnisko_ime) -> List[CevljiDto]:
        self.cur.execute(
            """
            SELECT u.uporabniskoime, t.vrsta, c.velikost, c.zapst
            FROM Uporabnik u 
            LEFT JOIN Plesalec p ON u.idplesalca = p.idplesalca
            LEFT JOIN Cevlji c ON p.idplesalca = c.idlastnika
            LEFT JOIN tipcevljev t ON c.idtipacevljev = t.idtipacevljev
            WHERE u.uporabniskoime = %s;
            """, (uporabnisko_ime,))

        cevlji_plesalca = self.cur.fetchall()
        return [CevljiDto(uporabniskoime, vrsta, velikost, zapst) for (uporabniskoime, vrsta, velikost, zapst) in cevlji_plesalca]
    
    def delo_posameznika(self, uporabnisko_ime) -> List[DeloDto]:
        trenutni_mesec = datetime.now().month
        self.cur.execute(
            """
            SELECT d.vrstadela, SUM(d.trajanje) AS skupno_trajanje, u.uporabniskoime
            FROM Delo d
            LEFT JOIN Uporabnik u ON u.idplesalca = d.idplesalca
            WHERE EXTRACT('month' FROM datumizvajanja) = %s
            AND u.uporabniskoime = %s
            GROUP BY d.vrstadela, u.uporabniskoime;
            """, (trenutni_mesec, uporabnisko_ime,))
        
        podatki_o_delu_uporabnika = self.cur.fetchall()
        return [DeloDto(uporabniskoime, vrstadela, skupno_trajanje) for (vrstadela, skupno_trajanje, uporabniskoime ) in podatki_o_delu_uporabnika]



