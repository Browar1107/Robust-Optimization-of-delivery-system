# import pandas as pd
# import numpy as np
# import random

# class Symulacja:
#     def __init__(self, dane, paczkop, macierz_D, koszty_przesylek):
#         self.dane = dane
#         self.paczkop = paczkop
#         self.macierz_D = macierz_D
#         self.koszty_przesylek = koszty_przesylek
#         self.df_zamowien = pd.DataFrame()
#         self.df_podsumowania = pd.DataFrame()

#     def run(self, KLIENTOW=1000, MIESIAC=30):
#         zamowienia = []

#         # Generujemy zamówienia
#         for klient_id in range(KLIENTOW):
#             dni = random.sample(range(1, MIESIAC+1), 4)
#             for dzien in dni:
#                 rolnik_idx = random.randint(0, len(self.dane.rolnicy)-1)
#                 od_kogo = 'rolnik'
#                 if rolnik_idx in self.paczkop:
#                     od_kogo = 'paczkopunkt'
#                 else:
#                     od_kogo = 'rolnik'
#                 zamowienie = {
#                     'klient_id': klient_id,
#                     'dzien': dzien,
#                     'rolnik_idx': rolnik_idx,
#                     'od_kogo': od_kogo
#                 }
#                 zamowienia.append(zamowienie)
#         self.df_zamowien = pd.DataFrame(zamowienia)

#     def podsumuj_wynik(self, przypisanie):
#         """
#         Podlicza zysk i koszty na podstawie przypisania rolników do paczkopunktów.
#         """
#         # Tworzymy słownik: rolnik -> paczkopunkt (z przypisania)
#         rolnik_do_paczko = {row['rolnik_idx']: row['paczko_idx'] for _, row in przypisanie.iterrows()}

#         # Grupuj zamówienia po paczkopunku i dniu
#         podsumowanie = {}
#         for _, zam in self.df_zamowien.iterrows():
#             j = zam['rolnik_idx']
#             dz = zam['dzien']
#             paczko_idx = rolnik_do_paczko.get(j, None)  # jeśli przypisany
#             # Sprawdzamy od kogo pochodzi zamówienie
#             od_kogo = zam['od_kogo']

#             if od_kogo == 'paczkopunkt':
#                 przychód_zam = 0
#             else:
#                 przychód_zam = 10  # od rolnika, który NIE jest paczkopunkt

#             # Zapisywanie do grupy
#             if paczko_idx is None:
#                 continue  # brak przypisania, pomijamy
#             klucz = (paczko_idx, dz)
#             if klucz not in podsumowanie:
#                 podsumowanie[klucz] = {
#                     'liczba_przesylki': 0,
#                     'koszt': 0,
#                     'przychód': 0
#                 }
#             podsumowanie[klucz]['liczba_przesylki'] += 1
#             # Zapisujemy przychód
#             podsumowanie[klucz]['przychód'] += przychód_zam

#         # Oblicz sumaryczne koszty i zyski
#         suma_kosztow = 0
#         suma_przychodów = 0
#         for (paczko_idx, dz), wartosc in podsumowanie.items():
#             liczba = wartosc['liczba_przesylki']
#             koszt = self.koszty_przesylek.get(liczba, 0)
#             # tutaj można jeszcze uwzględnić ograniczenie 5 przesyłek
#             wartosc['koszt'] = koszt
#             # Zysk od przesyłek od rolnika, który nie był paczkopunktem, to 10 zł za przesyłkę
#             # od rolnika będącego paczkopunktem — 0
#             przychód = wartosc['przychód']
#             suma_kosztow += koszt
#             suma_przychodów += przychód

#         return suma_przychodów, suma_kosztow


import random
import pandas as pd
import numpy as np

class Symulacja:
    def __init__(self, dane, paczkop, macierz_D, koszty_przesylek):
        self.dane = dane
        self.paczkop = paczkop
        self.macierz_D = macierz_D
        self.koszty_przesylek = koszty_przesylek
        self.df_zamowien = pd.DataFrame()
        self.df_podsumowania = pd.DataFrame()

    def run(self, KLIENTOW=1000, MIESIAC=30):
        zamowienia = []

        # Randomize orders and profit
        for klient_id in range(KLIENTOW):
            liczba_zamowien = random.randint(1, 4)  # between 1 and 5
            dni = random.sample(range(1, MIESIAC+1), liczba_zamowien)
            for dzien in dni:
                rolnik_idx = random.randint(0, len(self.dane.rolnicy)-1)
                od_kogo = 'rolnik' if rolnik_idx not in self.paczkop else 'paczkopunkt'
                profit = random.uniform(5, 15)
                zamowienie = {
                    'klient_id': klient_id,
                    'dzien': dzien,
                    'rolnik_idx': rolnik_idx,
                    'od_kogo': od_kogo,
                    'profit': profit
                }
                zamowienia.append(zamowienie)

        self.df_zamowien = pd.DataFrame(zamowienia)
        return len(self.df_zamowien)  # returns total number of generated orders

    def podsumuj_wynik(self, przypisanie):
        """
        Podlicza zysk i koszty na podstawie przypisania rolników do paczkopunktów.
        """
        # Tworzymy słownik: rolnik -> paczkopunkt (z przypisania)
        rolnik_do_paczko = {row['rolnik_idx']: row['paczko_idx'] for _, row in przypisanie.iterrows()}

        # Grupuj zamówienia po paczkopunku i dniu
        podsumowanie = {}
        for _, zam in self.df_zamowien.iterrows():
            j = zam['rolnik_idx']
            dz = zam['dzien']
            paczko_idx = rolnik_do_paczko.get(j, None)  # jeśli przypisany
            # Sprawdzamy od kogo pochodzi zamówienie
            od_kogo = zam['od_kogo']

            if od_kogo == 'paczkopunkt':
                przychód_zam = 0
            else:
                przychód_zam = 10  # od rolnika, który NIE jest paczkopunkt

            # Zapisywanie do grupy
            if paczko_idx is None:
                continue  # brak przypisania, pomijamy
            klucz = (paczko_idx, dz)
            if klucz not in podsumowanie:
                podsumowanie[klucz] = {
                    'liczba_przesylki': 0,
                    'koszt': 0,
                    'przychód': 0
                }
            podsumowanie[klucz]['liczba_przesylki'] += 1
            # Zapisujemy przychód
            podsumowanie[klucz]['przychód'] += przychód_zam

        # Oblicz sumaryczne koszty i zyski
        suma_kosztow = 0
        suma_przychodów = 0
        for (paczko_idx, dz), wartosc in podsumowanie.items():
            liczba = wartosc['liczba_przesylki']
            koszt = self.koszty_przesylek.get(liczba, 0)
            # tutaj można jeszcze uwzględnić ograniczenie 5 przesyłek
            wartosc['koszt'] = koszt
            # Zysk od przesyłek od rolnika, który nie był paczkopunktem, to 10 zł za przesyłkę
            # od rolnika będącego paczkopunktem — 0
            przychód = wartosc['przychód']
            suma_kosztow += koszt
            suma_przychodów += przychód

        return suma_przychodów, suma_kosztow