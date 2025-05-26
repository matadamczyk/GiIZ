import random
import numpy as np
from collections import defaultdict

def build_graph(adj_list):
    graph = defaultdict(list)
    nodes = set()
    for u, vs in adj_list.items():
        for v in vs:
            graph[u].append(v)
            nodes.update([u, v])
    return graph, list(nodes)

def pagerank_random_walk(graph, nodes, d=0.15, steps=1_000_000):
    """
    Metoda błądzenia przypadkowego z teleportacją.
    d - prawdopodobieństwo teleportacji
    """
    visits = defaultdict(int)
    node = random.choice(nodes)
    
    for _ in range(steps):
        if random.random() < d or not graph[node]:
            # Teleportacja - wybierz losowy węzeł
            node = random.choice(nodes)
        else:
            # Przejdź do sąsiada
            node = random.choice(graph[node])
        visits[node] += 1
    
    total = sum(visits.values())
    return {k: v / total for k, v in visits.items()}

def pagerank_power_iteration(graph, nodes, d=0.15, max_iter=100, tolerance=1e-6):
    """
    Metoda iteracji wektora obsadzeń.
    d - prawdopodobieństwo teleportacji
    """
    n = len(nodes)
    index = {node: i for i, node in enumerate(nodes)}
    
    # Budowa macierzy przejścia A
    A = np.zeros((n, n))
    for node in nodes:
        j = index[node]
        neighbors = graph[node]
        if neighbors:
            for neighbor in neighbors:
                i = index[neighbor]
                A[i, j] = 1 / len(neighbors)
        else:
            # Węzeł bez wychodzących krawędzi - równomierne rozłożenie
            for i in range(n):
                A[i, j] = 1 / n
    
    P = (1 - d) * A + d / n * np.ones((n, n))
    
    # Wektor początkowy
    p = np.ones(n) / n
    
    # Iteracje
    for iteration in range(max_iter):
        p_new = P @ p
        if np.linalg.norm(p_new - p, 1) < tolerance:
            print(f"Zbieżność metody uzyskano po {iteration + 1} iteracjach.")
            break
        p = p_new
    
    return {nodes[i]: p[i] for i in range(n)}

def print_results(rank, method_name):
    """Wypisuje wyniki posortowane malejąco według wartości PageRank"""
    sorted_rank = sorted(rank.items(), key=lambda x: x[1], reverse=True)
    print(f"\n({method_name})")
    for i, (node, value) in enumerate(sorted_rank, 1):
        print(f"{i:2d} {node} ==> PageRank = {value:.5f}")

# Dane wejściowe zgodne z obrazkiem
adj_list = {
    'A': ['E', 'F', 'I'],
    'B': ['A', 'C', 'F'],
    'C': ['B', 'D', 'E', 'L'],
    'D': ['C', 'E', 'H', 'I', 'K'],
    'E': ['C', 'G', 'H', 'I'],
    'F': ['B', 'G'],
    'G': ['E', 'F', 'H'],
    'H': ['D', 'G', 'I', 'L'],
    'I': ['D', 'E', 'H', 'J'],
    'J': ['I'],
    'K': ['D', 'I'],
    'L': ['A', 'H'],
}

graph, nodes = build_graph(adj_list)

# Ustawienie ziarna dla powtarzalności wyników
random.seed(42)
np.random.seed(42)

# Obliczenia PageRank
rank_a = pagerank_random_walk(graph, nodes, d=0.15, steps=1_000_000)
rank_b = pagerank_power_iteration(graph, nodes, d=0.15, max_iter=100)

# Wyświetlenie wyników
print_results(rank_a, "a) Efekt N = 1000000 kroków błądzenia przypadkowego z teleportacją")
print_results(rank_b, "b) Efekt metody potęgowej (metody iteracji wektora obsadzeń)")