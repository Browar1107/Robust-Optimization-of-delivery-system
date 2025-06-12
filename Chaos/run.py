from Chaos.test import Dane
from Solution.symulacja import Symulacja

# Wczytanie i konwersja danych
dane = Dane()
dane.wczytaj_z_pliku("dane.txt")
dane.konwertuj_wszystkich_na_km()

# Wybór paczkopunktów na podstawie danych
paczkop = dane.wybierz_paczko_punkty()

# Obliczenie macierzy odległości
macierz_D = dane.oblicz_macierz_odleglosci()

przypisanie = dane.przypisz_do_najblizszego(paczkop)

# Definiujesz koszty przesylek
koszty_przesylek = {1: 6.36, 2: 5.71, 3: 5.07, 4: 4.44, 5: 0}


# Tworzysz i uruchamiasz symulację
sym = Symulacja(dane, paczkop, macierz_D, koszty_przesylek)
liczba_zamowien =sym.run(KLIENTOW=1000)



przychód, koszt = sym.podsumuj_wynik(przypisanie)

zysk = przychód - koszt

print("Random results:")
print(f"Liczba zamówień: {liczba_zamowien}")
print(f"Liczba paczkopunktów: {len(paczkop)}")
print(f"Przychód: {przychód:.2f}, Koszt: {koszt:.2f}")
print(f"Zysk: {zysk:.2f}")


from Chaos.greedy import Greedy

# Wczytanie i konwersja danych
dane = Greedy()
dane.wczytaj_z_pliku("dane.txt")
dane.konwertuj_wszystkich_na_km()


# Wybór paczkopunktów na podstawie danych
paczkop = dane.wybierz_paczko_punkty()

# Obliczenie macierzy odległości
macierz_D = dane.oblicz_macierz_odleglosci()

przypisanie = dane.przypisz_do_najblizszego(paczkop)

# Definiujesz koszty przesylek
koszty_przesylek = {1: 6.36, 2: 5.71, 3: 5.07, 4: 4.44, 5: 0}

# Tworzysz i uruchamiasz symulację
sym = Symulacja(dane, paczkop, macierz_D, koszty_przesylek)
liczba_zamowien =sym.run(KLIENTOW=1000)



przychód, koszt = sym.podsumuj_wynik(przypisanie)

zysk = przychód - koszt

print("Greedy results:")
print(f"Liczba zamówień: {liczba_zamowien}")
print(f"Liczba paczkopunktów: {len(paczkop)}")
print(f"Przychód: {przychód:.2f}, Koszt: {koszt:.2f}")
print(f"Zysk: {zysk:.2f}")


from Solution.distance_matrix import SetCover

# Wczytanie i konwersja danych
dane = SetCover()
dane.wczytaj_z_pliku("dane.txt")
dane.konwertuj_wszystkich_na_km()

# Wybór paczkopunktów na podstawie danych
paczkop = dane.wybierz_paczko_punkty()

# Obliczenie macierzy odległości
macierz_D = dane.oblicz_macierz_odleglosci()

przypisanie = dane.przypisz_do_najblizszego(paczkop)

# Definiujesz koszty przesylek
koszty_przesylek = {1: 6.36, 2: 5.71, 3: 5.07, 4: 4.44, 5: 0}

# Tworzysz i uruchamiasz symulację
sym = Symulacja(dane, paczkop, macierz_D, koszty_przesylek)
liczba_zamowien = sym.run(KLIENTOW=1000)


przychód, koszt = sym.podsumuj_wynik(przypisanie)

zysk = przychód - koszt


print("Set Cover results:")
print(f"Liczba zamówień: {liczba_zamowien}")
print(f"Liczba paczkopunktów: {len(paczkop)}")
print(f"Przychód: {przychód:.2f}, Koszt: {koszt:.2f}")
print(f"Zysk: {zysk:.2f}")


import numpy as np
import pandas as pd


