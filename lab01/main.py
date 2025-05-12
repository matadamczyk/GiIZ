from graph import Graph, visualize_circular, generate_gnm_random_graph, generate_gnp_random_graph
import numpy as np
import matplotlib.pyplot as plt
import os

def print_matrix(matrix):
    for i, row in enumerate(matrix):
        print(f"{i+1:2d}: {row}")

def main():
    print("Zadanie 1 - Reprezentacje grafów prostych")
    print("=" * 70)

    print("\n1.1. Tworzenie grafu z macierzy sąsiedztwa")
    print("-" * 70)
    
    adjacency_matrix = [
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    ]
    
    graph_from_adj = Graph(12, 'adjacency_matrix', adjacency_matrix)
    
    print("Macierz sąsiedztwa z przykładu:")
    print_matrix(adjacency_matrix)
    
    print("\n1.2. Lista sąsiedztwa wygenerowana z macierzy:")
    print("-" * 70)
    
    adj_list = graph_from_adj.get_adjacency_list()
    for i, neighbors in enumerate(adj_list):
        neighbors_plus1 = [n+1 for n in neighbors]
        print(f"{i+1:2d}: {neighbors_plus1}")
    
    print("\n1.3. Macierz incydencji wygenerowana z macierzy sąsiedztwa:")
    print("-" * 70)
    
    inc_matrix = graph_from_adj.get_incidence_matrix()
    print_matrix(inc_matrix)
    
    print("\n2. Wizualizacja grafu")
    print("-" * 70)
    
    if not os.path.exists("output"):
        os.makedirs("output")
        
    save_path = "output/graf_z_zadania.png"
    visualize_circular(graph_from_adj, title="Graf z zadania", save_path=save_path)
    print(f"Wizualizacja zapisana do pliku: {save_path}")
    
    visualize_circular(graph_from_adj, title="Graf z zadania")
    
    print("\n3. Generowanie losowych grafów")
    print("-" * 70)
    
    print("\n3.1. Model G(n,l) - graf losowy z zadaną liczbą wierzchołków i krawędzi")
    print("-" * 70)
    
    n = 7  # liczba wierzchołków
    l = 10  # liczba krawędzi
    
    print(f"Generowanie grafu G({n},{l}) - {n} wierzchołków, {l} krawędzi")
    g_nl = generate_gnm_random_graph(n, l)
    
    print("Wygenerowana macierz sąsiedztwa:")
    print_matrix(g_nl.get_adjacency_matrix())
    
    print("\nWygenerowana lista sąsiedztwa:")
    adj_list = g_nl.get_adjacency_list()
    for i, neighbors in enumerate(adj_list):
        neighbors_plus1 = [n+1 for n in neighbors]
        print(f"{i+1:2d}: {neighbors_plus1}")
    
    save_path_nl = f"output/graf_gnl_{n}_{l}.png"
    visualize_circular(g_nl, title=f"Losowy graf G({n},{l})", save_path=save_path_nl)
    print(f"Wizualizacja zapisana do pliku: {save_path_nl}")
    
    print("\n3.2. Model G(n,p) - graf losowy z zadaną liczbą wierzchołków i prawdopodobieństwem")
    print("-" * 70)
    
    n = 7  # liczba wierzchołków
    p = 0.5  # prawdopodobieństwo istnienia krawędzi
    
    print(f"Generowanie grafu G({n},{p}) - {n} wierzchołków, p={p}")
    g_np = generate_gnp_random_graph(n, p)
    
    print("Wygenerowana macierz sąsiedztwa:")
    print_matrix(g_np.get_adjacency_matrix())
    
    print("\nWygenerowana lista sąsiedztwa:")
    adj_list = g_np.get_adjacency_list()
    for i, neighbors in enumerate(adj_list):
        neighbors_plus1 = [n+1 for n in neighbors]
        print(f"{i+1:2d}: {neighbors_plus1}")
    
    save_path_np = f"output/graf_gnp_{n}_{p}.png"
    visualize_circular(g_np, title=f"Losowy graf G({n},{p})", save_path=save_path_np)
    print(f"Wizualizacja zapisana do pliku: {save_path_np}")
    
    print("\nZadanie zakończone.")

if __name__ == "__main__":
    main() 