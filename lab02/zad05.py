import numpy as np
import random
from graph_representation import Graph
from graph_visualization import visualize_circular

def generate_k_regular_graph(n, k):
    """Generuje k-regularny graf dla n wierzchołków, obsługując przypadek k=1."""
    if n <= k:
        raise ValueError("Błąd: n musi być większe niż k.")
    if k % 2 == 1 and n % 2 == 1:
        raise ValueError("Błąd: jeśli k jest nieparzyste, to n musi być parzyste.")

    graph = Graph(n)

    # Przypadek specjalny: jeśli k = 1, łączymy wierzchołki w pary
    if k == 1:
        vertices = list(range(n))
        random.shuffle(vertices)  # Mieszamy wierzchołki, aby dobrać losowe pary
        for i in range(0, n, 2):
            graph.add_edge(vertices[i], vertices[i + 1])
        print(f"Wygenerowano {k}-regularny graf dla {n} wierzchołków (niespójne pary).")
        return graph

    # Tworzymy cykl (pierścień) – każde n jest połączone z n+1
    for i in range(n):
        graph.add_edge(i, (i + 1) % n)

    # Dodajemy kolejne krawędzie, aby uzyskać k-regularność
    half_k = k // 2  # Połowa stopnia (dla k parzystych)
    for step in range(1, half_k + 1):
        for i in range(n):
            graph.add_edge(i, (i + step) % n)

    # Jeśli k jest nieparzyste, dodajemy jedną dodatkową warstwę połączeń
    if k % 2 == 1:
        for i in range(n // 2):
            graph.add_edge(i, i + (n // 2))

    print(f"Wygenerowano {k}-regularny graf dla {n} wierzchołków.")
    return graph

# Przykładowe użycie:
n, k = 8, 5  # Liczba wierzchołków i stopień k
graph = generate_k_regular_graph(n, k)
visualize_circular(graph, title=f"{k}-regularny graf dla {n} wierzchołków")