# import pulp
# from distance_matrix import DistanceMatrix
# from scenarios import Scenarios
# from test import Dane

# # Załaduj dane i oblicz macierze
# distances = DistanceMatrix()
# distances.wczytaj_z_pliku("dane.txt")
# distances.konwertuj_wszystkich_na_km()
# macierz_D = distances.oblicz_macierz_odleglosci()

# dane = Dane()
# dane.wczytaj_z_pliku("dane.txt")
# dane.konwertuj_wszystkich_na_km()

# scenarios_manager = Scenarios(dane)
# scenario_df = scenarios_manager.generate_scenario(KLIENTOW=100, MIESIAC=30)
# print(scenario_df)

# koszty_przesylek = {1: 6.36, 2: 5.71, 3: 5.07, 4: 4.44, 5: 0}

# # Liczba rolników
# n_farmers = len(dane.rolnicy)

# # Oblicz sumę profitów od zamówień każdego rolnika
# profit_per_farmer = scenario_df.groupby('rolnik_idx')['profit'].sum()

# # Tworzymy model maksymalizacji zysku
# model = pulp.LpProblem("Maksymalizacja_zysku", pulp.LpMaximize)

# # Zmienna binarna: czy rolnik jest wybrany jako punkt odbioru
# y = {j: pulp.LpVariable(f'y_{j}', cat='Binary') for j in range(n_farmers)}

# # Funkcja celu: max profit od rolników, którzy nie są punktem odbioru
# model += pulp.lpSum(profit_per_farmer[j] * (1 - y[j]) for j in range(n_farmers))

# # Ograniczenia: każdy rolnik musi być pokryty przez punkt odbioru w odległości ≤ 10 km
# for i in range(n_farmers):
#     model += pulp.lpSum(y[j] for j in range(n_farmers) if macierz_D[i][j] <= 10) >= 1, f'Pokrycie_rolnika_{i}'

# # Rozwiąż model
# status = model.solve()

# # Wypisz status
# print(f"Status rozwiązania: {pulp.LpStatus[model.status]}")

# # Wybrani rolnicy jako punkty odbioru
# wybrani_rolnicy = [j for j in range(n_farmers) if pulp.value(y[j]) == 1]


# print("Rolnicy wybrani jako punkty odbioru (indeksy):", wybrani_rolnicy)

# # Wartość funkcji celu (max zysk)
# print("Wartość funkcji celu (max profit):", pulp.value(model.objective))

# punkt_odbioru = [dane.rolnicy[j].id for j in wybrani_rolnicy]

# # Przypisz każdego rolnika, który nie jest paczkopunktem, do najbliższego punktu
# przypisanie = {}
# for i in range(n_farmers):
#     if i not in wybrani_rolnicy:
#         d_min = float('inf')
#         najblizszy_j = None
#         for j in wybrani_rolnicy:
#             if macierz_D[i][j] < d_min:
#                 d_min = macierz_D[i][j]
#                 najblizszy_j = j
#         przypisanie[i] = najblizszy_j

# # Tworzymy słownik, który grupuje rolników przypisanych do każdego punktu odbioru
# przypisani_z_rolnika = {}

# # najpierw dodaj wszystkie paczkopunkty jako klucze (ID rolnika jako punktu), nawet bez rolników
# for j in wybrani_rolnicy:
#     id_punktu = dane.rolnicy[j].id
#     przypisani_z_rolnika[id_punktu] = []

# # potem dodajesz przypisania dla tych, co mają rolników podległych
# for i, j in przypisanie.items():
#     id_rolnika = dane.rolnicy[i].id
#     id_punktu = dane.rolnicy[j].id
#     # dodaj tylko jeśli już nie istnieje, bo dodaliśmy powyżej, więc nie musisz obsługiwać braku klucza
#     przypisani_z_rolnika[id_punktu].append(id_rolnika)


# print(przypisani_z_rolnika)
# # Wyświetlamy wynik
# print("ID punktów odbioru (rolników wybranych jako paczkopunkty):", punkt_odbioru)

# print("Przypisanie rolników do punktów odbioru:")
# for punkt_id, rolnicy_ids in przypisani_z_rolnika.items():
#     print(f"Punkt odbioru (rolnik ID): {punkt_id} -> Rolnicy ({len(rolnicy_ids)}): {rolnicy_ids}")


# dny = scenario_df['dzien'].unique()


# koszty_przesylek = {1: 6.36, 2: 5.71, 3: 5.07, 4: 4.44, 5: 0}
# # Słownik na koszty: klucz: (rolnik_id, dzien), wartość: koszt
# koszty_w_dniu = {}

# for j in wybrani_rolnicy:
#     podlegli = przypisani_z_rolnika[j]
#     # dodaj rolnika j do listy podległych (jeśli jeszcze nie ma)
#     podlegli_z_j = podlegli + [j]
#     for d in dny:
#         liczba_zamowien = len(scenario_df[
#             (scenario_df['dzien'] == d) &
#             (scenario_df['rolnik_idx'].isin(podlegli_z_j))
#         ])

#         # Dobierz koszt wg. tabeli
#         if liczba_zamowien > 0:
#             if liczba_zamowien > 5:
#                 koszt = 0
#             else:
#                 koszt = koszty_przesylek.get(liczba_zamowien, 0)
#             koszt_calkowity = koszt * liczba_zamowien
#             koszty_w_dniu[(j, d)] = koszt_calkowity

# total_koszt = sum(koszty_w_dniu.values())
# print(f"Całkowity koszt przesyłek (od wszystkich paczkopunktów): {total_koszt:.2f}")

# # Posortowane po dniach
# for (j, d) in sorted(koszty_w_dniu.keys(), key=lambda x: x[1]):
#     koszt = koszty_w_dniu[(j, d)]


#     print(f"Punkt (rolnik ID): {j} — Dzień: {d} — Koszt: {koszt:.2f}")


import pulp
import pandas as pd
from distance_matrix import DistanceMatrix
from scenarios import Scenarios
from test import Dane

distances = DistanceMatrix()
distances.wczytaj_z_pliku("Robust-Optimization-of-delivery-system\Solution\dane.txt")
distances.konwertuj_wszystkich_na_km()
macierz_D = distances.oblicz_macierz_odleglosci()

dane = Dane()
dane.wczytaj_z_pliku("Robust-Optimization-of-delivery-system\Solution\dane.txt")
dane.konwertuj_wszystkich_na_km()

scenarios_manager = Scenarios(dane)

koszty_przesylek = {1: 6.36, 2: 5.71, 3: 5.07, 4: 4.44, 5: 0}


def generate_candidate_solutions(macierz_D, dane, scenarios_manager, NUM_SOLUTIONS=10):
    scenario_df = scenarios_manager.generate_scenario(KLIENTOW=100, MIESIAC=30)
    profit_per_farmer = scenario_df.groupby("rolnik_idx")["profit"].sum()
    farmer_indices = profit_per_farmer.index.tolist()

    solutions = []

    for _ in range(NUM_SOLUTIONS):
        model = pulp.LpProblem("Maksymalizacja_zysku", pulp.LpMaximize)
        y = {j: pulp.LpVariable(f"y_{j}", cat="Binary") for j in farmer_indices}

        model += pulp.lpSum(profit_per_farmer[j] * (1 - y[j]) for j in farmer_indices)

        for i in range(len(farmer_indices)):
            model += (
                pulp.lpSum(y[j] for j in farmer_indices if macierz_D[i][j] <= 10) >= 1
            )

        for prev in solutions:
            model += pulp.lpSum(y[j] for j in prev["set"]) <= len(prev["set"]) - 1

        status = model.solve()
        if pulp.LpStatus[status] != "Optimal":
            break

        chosen = [int(j) for j in farmer_indices if pulp.value(y[j]) >= 0.5]
        solutions.append({"set": set(chosen)})
        print(f"\nSolution {_ + 1}:")
        print(f"  Chosen farmers: {chosen}")
        print(f"  Objective value: {pulp.value(model.objective):.2f}")

    return solutions


def compute_solution_cost(
    chosen_farmers, scenario_df, dane, macierz_D, koszty_przesylek, dane_inv
):
    przypisanie = {}
    n = len(dane.rolnicy)
    for i in range(n):
        if i not in chosen_farmers:
            d_min = float("inf")
            najblizszy_j = None
            for j in chosen_farmers:
                dist = macierz_D[i][j]
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


def generate_scenarios(macierz_D, dane, scenarios_manager, number_of_scenarios):
    scenarios = []
    for i in range(number_of_scenarios):
        df = scenarios_manager.generate_scenario(KLIENTOW=100, MIESIAC=30)
        profit_per_farmer = df.groupby("rolnik_idx")["profit"].sum()
        scenarios.append(
            {
                "scenario_idx": i,
                "scenario_df": df,
                "profit_per_farmer": profit_per_farmer,
            }
        )
    return scenarios



candidate_solutions = generate_candidate_solutions(
    macierz_D, dane, scenarios_manager, NUM_SOLUTIONS=10
)


scenario_list = generate_scenarios(
    macierz_D, dane, scenarios_manager, number_of_scenarios=10
)



print("\nSummary of candidate solutions:")
for scenarios in scenario_list:
    print(f"\nScenario {scenarios['scenario_idx'] + 1}:")
    for idx, solution in enumerate(candidate_solutions):
        chosen_farmers = list(solution["set"])
        cost = compute_solution_cost(
            chosen_farmers,
            scenarios["scenario_df"],
            dane,
            macierz_D,
            koszty_przesylek,
            dane_inv={rolnik.id: idx for idx, rolnik in enumerate(dane.rolnicy)},
        )
        print(f"Solution {idx + 1}:")
        print(f"  Chosen farmers: {sorted(chosen_farmers)}")
        print(f"  Total cost: {cost:.2f}")


all_solutions = []
for scenario in scenario_list:
    for idx, solution in enumerate(candidate_solutions):
        all_solutions.append(
            {
                "scenario_idx": scenario["scenario_idx"],
                "solution_idx": idx,
                "chosen_farmers": list(solution["set"]),
                "profit_per_farmer": scenario["profit_per_farmer"],
                "total_cost": compute_solution_cost(
                    list(solution["set"]),
                    scenario["scenario_df"],
                    dane,
                    macierz_D,
                    koszty_przesylek,
                    dane_inv={
                        rolnik.id: idx for idx, rolnik in enumerate(dane.rolnicy)
                    },
                ),
            }
        )

print(all_solutions)


def find_single_minimax_regret_solution(
    candidate_solutions, scenarios, dane, macierz_D, koszty_przesylek
):
    dane_inv = {rolnik.id: idx for idx, rolnik in enumerate(dane.rolnicy)}

    best_solution = None
    best_max_regret = float("inf")

    for idx, candidate in enumerate(candidate_solutions):
        regrets = []
        profits = []

        for scenario in scenarios:
            scenario_df = scenario["scenario_df"]
            profit_per_farmer = scenario["profit_per_farmer"]

            chosen_set = candidate["set"]

            candidate_profit_sum = profit_per_farmer[
                ~profit_per_farmer.index.isin(chosen_set)
            ].sum()
            candidate_cost = compute_solution_cost(
                chosen_set, scenario_df, dane, macierz_D, koszty_przesylek, dane_inv
            )
            candidate_actual_profit = candidate_profit_sum - candidate_cost

            best_scenario_profit = float("-inf")
            for other in candidate_solutions:
                other_set = other["set"]
                other_profit_sum = profit_per_farmer[
                    ~profit_per_farmer.index.isin(other_set)
                ].sum()
                other_cost = compute_solution_cost(
                    other_set, scenario_df, dane, macierz_D, koszty_przesylek, dane_inv
                )
                other_actual_profit = other_profit_sum - other_cost
                if other_actual_profit > best_scenario_profit:
                    best_scenario_profit = other_actual_profit

            regret = best_scenario_profit - candidate_actual_profit
            regrets.append(regret)
            profits.append(candidate_actual_profit)

        max_regret = max(regrets)
        avg_profit = sum(profits) / len(profits)

        if max_regret < best_max_regret:
            best_max_regret = max_regret
            best_solution = {
                "solution_idx": idx,
                "set": chosen_set,
                "max_regret": max_regret,
                "avg_profit": avg_profit,
            }

    return best_solution


best_solution = find_single_minimax_regret_solution(
    candidate_solutions, scenario_list, dane, macierz_D, koszty_przesylek
)

print("\nBest single Minimax Regret solution from all solutions:")
print(f" Chosen Farmers: {sorted(best_solution['set'])}")
print(f" Max Regret: {best_solution['max_regret']:.2f}")
print(f" Avg Profit: {best_solution['avg_profit']:.2f}")


def compare_best_solutions_vs_minimax(
    best_solution, all_solutions, scenario_list, dane
):
    dane_inv = {rolnik.id: idx for idx, rolnik in enumerate(dane.rolnicy)}

    chosen_set = best_solution["set"]

    print("\nComparison of Best Scenario Solutions vs Minimax Regret Solution:\n")

    for scenario in scenario_list:
        scen_idx = scenario["scenario_idx"]
        profit_per_farmer = scenario["profit_per_farmer"]
        scenario_df = scenario["scenario_df"]

        best_profit = float("-inf")
        best_sol_in_scenario = None

        for sol in all_solutions:
            if sol["scenario_idx"] != scen_idx:
                continue
            sol_set = frozenset(sol["chosen_farmers"])
            profit_sum = profit_per_farmer[~profit_per_farmer.index.isin(sol_set)].sum()
            actual_profit = profit_sum - sol["total_cost"]

            if actual_profit > best_profit:
                best_profit = actual_profit
                best_sol_in_scenario = sol_set

        mmr_profit_sum = profit_per_farmer[
            ~profit_per_farmer.index.isin(chosen_set)
        ].sum()
        mmr_total_cost = None

        for sol in all_solutions:
            if (
                sol["scenario_idx"] == scen_idx
                and frozenset(sol["chosen_farmers"]) == chosen_set
            ):
                mmr_total_cost = sol["total_cost"]
                break

        mmr_profit = mmr_profit_sum - (
            mmr_total_cost if mmr_total_cost is not None else 0
        )

        print(f"Scenario {scen_idx + 1}:")
        print(
            f"  Best Scenario Solution Profit: {best_profit:.2f} (Chosen Farmers: {sorted(best_sol_in_scenario)})"
        )
        print(
            f"  Minimax Regret Solution Profit: {mmr_profit:.2f} (Chosen Farmers: {sorted(chosen_set)})"
        )
        print()


compare_best_solutions_vs_minimax(best_solution, all_solutions, scenario_list, dane)



with open("best_solution_data.py", "w") as f:
    f.write(f"best_solution = {best_solution}")


















# import pulp
# from distance_matrix import DistanceMatrix
# from scenarios import Scenarios
# from test import Dane

# # --- Load Data ---
# distances = DistanceMatrix()
# distances.wczytaj_z_pliku("dane.txt")
# distances.konwertuj_wszystkich_na_km()
# macierz_D = distances.oblicz_macierz_odleglosci()

# dane = Dane()
# dane.wczytaj_z_pliku("dane.txt")
# dane.konwertuj_wszystkich_na_km()

# scenarios_manager = Scenarios(dane)
# scenario_df = scenarios_manager.generate_scenario(KLIENTOW=100, MIESIAC=30)
# print(scenario_df)

# # Costs per order
# koszty_przesylek = {1: 6.36, 2: 5.71, 3: 5.07, 4: 4.44, 5: 0}

# n_farmers = len(dane.rolnicy)
# profit_per_farmer = scenario_df.groupby("rolnik_idx")["profit"].sum()
# farmer_indices = profit_per_farmer.index.tolist()

# # Store each solution's chosen farmer indices and objective value
# solutions_data = []

# NUM_SOLUTIONS = 10  # Number of distinct solutions to find

# for iteration in range(NUM_SOLUTIONS):
#     model = pulp.LpProblem("Maksymalizacja_zysku", pulp.LpMaximize)
#     y = {j: pulp.LpVariable(f"y_{j}", cat="Binary") for j in farmer_indices}

#     # Objective: maximize profit from farmers not chosen as points
#     model += pulp.lpSum(profit_per_farmer[j] * (1 - y[j]) for j in farmer_indices)

#     # Coverage constraints
#     for i in range(n_farmers):
#         model += pulp.lpSum(y[j] for j in farmer_indices if macierz_D[i][j] <= 10) >= 1

#     # Exclude all previous sets of chosen points
#     for prev_set in solutions_data:
#         model += pulp.lpSum(y[j] for j in prev_set["set"]) <= len(prev_set["set"]) - 1

#     # Solve LP
#     status = model.solve()

#     if pulp.LpStatus[status] != "Optimal":
#         print("No more distinct solutions can be found.")
#         break

#     # Extract chosen farmers
#     chosen_farmers = [int(j) for j in farmer_indices if pulp.value(y[j]) >= 0.5]
#     obj_value = pulp.value(model.objective)
#     solutions_data.append({"set": set(chosen_farmers), "objective": obj_value})

#     print(f"\nSolution {iteration+1}:")
#     print(f"Chosen points: {chosen_farmers}")
#     print(f"Objective: {obj_value:.2f}")

# # After loop, compare objective values
# print("\nSummary of solutions and their objectives:")
# for idx, s in enumerate(solutions_data):
#     print(
#         f"Solution {idx+1}: Objective = {s['objective']:.2f}, Chosen farmers = {sorted(s['set'])}"
#     )

# # Find max, min, and difference
# objectives = [s["objective"] for s in solutions_data]
# max_obj = max(objectives)
# min_obj = min(objectives)
# print(f"\nMaximum Objective Value: {max_obj:.2f}")
# print(f"Minimum Objective Value: {min_obj:.2f}")
# print(f"Difference: {max_obj - min_obj:.2f}")
# # Display the objective vaule of each solution


# # Function to compute total transport cost for a given solution
# def compute_solution_cost(chosen_farmers, scenario_df, dane, macierz_D, koszty_przesylek):
#     punkt_odbioru_ids = [dane.rolnicy[j].id for j in chosen_farmers]

#     # Assign each farmer (not in chosen) to the nearest pickup point
#     przypisanie = {}
#     n = len(dane.rolnicy)

#     for i in range(n):
#         if i not in chosen_farmers:
#             d_min = float('inf')
#             najblizszy_j = None
#             for j in chosen_farmers:
#                 if macierz_D[i][j] < d_min:
#                     d_min = macierz_D[i][j]
#                     najblizszy_j = j
#             przypisanie[i] = najblizszy_j

#     # Prepare a dict: key=pickup_point_id, value=list of farmers assigned
#     przypisani_z_rolnika = {dane.rolnicy[j].id: [] for j in chosen_farmers}
#     for i, j in przypisanie.items():
#         id_rolnika = dane.rolnicy[i].id
#         id_punktu = dane.rolnicy[j].id
#         przypisani_z_rolnika[id_punktu].append(id_rolnika)

#     # Calculate total transportation cost over scenario days
#     total_koszt = 0
#     dny = scenario_df['dzien'].unique()
#     for punkt_id, rolnicy_ids in przypisani_z_rolnika.items():
#         for d in dny:
#             # Count orders for this pickup point and day
#             liczba_zamowien = len(scenario_df[
#                 (scenario_df['dzien'] == d) &
#                 (scenario_df['rolnik_idx'].isin([dane.rolnicy_inv[id] for id in rolnicy_ids]))
#             ])
#             if liczba_zamowien > 0:
#                 if liczba_zamowien > 5:
#                     koszt = 0
#                 else:
#                     koszt = koszty_przesylek.get(liczba_zamowien, 0)
#                 total_koszt += koszt * liczba_zamowien
#     return total_koszt

# # Placeholder: create a reverse mapping from 'id' to index if needed
# dane.rolnicy_inv = {rolnik.id: idx for idx, rolnik in enumerate(dane.rolnicy)}

# # For each solution, compute cost
# solution_costs = []
# for s in solutions_data:
#     chosen_farmers = list(s['set'])
#     cost = compute_solution_cost(chosen_farmers, scenario_df, dane, macierz_D, koszty_przesylek)
#     solution_costs.append(cost)

# print("\nSummary of all solutions:")
# for idx, s in enumerate(solutions_data):
#     print(f"Solution {idx+1}:")
#     print(f"  Objective (profit): {s['objective']:.2f}")
#     print(f"  Total transportation cost: {solution_costs[idx]:.2f}")
#     print(f"  Chosen farmers (indices): {sorted(s['set'])}")

# # Find the best solution based on criteria
# best_idx = None
# best_value = None
# for idx, s in enumerate(solutions_data):
#     # Example criterion: minimal cost, then maximal profit
#     if best_idx is None:
#         best_idx = idx
#         best_value = (solution_costs[idx], s['objective'])
#     else:
#         if solution_costs[idx] < best_value[0]:
#             best_idx = idx
#             best_value = (solution_costs[idx], s['objective'])
#         elif solution_costs[idx] == best_value[0]:
#             if s['objective'] > best_value[1]:
#                 best_idx = idx
#                 best_value = (solution_costs[idx], s['objective'])

# # Output the best solution
# best_solution = solutions_data[best_idx]
# print("\nBest solution based on minimal cost and maximal profit:")
# print(f"Objective (profit): {best_solution['objective']:.2f}")
# print(f"Total transportation cost: {solution_costs[best_idx]:.2f}")
# print(f"Chosen farmers (indices): {sorted(best_solution['set'])}")


# n_scenarios = 10
# scenario_list = []
# for _ in range(n_scenarios):
#     scenario_df = scenarios_manager.generate_scenario(KLIENTOW=100, MIESIAC=30)
#     print(f"Generated scenario with {len(scenario_df)} orders.")
#     scenario_list.append(scenario_df)


# all_solution_costs = [[] for _ in range(len(solutions_data))]

# for scenario_idx, scenario_df in enumerate(scenario_list):
#     for sol_idx, s in enumerate(solutions_data):
#         chosen_farmers = list(s['set'])
#         print(f"Computing cost for solution {sol_idx+1} in scenario {scenario_idx+1}...")
#         cost = compute_solution_cost(chosen_farmers, scenario_df, dane, macierz_D, koszty_przesylek)
#         all_solution_costs[sol_idx].append(cost)


# max_regrets = []

# for sol_idx in range(len(solutions_data)):
#     regrets = []
#     for scenario_idx in range(n_scenarios):
#         costs = [all_solution_costs[other_idx][scenario_idx] for other_idx in range(len(solutions_data))]
#         min_cost_in_scenario = min(costs)
#         print(f"Solution {sol_idx+1}, Scenario {scenario_idx+1}: Min cost = {min_cost_in_scenario:.2f}")
#         regret = all_solution_costs[sol_idx][scenario_idx] - min_cost_in_scenario
#         regrets.append(regret)
#     max_regret = max(regrets)
#     max_regrets.append(max_regret)


# best_idx = min(range(len(solutions_data)), key=lambda i: max_regrets[i])
# best_solution = solutions_data[best_idx]

# print(f"\nSolution with minimal maximum regret:")
# print(f"Objective (profit): {best_solution['objective']:.2f}")
# print(f"Maximum regret: {max_regrets[best_idx]:.2f}")
# print(f"Chosen farmers (indices): {sorted(best_solution['set'])}")


# print("\nDetailed comparison of all solutions:")

# for idx, s in enumerate(solutions_data):
#     print(f"\nSolution {idx+1}:")
#     print(f"  Objective (profit): {s['objective']:.2f}")
#     print(f"  Max regret: {max_regrets[idx]:.2f}")
#     print(f"  Farmers (indices): {sorted(s['set'])}")
#     costs = all_solution_costs[idx]
#     print("  Costs per scenario:")
#     for scenario_idx, cost in enumerate(costs):
#         print(f"    Scenario {scenario_idx+1}: {cost:.2f}")
#     # Optional: show average or median cost across scenarios
#     avg_cost = sum(costs) / len(costs)
#     print(f"  Average cost: {avg_cost:.2f}")


# best_scenario_values = []

# for scenario_idx, scenario_df in enumerate(scenario_list):
#     max_profit_minus_cost = None
#     best_solution_idx = None
#     for sol_idx, s in enumerate(solutions_data):
#         chosen_farmers = list(s['set'])
#         cost = compute_solution_cost(chosen_farmers, scenario_df, dane, macierz_D, koszty_przesylek)
#         profit = s['objective']
#         profit_minus_cost = profit - cost
#         if (max_profit_minus_cost is None) or (profit_minus_cost > max_profit_minus_cost):
#             max_profit_minus_cost = profit_minus_cost
#             best_solution_idx = sol_idx
#     best_scenario_values.append({
#         'scenario': scenario_idx,
#         'best_solution_idx': best_solution_idx,
#         'max_profit_minus_cost': max_profit_minus_cost
#     })
