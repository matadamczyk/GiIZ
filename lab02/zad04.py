import random
import numpy as np
from graph_representation import Graph
from graph_visualization import visualize_circular
from lab02.zad01 import construct_graph, is_graphical_sequence
from lab02.zad03 import is_graph_connected


def generate_eulerian_graph(num_vertices):
    """Generuje losowy graf eulerowski poprzez tworzenie stopni parzystych."""
    while True:
        degree_sequence = [random.randrange(2, num_vertices, 2) for _ in range(num_vertices)]  # Parzyste stopnie

        if is_graphical_sequence(degree_sequence):
            graph = construct_graph(degree_sequence)
            if is_graph_connected(graph):
                print("Ciąg jest graficzny i graf jest spójny. Budowanie grafu eulerowskiego...")
                return graph
            else:
                print("Wylosowany graf nie jest spójny, próbuję ponownie...")
        else:
            print("Wylosowany ciąg nie jest graficzny, próbuję ponownie...")

def find_eulerian_cycle(graph):
    """Znajduje cykl Eulera w grafie przy użyciu algorytmu Fleury'ego."""
    if not is_graph_connected(graph):
        print("Graf nie jest spójny, więc nie posiada cyklu Eulera.")
        return None

    for v in range(graph.V):
        if len(graph.get_adjacency_list()[v]) % 2 != 0:
            print("Graf nie jest eulerowski, ponieważ posiada wierzchołek o nieparzystym stopniu.")
            return None

    graph_copy = Graph(graph.V)
    for u, neighbors in enumerate(graph.get_adjacency_list()):
        for v in neighbors:
            graph_copy.add_edge(u, v)

    stack = [0]
    path = []

    while stack:
        u = stack[-1]
        if graph_copy.get_adjacency_list()[u]:
            v = graph_copy.get_adjacency_list()[u][0]
            graph_copy.get_adjacency_list()[u].remove(v)
            graph_copy.get_adjacency_list()[v].remove(u)
            stack.append(v)
        else:
            path.append(stack.pop())

    return path

# Przykładowe użycie:
num_vertices = 6  # Liczba wierzchołków
graph = generate_eulerian_graph(num_vertices)

if graph:
    visualize_circular(graph, title="Graf Eulerowski")
    eulerian_cycle = find_eulerian_cycle(graph)
    if eulerian_cycle:
        print(f"Znaleziony cykl Eulera: {eulerian_cycle}")
    else:
        print("Nie znaleziono cyklu Eulera.")