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

    if k == 1:
        vertices = list(range(n))
        random.shuffle(vertices)
        for i in range(0, n, 2):
            graph.add_edge(vertices[i], vertices[i + 1])
        print(f"Wygenerowano {k}-regularny graf dla {n} wierzchołków (niespójne pary).")
        return graph

    for i in range(n):
        graph.add_edge(i, (i + 1) % n)

    half_k = k // 2
    for step in range(1, half_k + 1):
        for i in range(n):
            graph.add_edge(i, (i + step) % n)

    if k % 2 == 1:
        for i in range(n // 2):
            graph.add_edge(i, i + (n // 2))

    print(f"Wygenerowano {k}-regularny graf dla {n} wierzchołków.")
    return graph

def zad05(n, k):
    graph = generate_k_regular_graph(n, k)
    visualize_circular(graph, title=f"{k}-regularny graf dla {n} wierzchołków")