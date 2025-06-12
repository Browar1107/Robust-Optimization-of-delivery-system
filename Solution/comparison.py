import random
import numpy as np
import json
from distance_matrix import DistanceMatrix
from test import Dane
import pulp
#from best_solution_data import best_solution  #Comment this line for the script to run correctly
from scenarios import Scenarios
import matplotlib.pyplot as plt
from best_solution_data import best_solution  # Importing the best solution from the provided file



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
    return profits

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
    num_scenarios = 20
    scenario_list = []
    for i in range(num_scenarios):
        df = scenarios_manager.generate_scenario(KLIENTOW=100, MIESIAC=30)
        profit_per_farmer = df.groupby("rolnik_idx")["profit"].sum()
        scenario_list.append({"scenario_df": df, "profit_per_farmer": profit_per_farmer})

    koszty_przesylek = {1: 6.36, 2: 5.71, 3: 5.07, 4: 4.44, 5: 0}

    greedy = greedy_set_cover(D, N)
    random_cover = random_valid_cover(D, N)
    set_cover = pulp_set_cover(D, N)
    minmax = best_solution['set']  # Using the best solution from the provided data

    # Evaluate strategies and store individual scenario profits
    greedy_profits = evaluate_strategy(greedy, scenario_list, dane, D, koszty_przesylek)
    random_profits = evaluate_strategy(random_cover, scenario_list, dane, D, koszty_przesylek)
    set_cover_profits = evaluate_strategy(set_cover, scenario_list, dane, D, koszty_przesylek)
    minmax_profits = evaluate_strategy(minmax, scenario_list, dane, D, koszty_przesylek)

    # Calculate average profits
    greedy_avg = np.mean(greedy_profits)
    random_avg = np.mean(random_profits)
    set_cover_avg = np.mean(set_cover_profits)
    minmax_avg = np.mean(minmax_profits)

    print("Comparison of Pickup Point Strategies:")
    print(f"Greedy Set Cover - Points: {len(greedy)}, Avg Profit: {greedy_avg:.2f}")
    print(f"Random Valid Cover - Points: {len(random_cover)}, Avg Profit: {random_avg:.2f}")
    print(f"Minimized Set Cover (Pulp) - Points: {len(set_cover)}, Avg Profit: {set_cover_avg:.2f}")
    print(f"Minimax Regret Solution - Points: {len(minmax)}, Avg Profit: {minmax_avg:.2f}")

    # ---------------------- Visualization 1: Bar chart of average profits ----------------------
    strategies = ['Greedy', 'Random', 'Pulp', 'Minimax']
    avg_profits = [greedy_avg, random_avg, set_cover_avg, minmax_avg]

    plt.figure(figsize=(10, 6))
    plt.bar(strategies, avg_profits, color=['blue', 'orange', 'green', 'red'])
    plt.xlabel("Strategy")
    plt.ylabel("Average Profit")
    plt.title("Comparison of Average Profits Across Strategies")
    plt.ylim(min(avg_profits) * 0.9, max(avg_profits) * 1.1)  # Adjust y-axis limits

    # Add value labels on top of bars
    for i, profit in enumerate(avg_profits):
        plt.text(i, profit + 0.5, f"{profit:.2f}", ha='center')

    plt.tight_layout()
    plt.show()


    # ---------------------- Visualization 2: Line chart of scenario profits ----------------------
    plt.figure(figsize=(12, 6))
    scenario_numbers = range(1, num_scenarios + 1)

    plt.plot(scenario_numbers, greedy_profits, label='Greedy', marker='o')
    plt.plot(scenario_numbers, random_profits, label='Random', marker='o')
    plt.plot(scenario_numbers, set_cover_profits, label='Pulp', marker='o')
    plt.plot(scenario_numbers, minmax_profits, label='Minimax', marker='o')

    plt.xlabel("Scenario Number")
    plt.ylabel("Profit")
    plt.title("Profit for Each Strategy Across Scenarios")
    plt.xticks(np.arange(1, num_scenarios + 1, step=1))  # Show all scenario numbers
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_comparison()