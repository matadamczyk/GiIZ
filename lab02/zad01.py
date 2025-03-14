import numpy as np
from itertools import combinations
from copy import deepcopy

from graph_representation import Graph
from graph_visualization import visualize_circular


def is_graphical_sequence(sequence):
    sequence = sorted(sequence, reverse=True)

    while True:
        if all(deg == 0 for deg in sequence):
            return True, "Ciąg jest graficzny."

        if sequence[0] >= len(sequence):
            return False, "Największy stopień jest większy niż liczba wierzchołków."

        if any(deg < 0 for deg in sequence):
            return False, "Ciąg zawiera ujemne stopnie, co jest niemożliwe w grafie prostym."

        first = sequence.pop(0)
        for i in range(first):
            if i >= len(sequence):
                return False, "Nie można poprawnie połączyć wierzchołków w grafie."
            sequence[i] -= 1

        sequence = sorted(sequence, reverse=True)


def construct_graph(sequence):
    is_graphical, reason = is_graphical_sequence(sequence)
    if not is_graphical:
        raise ValueError(f"Podany ciąg nie jest graficzny: {reason}")

    sequence = sorted(enumerate(sequence), key=lambda x: x[1], reverse=True)  # Sortowanie par (index, stopień)
    graph = Graph(len(sequence))  # Tworzenie pustego grafu

    while any(deg > 0 for _, deg in sequence):
        index, degree = sequence.pop(0)  # Pobranie pierwszego wierzchołka
        sequence = sorted(sequence, key=lambda x: x[1], reverse=True)  # Ponowne sortowanie

        for i in range(degree):
            if i >= len(sequence):
                raise ValueError("Nie można utworzyć grafu dla podanego ciągu")

            neighbor_index, neighbor_degree = sequence[i]
            graph.add_edge(index, neighbor_index)
            sequence[i] = (neighbor_index, neighbor_degree - 1)

        sequence = sorted(sequence, key=lambda x: x[1], reverse=True)  # Ponowne sortowanie

    return graph

# Przykładowe użycie:
degree_sequences = [
    [1,3,2,3,2,4,1],
    [1,3,3,4,2,3,1],
    [1,3,3,7,2,3,1],
    [2,2,6,4,4,6,6]
]

for degree_sequence in degree_sequences:
    is_graphical, reason = is_graphical_sequence(degree_sequence)
    if is_graphical:
        print(f"Ciąg {degree_sequence} jest graficzny. Budowanie grafu...")
        graph = construct_graph(degree_sequence)
        visualize_circular(graph)
    else:
        print(f"Podany ciąg {degree_sequence} nie jest graficzny. Powód: {reason}")