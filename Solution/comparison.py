



import random
import numpy as np
import json
from distance_matrix import DistanceMatrix
from test import Dane
import pulp
from best_solution_data import best_solution
from scenarios import Scenarios

def greedy_set_cover(D, N, radius=10):
    pokryte = set()
    paczkop = []
    while len(pokryte) < N:
        niepokryci = list(set(range(N)) - pokryte)
        best_j = None
        max_coverage = -1
        for j in niepokryci:
            coverage = sum(1 for i in niepokryci if D[i, j] <= radius)
            if coverage > max_coverage:
                max_coverage = coverage
                best_j = j
        paczkop.append(best_j)
        for i in niepokryci:
            if D[i, best_j] <= radius:
                pokryte.add(i)
    return set(paczkop)

def random_valid_cover(D, N, radius=10):
    all_indices = list(range(N))
    pokryte = set()
    paczkop = []
    attempts = 0
    while len(pokryte) < N and attempts < 1000:
        j = random.choice(all_indices)
        if j in paczkop:
            continue
        paczkop.append(j)
        for i in range(N):
            if D[i, j] <= radius:
                pokryte.add(i)
        attempts += 1
    return set(paczkop)

def pulp_set_cover(D, N, radius=10):
    model = pulp.LpProblem("Set_Cover_Minimize_Pickup_Points", pulp.LpMinimize)
    y = [pulp.LpVariable(f"y_{j}", cat="Binary") for j in range(N)]
    model += pulp.lpSum(y[j] for j in range(N))
    for i in range(N):
        model += pulp.lpSum(y[j] for j in range(N) if D[i][j] <= radius) >= 1
    status = model.solve()
    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError("No optimal solution found")
    return set(j for j in range(N) if pulp.value(y[j]) >= 0.5)

def compute_solution_cost(chosen_farmers, scenario_df, dane, D, koszty_przesylek, dane_inv):
    przypisanie = {}
    for i in range(len(dane.rolnicy)):
        if i not in chosen_farmers:
            d_min = float("inf")
            najblizszy_j = None
            for j in chosen_farmers:
                dist = D[i][j]
                if dist < d_min:
                    d_min = dist
                    najblizszy_j = j
            przypisanie[i] = najblizszy_j

    przypisani_z_rolnika = {dane.rolnicy[j].id: [] for j in chosen_farmers}
    for i, j in przypisanie.items():
        id_rolnika = dane.rolnicy[i].id
        id_punktu = dane.rolnicy[j].id
        przypisani_z_rolnika[id_punktu].append(id_rolnika)

    total_cost = 0
    dny = scenario_df["dzien"].unique()
    for punkt_id, rolnicy_ids in przypisani_z_rolnika.items():
        for d in dny:
            orders = scenario_df[
                (scenario_df["dzien"] == d)
                & (scenario_df["rolnik_idx"].isin([dane_inv[id] for id in rolnicy_ids]))
            ]
            num_orders = len(orders)
            if num_orders > 0:
                cost = 0 if num_orders > 5 else koszty_przesylek.get(num_orders, 0)
                total_cost += cost * num_orders
    return total_cost

def evaluate_strategy(farmer_set, scenarios, dane, D, koszty_przesylek):
    dane_inv = {rolnik.id: idx for idx, rolnik in enumerate(dane.rolnicy)}
    profits = []
    for scenario in scenarios:
        profit_per_farmer = scenario["profit_per_farmer"]
        scenario_df = scenario["scenario_df"]
        chosen_set = farmer_set
        profit_sum = profit_per_farmer[~profit_per_farmer.index.isin(chosen_set)].sum()
        cost = compute_solution_cost(chosen_set, scenario_df, dane, D, koszty_przesylek, dane_inv)
        actual_profit = profit_sum - cost
        profits.append(actual_profit)
    return sum(profits) / len(profits)

def run_comparison():
    dane = Dane()
    dane.wczytaj_z_pliku("Robust-Optimization-of-delivery-system\Solution\dane.txt")
    dane.konwertuj_wszystkich_na_km()
    distances = DistanceMatrix()
    distances.wczytaj_z_pliku("Robust-Optimization-of-delivery-system\Solution\dane.txt")
    distances.konwertuj_wszystkich_na_km()
    D = distances.oblicz_macierz_odleglosci()
    N = len(dane.rolnicy)

    scenarios_manager = Scenarios(dane)
    scenario_list = []
    for i in range(20):
        df = scenarios_manager.generate_scenario(KLIENTOW=100, MIESIAC=30)
        profit_per_farmer = df.groupby("rolnik_idx")["profit"].sum()
        scenario_list.append({"scenario_df": df, "profit_per_farmer": profit_per_farmer})

    koszty_przesylek = {1: 6.36, 2: 5.71, 3: 5.07, 4: 4.44, 5: 0}

    greedy = greedy_set_cover(D, N)
    random_cover = random_valid_cover(D, N)
    set_cover = pulp_set_cover(D, N)
    minmax = best_solution['set']

    print("Comparison of Pickup Point Strategies:")
    print(f"Greedy Set Cover - Points: {len(greedy)}, Avg Profit: {evaluate_strategy(greedy, scenario_list, dane, D, koszty_przesylek):.2f}")
    print(f"Random Valid Cover - Points: {len(random_cover)}, Avg Profit: {evaluate_strategy(random_cover, scenario_list, dane, D, koszty_przesylek):.2f}")
    print(f"Minimized Set Cover (Pulp) - Points: {len(set_cover)}, Avg Profit: {evaluate_strategy(set_cover, scenario_list, dane, D, koszty_przesylek):.2f}")
    print(f"Minimax Regret Solution - Points: {len(minmax)}, Avg Profit: {evaluate_strategy(minmax, scenario_list, dane, D, koszty_przesylek):.2f}")

if __name__ == "__main__":
    run_comparison()
