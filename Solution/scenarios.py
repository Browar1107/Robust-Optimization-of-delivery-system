import random
import pandas as pd
from test import Dane

class Scenarios:
    def __init__(self, dane):
        self.dane = dane
        self.scenarios = []

    def generate_scenario(self, KLIENTOW=100, MIESIAC=30, min_orders=1, max_orders=4):
        """
        Generate a scenario: a DataFrame of orders with randomly assigned day, farmer, profit.
        """
        zamowienia = []

        for klient_id in range(KLIENTOW):
            liczba_zamowien = random.randint(min_orders, max_orders)
            dni = random.sample(range(1, MIESIAC + 1), liczba_zamowien)
            for dzien in dni:
                # Select a random farmer
                rolnik_idx = random.randint(0, len(self.dane.rolnicy) - 1)
                od_kogo = 'rolnik'  # or 'paczko' later, when managed
                profit = random.uniform(5, 15)
                zamowienie = {
                    'klient_id': klient_id,
                    'dzien': dzien,
                    'rolnik_idx': rolnik_idx,
                    'od_kogo': od_kogo,
                    'profit': profit
                }
                zamowienia.append(zamowienie)

        df = pd.DataFrame(zamowienia)
        self.scenarios.append(df)
        return df

    def get_scenario(self, index):
        if index < 0 or index >= len(self.scenarios):
            raise IndexError("Scenario index out of range.")
        return self.scenarios[index]


# Example usage:
if __name__ == "__main__":
    dane = Dane()
    dane.wczytaj_z_pliku("dane.txt")
    dane.konwertuj_wszystkich_na_km()

    scenarios_manager = Scenarios(dane)
    scenario_df = scenarios_manager.generate_scenario(KLIENTOW=100, MIESIAC=30)
    print(scenario_df)

    print("\nScenario summary:")
    print(f"Total orders: {len(scenario_df)}")
    print(f"Unique clients: {scenario_df['klient_id'].nunique()}")
    # print(f"Order distribution per client:\n{scenario_df['klient_id'].value_counts()}")
    print(f"Average profit per order: {scenario_df['profit'].mean():.2f}")
    print(f"Total profit: {scenario_df['profit'].sum():.2f}")