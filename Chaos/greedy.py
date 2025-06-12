import numpy as np
import matplotlib.pyplot as plt
import random
from geopy.distance import geodesic
import pandas as pd


class Klient:
    def __init__(self, id, lat, lon):
        self.id = int(id)
        self.lat = float(lat)
        self.lon = float(lon)
        self.x = None
        self.y = None
    
    def konwertuj_na_km(self, wsp_wroclaw_lat=51.1079, wsp_wroclaw_lon=17.0385):
        delta_lat = self.lat - wsp_wroclaw_lat
        delta_lon = self.lon - wsp_wroclaw_lon
        self.y = delta_lat * 111
        self.x = delta_lon * 111 * np.cos(np.radians(wsp_wroclaw_lat))

# Klasa Rolnik
class Rolnik:
    def __init__(self, id, lat, lon):
        self.id = int(id)
        self.lat = float(lat)
        self.lon = float(lon)
        self.x = None
        self.y = None
    
    def konwertuj_na_km(self, wsp_wroclaw_lat=51.1079, wsp_wroclaw_lon=17.0385):
        delta_lat = self.lat - wsp_wroclaw_lat
        delta_lon = self.lon - wsp_wroclaw_lon
        self.y = delta_lat * 111
        self.x = delta_lon * 111 * np.cos(np.radians(wsp_wroclaw_lat))



class Greedy:
    def __init__(self):
        self.klienci = []
        self.rolnicy = []

    def wczytaj_z_pliku(self, nazwa_pliku):
        self.klienci = []
        self.rolnicy = []
        current_section = None
        with open(nazwa_pliku, 'r') as f:
            for line in f:
                line = line.strip()
                if line == "Klienci:":
                    current_section = 'klienci'
                    continue
                elif line == "Rolnicy:":
                    current_section = 'rolnicy'
                    continue
                elif not line:
                    continue
                id_str, x_str, y_str = line.split(",")
                if current_section == 'klienci':
                    self.klienci.append(Klient(id_str, x_str, y_str))
                elif current_section == 'rolnicy':
                    self.rolnicy.append(Rolnik(id_str, x_str, y_str))
                    
    def konwertuj_wszystkich_na_km(self):
        for k in self.klienci:
            k.konwertuj_na_km()
        for r in self.rolnicy:
            r.konwertuj_na_km()

    def oblicz_macierz_odleglosci(self):
        N = len(self.rolnicy)
        D = np.zeros((N, N))
        coords = [(r.x, r.y) for r in self.rolnicy]
        for i in range(N):
            for j in range(N):
                D[i,j] = np.linalg.norm([coords[i][0] - coords[j][0], coords[i][1] - coords[j][1]])
        return D

    def wybierz_paczko_punkty(self):
        N = len(self.rolnicy)
        D = self.oblicz_macierz_odleglosci()

        pokryte = set()
        paczkop = []

        while len(pokryte) < N:
            # Szukamy rolnika spośród jeszcze nie pokrytych, którego odległości do innych niepokrytych
            niepokryci = list(set(range(N)) - pokryte)
            best_j = None
            max_coverage = -1
            for j in niepokryci:
                # Liczymy, ile rolników może pokryć ten paczkopunkt (w odległości ≤10km)
                coverage = sum(1 for i in niepokryci if D[i,j] <= 10)
                if coverage > max_coverage:
                    max_coverage = coverage
                    best_j = j
            # Dodajemy najważniejszego rolnika do paczkopunktów
            paczkop.append(best_j)
            # pokrywamy wszystkich w odległości ≤10 km od niego
            for i in niepokryci:
                if D[i, best_j] <= 10:
                    pokryte.add(i)
        return paczkop
    
    def przypisz_do_najblizszego(self, paczkop):
        D = self.oblicz_macierz_odleglosci()
        przypisania = []
        for i in range(len(self.rolnicy)):
            odleglosci_do_paczko = D[i, paczkop]
            najblizszy_j_idx = np.argmin(odleglosci_do_paczko)
            najblizszy_j = paczkop[najblizszy_j_idx]
            odl = odleglosci_do_paczko[najblizszy_j_idx]
            przypisania.append({'rolnik_idx': i, 'paczko_idx': najblizszy_j, 'odl_km': odl})
        return pd.DataFrame(przypisania)

    def wizualizacja_kw_km(self, paczkop, promien_km=10):
        coords = [(r.x, r.y) for r in self.rolnicy]
        N = len(self.rolnicy)
        D = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                D[i,j] = np.linalg.norm([coords[i][0] - coords[j][0], coords[i][1] - coords[j][1]])

        max_dist = 0
        for j in paczkop:
            max_dist = max(max_dist, np.max(D[:,j]))

        # Wyznacza najdalej od (0,0)
        odleglosci_od_0 = [np.linalg.norm([r.x, r.y]) for r in self.rolnicy]
        max_odl_od_0 = max(odleglosci_od_0)

        limit = max(max_dist, max_odl_od_0) * 0.8  # o 10% więcej

        plt.figure(figsize=(10,8))
        # wszystkie rolnicy
        plt.scatter([r.x for r in self.rolnicy], [r.y for r in self.rolnicy], c='gray', s=20, label='Rolnicy')
        # paczkopunkty
        for j in paczkop:
            plt.scatter(self.rolnicy[j].x, self.rolnicy[j].y, c='red', s=100, marker='^', label='PaczkoPunkt' if 'PaczkoPunkt' not in plt.gca().get_legend_handles_labels()[1] else '')
        # okręgi 10 km
        for j in paczkop:
            center = (self.rolnicy[j].x, self.rolnicy[j].y)
            radius = promien_km
            theta = np.linspace(0, 2*np.pi, 200)
            x_circ = center[0] + radius*np.cos(theta)
            y_circ = center[1] + radius*np.sin(theta)
            plt.plot(x_circ, y_circ, 'r--', alpha=0.5)

        plt.xlim(-limit, limit)
        plt.ylim(-limit, limit)
        plt.xlabel('Odległość od Wrocławia (km)')
        plt.ylabel('Odległość od Wrocławia (km)')
        plt.title('Rozmieszczenie rolników i paczkopunktów w km (środek: Wrocław)')
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    dane = Greedy()
    dane.wczytaj_z_pliku("dane.txt")
    dane.konwertuj_wszystkich_na_km()
    
    # Wybór paczkopunktów
    paczkop = dane.wybierz_paczko_punkty()
    print(f"Wylosowane paczkopunkty: {paczkop}")
    
    
    przypisania = dane.przypisz_do_najblizszego(paczkop)
    print("Przypisania do najbliższego paczkopunktu:")
    print(przypisania)
    

    macierz_D = dane.oblicz_macierz_odleglosci()

    # Wizualizacja
    dane.wizualizacja_kw_km(paczkop, promien_km=10)
    