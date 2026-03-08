"""
============================================================
  Genetic Algorithm (GA) — Evolution-Inspired Algorithm
============================================================
  Genetic Algorithms are optimization algorithms inspired
  by Charles Darwin's theory of natural evolution.

  Biological Analogy → GA Concept:
    Individual/Organism  → Candidate solution (chromosome)
    Population           → Set of candidate solutions
    Fitness              → Quality of a solution
    Selection            → Choose best individuals to reproduce
    Crossover (Recomb.)  → Combine parents to create offspring
    Mutation             → Random changes to offspring
    Generation           → One iteration of the algorithm

  Steps:
    1. Initialize a random population
    2. Evaluate fitness of each individual
    3. Select parents based on fitness
    4. Apply crossover to create offspring
    5. Apply mutation to offspring
    6. Replace old population with new generation
    7. Repeat steps 2–6 until solution is found or
       max generations reached
============================================================
"""

import random
import math

random.seed(42)  # For reproducibility


# ─────────────────────────────────────────────
# EXAMPLE 1: Maximizing a Mathematical Function
# Find x in [0, 31] that maximizes f(x) = x²
# Using binary encoding (5-bit chromosome)
# ─────────────────────────────────────────────

def ga_maximize_function():
    print("=" * 58)
    print("  GENETIC ALGORITHM — EXAMPLE 1: Maximize f(x) = x²")
    print("  Domain: x ∈ [0, 31]  (5-bit binary chromosome)")
    print("=" * 58)

    # Parameters
    POP_SIZE    = 6
    GENERATIONS = 20
    CROSSOVER_RATE = 0.8
    MUTATION_RATE  = 0.05
    CHROMOSOME_LEN = 5  # 2^5 = 32 possible values (0–31)

    def encode(x):
        return format(x, f'0{CHROMOSOME_LEN}b')

    def decode(chromosome):
        return int(chromosome, 2)

    def fitness(chromosome):
        x = decode(chromosome)
        return x ** 2

    def selection(population):
        # Tournament selection (pick best of 3 random individuals)
        tournament = random.sample(population, 3)
        return max(tournament, key=fitness)

    def crossover(parent1, parent2):
        if random.random() < CROSSOVER_RATE:
            point = random.randint(1, CHROMOSOME_LEN - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2

    def mutate(chromosome):
        result = ""
        for bit in chromosome:
            if random.random() < MUTATION_RATE:
                result += '1' if bit == '0' else '0'
            else:
                result += bit
        return result

    # Initialize random population
    population = [encode(random.randint(0, 31)) for _ in range(POP_SIZE)]

    print(f"\n  Initial Population:")
    for chrom in population:
        x = decode(chrom)
        print(f"    Chromosome: {chrom}  |  x = {x:2d}  |  f(x) = {fitness(chrom)}")

    best_history = []

    for gen in range(GENERATIONS):
        new_population = []
        while len(new_population) < POP_SIZE:
            p1 = selection(population)
            p2 = selection(population)
            c1, c2 = crossover(p1, p2)
            new_population.append(mutate(c1))
            new_population.append(mutate(c2))
        population = new_population[:POP_SIZE]

        best = max(population, key=fitness)
        best_history.append((gen + 1, decode(best), fitness(best)))

    print(f"\n  Evolution Progress (every 5 generations):")
    print(f"  {'Gen':>4}  {'Best x':>8}  {'f(x) = x²':>12}")
    print("  " + "-" * 30)
    for g, x, f in best_history:
        if g % 5 == 0 or g == 1 or g == GENERATIONS:
            print(f"  {g:>4}  {x:>8}  {f:>12}")

    best_final = max(population, key=fitness)
    x_best = decode(best_final)
    print(f"\n  ✔ Best Solution Found: x = {x_best}, f({x_best}) = {fitness(best_final)}")
    print(f"  ✔ Optimal Answer:      x = 31,  f(31) = 961")


ga_maximize_function()


# ─────────────────────────────────────────────
# EXAMPLE 2: Travelling Salesman Problem (TSP)
# Find the shortest route visiting all cities
# exactly once and returning to the start
# ─────────────────────────────────────────────

def ga_tsp():
    print("\n" + "=" * 58)
    print("  GENETIC ALGORITHM — EXAMPLE 2: Travelling Salesman")
    print("  Find the shortest route visiting 7 Philippine cities")
    print("=" * 58)

    # Cities and approximate distances (km) between them
    cities = ["Manila", "Cebu", "Davao", "Iloilo", "Zamboanga", "Cagayan de Oro", "Bacolod"]
    # Distance matrix (symmetric)
    dist = [
        #  MNL   CEB   DAV   ILO   ZAM   CDO   BAC
        [   0,  587,  964,  565,  922,  840,  533],  # Manila
        [ 587,    0,  457,  179,  520,  380,  196],  # Cebu
        [ 964,  457,    0,  484,  332,  302,  524],  # Davao
        [ 565,  179,  484,    0,  411,  431,  128],  # Iloilo
        [ 922,  520,  332,  411,    0,  225,  393],  # Zamboanga
        [ 840,  380,  302,  431,  225,    0,  322],  # Cagayan de Oro
        [ 533,  196,  524,  128,  393,  322,    0],  # Bacolod
    ]
    n_cities = len(cities)

    def route_distance(route):
        total = 0
        for i in range(len(route)):
            total += dist[route[i]][route[(i + 1) % len(route)]]
        return total

    def fitness(route):
        return 1 / route_distance(route)  # Higher is better (shorter route)

    def order_crossover(p1, p2):
        size = len(p1)
        a, b = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[a:b+1] = p1[a:b+1]
        pointer = (b + 1) % size
        for gene in p2[b+1:] + p2[:b+1]:
            if gene not in child:
                child[pointer] = gene
                pointer = (pointer + 1) % size
        return child

    def mutate_swap(route, mutation_rate=0.1):
        route = route[:]
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]
        return route

    def selection_tournament(population, k=3):
        tournament = random.sample(population, k)
        return max(tournament, key=fitness)

    # Initialize population (random permutations)
    POP_SIZE    = 50
    GENERATIONS = 200

    population = [random.sample(range(n_cities), n_cities) for _ in range(POP_SIZE)]

    print(f"\n  Cities: {', '.join(cities)}")
    best_route_overall = min(population, key=route_distance)
    print(f"\n  Initial Best Distance: {route_distance(best_route_overall)} km")
    print(f"  Initial Best Route:    {' → '.join(cities[i] for i in best_route_overall)} → {cities[best_route_overall[0]]}")

    best_history = []

    for gen in range(GENERATIONS):
        new_population = []
        # Elitism: keep the best individual
        elite = min(population, key=route_distance)
        new_population.append(elite)

        while len(new_population) < POP_SIZE:
            p1 = selection_tournament(population)
            p2 = selection_tournament(population)
            child = order_crossover(p1, p2)
            child = mutate_swap(child)
            new_population.append(child)

        population = new_population
        best = min(population, key=route_distance)
        best_history.append((gen + 1, route_distance(best)))

        if route_distance(best) < route_distance(best_route_overall):
            best_route_overall = best

    print(f"\n  Evolution Progress (every 50 generations):")
    print(f"  {'Gen':>6}  {'Best Distance (km)':>20}")
    print("  " + "-" * 30)
    for g, d in best_history:
        if g % 50 == 0 or g == 1 or g == GENERATIONS:
            print(f"  {g:>6}  {d:>20}")

    print(f"\n  ✔ Best Route Found:")
    route_names = [cities[i] for i in best_route_overall]
    print(f"     {' → '.join(route_names)} → {route_names[0]}")
    print(f"  ✔ Total Distance: {route_distance(best_route_overall)} km")


ga_tsp()

print("\n  Done! Genetic Algorithm solved both optimization problems.")
