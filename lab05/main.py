import random

from lab05.AddRandomEdges import add_random_edges
from lab05.ConnectLayers import connect_layers
from lab05.EdmondsKarp import edmonds_karp
from lab05.FlowNetwork import FlowNetwork
from lab05.GenerateRandomLayers import generate_random_layers


def build_random_network(N):
    assert 2 <= N <= 4

    # Generujemy warstwy i przypisujemy im wierzchołki
    node_layer_map = generate_random_layers(N)

    # Węzły podstawowe
    base_edges = connect_layers(node_layer_map, N)

    # Węzły pozostałe
    all_edges = add_random_edges(base_edges, node_layer_map, N)

    # Tworzenie obiektu FlowNetwork, używana głównie do rysowania
    net = FlowNetwork()

    # Dodatnie warstw i wierzchołków
    for node, layer in node_layer_map.items():
        net.add_node(node, layer)

    # Dodanie krawędzi
    for u, v in all_edges:
        capacity = random.randint(1, 10)
        net.add_edge(u, v, capacity)

    return net

if __name__ == "__main__":
    net = build_random_network(2)
    net.draw()

    fmax, flow, cap = edmonds_karp(net)
    print("Maksymalny przepływ:", fmax)

    net.draw_with_flow(flow, cap)
