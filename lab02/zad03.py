import numpy as np
from graph_representation import Graph
from graph_visualization import visualize_circular
from lab02.zad01 import construct_graph, is_graphical_sequence

def dfs(v, graph, visited, component):
    """Przechodzi przez graf DFS-em i zapisuje wierzchołki w jednej składowej spójnej."""
    visited[v] = True
    component.append(v)
    for neighbor in graph.get_adjacency_list()[v]:
        if not visited[neighbor]:
            dfs(neighbor, graph, visited, component)

def is_graph_connected(graph):
    """Sprawdza, czy graf jest spójny."""
    visited = [False] * graph.V
    component = []
    dfs(0, graph, visited, component)
    return all(visited)

def find_largest_connected_component(graph):
    """Znajduje największą składową spójną w grafie."""
    visited = [False] * graph.V
    largest_component = []

    for v in range(graph.V):
        if not visited[v]:
            component = []
            dfs(v, graph, visited, component)
            if len(component) > len(largest_component):
                largest_component = component

    return largest_component

# Przykładowe użycie:
degree_sequence = [3, 3, 2, 2, 1, 1]  # Przykładowy ciąg

if is_graphical_sequence(degree_sequence):
    print("Ciąg jest graficzny. Budowanie grafu...")
    graph = construct_graph(degree_sequence)
    visualize_circular(graph, title="Oryginalny graf")

    if is_graph_connected(graph):
        print("Graf jest spójny.")
    else:
        print("Graf NIE jest spójny.")

    largest_component = find_largest_connected_component(graph)
    print(f"Największa składowa spójna zawiera wierzchołki: {largest_component}")

    # Tworzenie podgrafu największej składowej
    largest_subgraph = Graph(len(largest_component))
    node_mapping = {node: i for i, node in enumerate(largest_component)}

    for u in largest_component:
        for v in graph.get_adjacency_list()[u]:
            if v in node_mapping:
                largest_subgraph.add_edge(node_mapping[u], node_mapping[v])

    visualize_circular(largest_subgraph, title="Największa składowa spójna")
else:
    print("Podany ciąg nie jest graficzny. Nie można zbudować grafu.")