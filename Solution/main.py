import random
import math

# Stałe
WROCLAW_COORDS = (51.1079, 17.0385)  # przybliżone współrzędne Wrocławia
PROMIEN_ODWIEDZANY = 50

# Funkcja do losowania współrzędnych w promieniu 50 km od Wrocławia
def losuj_lokalizacje(wsp_wroclaw, promien_km):
    # Przybliżone przeliczenie km na stopnie (średnio 111 km na stopień długości i szerokości)
    promien_stopnie = promien_km / 111
    
    # Losowanie odległości i kąta
    odleglosc = random.uniform(0, promien_stopnie)
    kat = random.uniform(0, 2 * math.pi)
    
    # Współrzędne losowego rolnika
    lat = wsp_wroclaw[0] + odleglosc * math.cos(kat)
    lon = wsp_wroclaw[1] + odleglosc * math.sin(kat)
    
    return (lat, lon)

class Klient:
    def __init__(self, id, lokalizacja):
        self.id = id
        self.lokalizacja = lokalizacja
        self.liczba_zamowien_miesiecznie = 4

    def zamowienia_miesiecznie(self):
        return self.liczba_zamowien_miesiecznie

class Rolnik:
    def __init__(self, id, lokalizacja):
        self.id = id
        self.lokalizacja = lokalizacja

class SystemDostaw:
    def __init__(self, liczba_klientow, liczba_rolnikow):
        self.klienci = []
        self.rolnicy = []
        
        # Tworzenie klientów z losową lokalizacją (wokół Wrocławia)
        for i in range(liczba_klientow):
            # Lokalizacja klientów może być wokół Wrocławia, np. w promieniu 10 km
            lokalizacja = losuj_lokalizacje(WROCLAW_COORDS, 10)
            self.klienci.append(Klient(i, lokalizacja))
        
        # Tworzenie rolników z losową lokalizacją w promieniu 50 km od Wrocławia
        for i in range(liczba_rolnikow):
            lokalizacja = losuj_lokalizacje(WROCLAW_COORDS, PROMIEN_ODWIEDZANY)
            self.rolnicy.append(Rolnik(i, lokalizacja))

    def podsumuj(self):
        print(f"Łączna liczba klientów: {len(self.klienci)}")
        print(f"Łączna liczba rolników: {len(self.rolnicy)}")
        # Przykładowe wyświetlenie pierwszych klientów i rolników
        print("Przykładowi klienci:")
        for kl in self.klienci[:5]:
            print(f"Klient {kl.id}: lokalizacja {kl.lokalizacja}")
        print("Przykładowi rolnicy:")
        for ro in self.rolnicy[:5]:
            print(f"Rolnik {ro.id}: lokalizacja {ro.lokalizacja}")

    def zapisz_do_pliku(self, nazwa_pliku):
        with open(nazwa_pliku, 'w') as f:
            f.write("Klienci:\n")
            for kl in self.klienci:
                f.write(f"{kl.id},{kl.lokalizacja[0]},{kl.lokalizacja[1]}\n")
            f.write("Rolnicy:\n")
            for ro in self.rolnicy:
                f.write(f"{ro.id},{ro.lokalizacja[0]},{ro.lokalizacja[1]}\n")
        print(f"Dane zapisane do pliku {nazwa_pliku}")

# Przykład użycia

system = SystemDostaw(liczba_klientow=100, liczba_rolnikow=50)
system.podsumuj()

system.zapisz_do_pliku("dane.txt")


import matplotlib.pyplot as plt

def wizualizacja(system):
    # Pobranie współrzędnych klientów i rolników
    klienci_coords = [klienc.lokalizacja for klienc in system.klienci]
    rolnicy_coords = [rolnik.lokalizacja for rolnik in system.rolnicy]
    
    # Rozdzielenie na współrzędne lat i lon
    klienci_lat, klienci_lon = zip(*klienci_coords)
    rolnicy_lat, rolnicy_lon = zip(*rolnicy_coords)
    
    plt.figure(figsize=(10, 8))
    
    # Rysowanie klientów (np. niebieskie kropki)
    plt.scatter(klienci_lon, klienci_lat, c='blue', s=10, label='Klienci', alpha=0.6)
    
    # Rysowanie rolników (np. zielone kropki)
    plt.scatter(rolnicy_lon, rolnicy_lat, c='green', s=20, label='Rolnicy', alpha=0.8)
    
    # Wyróżnienie Wrocławia
    plt.plot(WROCLAW_COORDS[1], WROCLAW_COORDS[0], 'ro', label='Wrocław')
    plt.text(WROCLAW_COORDS[1], WROCLAW_COORDS[0], 'Wrocław', fontsize=12, color='red')
    
    plt.xlabel('Długość geo (Lon)')
    plt.ylabel('Szerokość geo (Lat)')
    plt.title('Rozmieszczenie klientów i rolników w okolicy Wrocławia')
    plt.legend()
    plt.grid(True)
    plt.show()

# Wizualizacja
wizualizacja(system)

