# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import numpy as np
from typing import List, TypeVar, Type, Callable, Tuple, Any
from Data.Modeli import *
from pandas import DataFrame
from re import sub
import Data.auth_public as auth
from datetime import date, datetime
from dataclasses_json import dataclass_json


import base64
import dataclasses
# Ustvarimo generično TypeVar spremenljivko. Dovolimo le naše entitene, ki jih imamo tudi v bazi
# kot njene vrednosti. Ko dodamo novo entiteno, jo moramo dodati tudi v to spremenljivko.

T = TypeVar(
    "T",
    TipImena,
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

    
    def dobi_gen_id(self, typ: Type[T], id_tuple: Tuple[str], id_cols: Tuple[str]) -> T:
        """
        Generična metoda, ki vrne dataclass objekt pridobljen iz baze na podlagi njegovega PRIMARY KEY-a.
        """
        tbl_name = typ.__name__
        id_conditions = " AND ".join([f"{col} = %s" for col in id_cols])
        sql_cmd = f"SELECT * FROM {tbl_name} WHERE {id_conditions};"
        try:
            self.cur.execute(sql_cmd, id_tuple)

            d = self.cur.fetchone()

            if d is None:
                raise Exception(f"Vrstica s ključem {id_tuple} ne obstaja v {tbl_name}.")
        
            if 'slika' in d:  # Check if the 'slika' key is present
                slika_memoryview = d['slika']
                if isinstance(slika_memoryview, memoryview):
                    d['slika'] = bytes(slika_memoryview)

            return typ(**d)
        except:
            self.conn.rollback()
            raise Exception('Napaka')


    def posodobi_gen(self, typ: T, id_cols = ("id",), auto_commit=True):
        """
        Generična metoda, ki posodobi objekt v bazi. Predpostavljamo, da je ime pripadajoče tabele
        enako imenu objekta, ter da so atributi objekta direktno vezani na ime stolpcev v tabeli.
        """

        tbl_name = type(typ).__name__
        
        ids = tuple(getattr(typ, id_col, None) for id_col in id_cols)        
        # dobimo vse atribute objekta razen id stolpca
        fields = [c.name for c in dataclasses.fields(typ) if c.name != id_cols]

        # Iz objekta naredimo slovar (deluje za dataclasses_json)
        d = {field: getattr(typ, field) for field in fields}
    
        # Spremenimo "slika" atribut v bytea
        if hasattr(typ, 'slika'):
            d['slika'] = bytes(typ.slika) if typ.slika is not None else typ.slika

        id_conditions = ' AND '.join([f'{id_col} = %s' for id_col in id_cols])
        sql_cmd = f'UPDATE {tbl_name} SET\n' + ',\n'.join([f'{field} = %s' for field in fields]) + f'\nWHERE {id_conditions}'

        # sestavimo seznam parametrov, ki jih potem vstavimo v sql ukaz
        parameters = [d[field] for field in fields]
        parameters.extend(ids)

        # izvedemo sql
        self.cur.execute(sql_cmd, parameters)
        if auto_commit:
            self.conn.commit()
    
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

        try:
            self.cur.execute(sql_cmd)

            if serial_col != None:
                serial_val = self.cur.fetchone()[0]

                # Nastavimo vrednost serial stolpca
                setattr(typ, serial_col, serial_val)
            if auto_commit: self.conn.commit()
        except:
            self.conn.rollback()
            raise Exception('Napaka')
        



        # Dobro se je zavedati, da tukaj sam dataclass dejansko
        # "mutiramo" in ne ustvarimo nove reference. Return tukaj ni niti potreben.

    def izbrisi_gen(self,  typ: Type[T], id_tuple: Tuple[str], id_cols: Tuple[str]):
        """
        Generična metoda, ki izbriše vrstico it določene tabele v bazi na podlagi njegovega idja.
        """
        tbl_name = typ.__name__
        id_conditions = " AND ".join([f"{col} = %s" for col in id_cols])
        sql_cmd = f'Delete  FROM {tbl_name} WHERE {id_conditions};'
        self.cur.execute(sql_cmd, id_tuple)
        self.conn.commit()
    
    def dobi_gen_slike(self, typ: Type[T], id_tuple: Tuple[str], id_cols: Tuple[str]) -> T:
        """
        Generična metoda, ki vrne dataclass objekt pridobljen iz baze na podlagi njegovega PRIMARY KEY-a.
        """
        tbl_name = typ.__name__
        id_conditions = " AND ".join([f"{col} = %s" for col in id_cols])
        sql_cmd = f"SELECT * FROM {tbl_name} WHERE {id_conditions};"
        self.cur.execute(sql_cmd, id_tuple)

        d = self.cur.fetchone()

        if d is None:
            raise Exception(f"Vrstica s ključem {id_tuple} ne obstaja v {tbl_name}.")
        
        if 'slika' in d:  # Check if the 'slika' key is present
            slika_memoryview = d['slika']
            if isinstance(slika_memoryview, memoryview):
                d['slika'] = bytes(slika_memoryview)
        return typ(**d)


    def profil(self, uporabnisko_ime) -> PlesalecDto:
        self.cur.execute(
            """
            SELECT v.emso, v.ime, v.priimek, v.spolplesalca, v.datumprikljucitve, v.sirinaramen, v.obsegprsi, v.dolzinarokava, v.dolzinaodpasunavzdol, v.dolzinatelesa, v.stevilkanoge, g.uporabniskoime, g.rola 
            FROM Uporabnik g 
            LEFT JOIN Plesalec v ON g.emso = v.emso
            WHERE g.uporabniskoime = %s;
            """, (uporabnisko_ime,))

        podatki_uporabnika = self.cur.fetchall()
        emso, ime, priimek, spolplesalca, datumprikljucitve, sirinaramen, obsegprsi, dolzinarokava, dolzinaodpasunavzdol, dolzinatelesa, stevilkanoge, uporabniskoime, rola = podatki_uporabnika[0]
        return PlesalecDto(emso, uporabniskoime, ime, priimek, spolplesalca, datumprikljucitve.strftime("%d.%m.%Y"), sirinaramen, obsegprsi, dolzinarokava, dolzinaodpasunavzdol, dolzinatelesa, stevilkanoge, rola)
    
    def plesalci(self) -> List[PlesalecDto]:
        self.cur.execute(
            """
            SELECT v.emso, v.ime, v.priimek, v.spolplesalca, v.datumprikljucitve, v.sirinaramen, v.obsegprsi, v.dolzinarokava, v.dolzinaodpasunavzdol, v.dolzinatelesa, v.stevilkanoge, g.uporabniskoime, g.rola 
            FROM Uporabnik g 
            RIGHT JOIN Plesalec v ON g.emso = v.emso;
            """)

        plesalci = self.cur.fetchall()
        return { emso: PlesalecDto(emso, uporabniskoime, ime, priimek, spolplesalca, datumprikljucitve.strftime("%d.%m.%Y"), sirinaramen, obsegprsi, dolzinarokava, dolzinaodpasunavzdol, dolzinatelesa, stevilkanoge, rola) for emso, ime, priimek, spolplesalca, datumprikljucitve, sirinaramen, obsegprsi, dolzinarokava, dolzinaodpasunavzdol, dolzinatelesa, stevilkanoge, uporabniskoime, rola in plesalci}
    

    def cevlji_posameznika(self, emso) -> List[CevljiDto]:
        self.cur.execute(
            """
            SELECT p.emso, c.vrsta, c.velikost, c.zapst
            FROM Plesalec p 
            LEFT JOIN Cevlji c ON p.emso = c.emsolastnika
            WHERE p.emso = %s;
            """, (emso,))

        cevlji_plesalca = self.cur.fetchall()
        return [CevljiDto(emso, vrsta, velikost, zapst) for (emso, vrsta, velikost, zapst) in cevlji_plesalca]
    
    def delo_posameznika(self, emso) -> List[DeloDto]:
        trenutni_mesec = datetime.now().month
        self.cur.execute(
            """
            SELECT d.vrstadela, SUM(d.trajanje) AS skupno_trajanje, p.emso
            FROM Delo d
            LEFT JOIN Plesalec p ON p.emso = d.emso
            WHERE EXTRACT('month' FROM datumizvajanja) = %s
            AND p.emso = %s
            GROUP BY d.vrstadela, p.emso;
            """, (trenutni_mesec, emso,))
        
        podatki_o_delu_uporabnika = self.cur.fetchall()
        return [DeloDto(emso, vrstadela, skupno_trajanje) for (vrstadela, skupno_trajanje, emso ) in podatki_o_delu_uporabnika]

    def kostumske_podobe(self, uporabnik):
        if uporabnik.rola == True:
            self.cur.execute(
            """
            SELECT o.imekostumskepodobe, o.imeoprave,  o.spoloprave, t.vrsta, o.posebnosti  
            FROM opravakostumskepodobe o
            LEFT JOIN tipcevljev t ON o.vrstacevljev = t.vrsta 
            """)
        else:
            if uporabnik.spolplesalca == 'Ž':
                oprava = 'M'
            else:
                oprava = 'Ž'
            self.cur.execute(
                """
                SELECT o.imekostumskepodobe, o.imeoprave, o.spoloprave,t.vrsta, o.posebnosti  
                FROM opravakostumskepodobe o
                LEFT JOIN tipcevljev t ON o.vrstacevljev = t.vrsta 
                WHERE spoloprave != %s
                """, (oprava,))
        
        podatki = self.cur.fetchall()
        return [OpravaKostumskePodobeDto(imekostumske_podobe, ime_oprave, spol_oprave, vrsta_cevljev, posebnosti) for (imekostumske_podobe, ime_oprave, spol_oprave, vrsta_cevljev, posebnosti) in podatki]
    
    #def izberi_moznosti(self, ime_tabele):
    #    query = """
    #        SELECT MAX(moznost) AS max_value
    #        FROM {};
    #    """.format(ime_tabele)
    #    self.cur.execute(query)
    #    max_value = self.cur.fetchone()[0]
    #    print(max_value)

    
    def oprava_kostumske_podobe(self, kostumska_podoba, oprava)-> List[OpravaDto]:
        self.cur.execute(
            """
            SELECT v.ime, v.spol, r.moznost, v.pokrajina, v.omara
            FROM ROpravaVrsta r 
            LEFT JOIN VrstaOblacila v ON r.imevrste = v.ime AND r.spolvrste = v.spol AND r.pokrajinavrste = v.pokrajina
            WHERE r.imekostumskepodobe = %s
            AND r.imeoprave = %s;
            """, (kostumska_podoba, oprava,))
        
        oprava = self.cur.fetchall()
        return [OpravaDto(ime, spol, moznost, pokrajina, omara) for (ime, spol, moznost, pokrajina, omara) in oprava]   


    def vrste_oblacil(self) -> List[VrstaOblacilaDto]:
        self.cur.execute(
            """
            SELECT v.ime, v.spol, v.pokrajina, v.omara, t.tip 
            FROM VrstaOblacila v
            LEFT JOIN TipImena t ON t.ime = v.ime; 
            """)

        oblacila = self.cur.fetchall()
        return  [VrstaOblacilaDto(ime, spol, pokrajina, omara, tip) for (ime, spol, pokrajina, omara, tip) in oblacila]


    def poisci_oblacila(self, vrsta_tupple):
        pokrajna, ime, spol = vrsta_tupple
        self.cur.execute(
            """
            SELECT tip FROM TipImena
            WHERE ime = %s
            """,(ime,))

        tabela = self.cur.fetchall()[0][0]

        if tabela == 'ZgornjiDel':
            self.cur.execute(
                """
                SELECT g.zaporednast, g.barva, g.stanje, g.opombe, g.slika, z.sirinaramen, z.obsegprsi, z.dolzinarokava
                FROM GlavnaOblacila g
                LEFT JOIN ZgornjiDel z ON g.ime = z.ime AND g.spol = z.spol AND g.pokrajina = z.pokrajina AND g.zaporednast = z.zaporednast
                WHERE g.ime = %s AND g.pokrajina = %s AND g.spol = %s;
                """, (ime, pokrajna, spol))
            oblacila = self.cur.fetchall()
            return [ZgornjiDelDto(zaporedna_st, barva, stanje, opombe, slika if slika is None else base64.b64encode(slika).decode('utf-8'), sirina_ramen, obseg_prsi, dolzina_rokava) for (zaporedna_st, barva, stanje, opombe, slika, sirina_ramen, obseg_prsi, dolzina_rokava) in oblacila]
        
        elif tabela == 'SpodnjiDel':
            self.cur.execute(
                """
                SELECT g.zaporednast, g.barva, g.stanje, g.opombe, g.slika, s.dolzinaodpasunavzdol
                FROM GlavnaOblacila g
                LEFT JOIN spodnjidel s ON g.ime = s.ime AND g.spol = s.spol AND g.pokrajina = s.pokrajina AND g.zaporednast = s.zaporednast
                WHERE g.ime = %s AND g.pokrajina = %s AND g.spol = %s;
                """, (ime, pokrajna, spol))
            oblacila = self.cur.fetchall()
            return [SpodnjiDelDto(zaporedna_st, barva, stanje, opombe, slika if slika is None else base64.b64encode(slika).decode('utf-8'), dolzina_od_pasu_navzdol) for (zaporedna_st, barva, stanje, opombe, slika, dolzina_od_pasu_navzdol) in oblacila]
        
        elif tabela == 'EnodelniKos':
            self.cur.execute(
                """
                SELECT g.zaporednast, g.barva, g.stanje, g.opombe, g.slika, e.dolzinatelesa
                FROM GlavnaOblacila g
                LEFT JOIN enodelnikos e ON g.ime = e.ime AND g.spol = e.spol AND g.pokrajina = e.pokrajina AND g.zaporednast = e.zaporednast
                WHERE g.ime = %s AND g.pokrajina = %s AND g.spol = %s;
                """, (ime, pokrajna, spol))
            oblacila = self.cur.fetchall()
            return [EnodelniKosDto(zaporedna_st, barva, stanje, opombe,slika if slika is None else base64.b64encode(slika).decode('utf-8'), dolzina_telesa) for (zaporedna_st, barva, stanje, opombe, slika, dolzina_telesa) in oblacila]
        
        elif tabela == 'DodatnaOblacila':
            self.cur.execute(
                """
                SELECT kolicina, opombe, slika FROM dodatnaoblacila
                WHERE ime = %s AND pokrajina = %s AND spol = %s;
                """, (ime, pokrajna, spol))
            oblacila = self.cur.fetchall()
            return [DodatnaOblacilaDto(kolicina, opombe, slika if slika is None else base64.b64encode(slika).decode('utf-8')) for (kolicina, opombe, slika) in oblacila]
        
        else: 
            raise Exception('Napačna tabela!') # se načeloma ne bi smelo zgoditi!
        
    def imena_po_tipih(self):
        self.cur.execute("""
            SELECT tip, array_agg(ime) AS ImeSeznam
            FROM TipImena 
            GROUP BY Tip;
        """)
        imena_po_tipih = self.cur.fetchall()
        return {tip : imena for tip,imena in imena_po_tipih}
    
    def tipi_cevljev(self) -> List[TipiCevljevDto]:
        self.cur.execute(
            """
            SELECT vrsta
            FROM TipCevljev;
            """)

        tipi = self.cur.fetchall()
        return  [TipiCevljevDto(tip) for (tip) in tipi]
    
    def vsi_cevlji(self) -> List[CevljiDto2]:
        self.cur.execute(
            """
            SELECT c.emsolastnika, c.vrsta, c.velikost, c.zapst, p.ime, p.priimek
            FROM Cevlji c
            LEFT JOIN Plesalec p ON p.emso = c.emsolastnika;
            """)

        cevlji = self.cur.fetchall()
        return [CevljiDto2(emsolastnika, vrsta, velikost, zapst, ime, priimek) for (emsolastnika, vrsta, velikost, zapst, ime, priimek) in cevlji]

    def vrste_cevljev_in_slike(self) -> List[SlikeCevljevDto]:
        self.cur.execute(
            """
            SELECT vrsta, slika
            FROM TipCevljev;
            """)

        slike = self.cur.fetchall()
        return [SlikeCevljevDto(vrsta, slika if slika is None else base64.b64encode(slika).decode('utf-8')) for (vrsta, slika) in slike]    
    
