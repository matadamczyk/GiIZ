from graph_representation import Graph
from lab02.graph_visualization import visualize_circular


def is_graphical_sequence(sequence):
    odd_count = sum(1 for deg in sequence if deg % 2 != 0)
    if odd_count % 2 != 0:
        return False, "Liczba wierzchołków o nieparzystym stopniu jest nieparzysta, więc ciąg nie jest graficzny."

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

    sequence = sorted(enumerate(sequence), key=lambda x: x[1], reverse=True)
    graph = Graph(len(sequence))

    while any(deg > 0 for _, deg in sequence):
        index, degree = sequence.pop(0)
        sequence = sorted(sequence, key=lambda x: x[1], reverse=True)

        for i in range(degree):
            if i >= len(sequence):
                raise ValueError("Nie można utworzyć grafu dla podanego ciągu")

            neighbor_index, neighbor_degree = sequence[i]
            graph.add_edge(index, neighbor_index)
            sequence[i] = (neighbor_index, neighbor_degree - 1)

        sequence = sorted(sequence, key=lambda x: x[1], reverse=True)

    return graph

def zad01(degree_sequence):
    is_graphical, reason = is_graphical_sequence(degree_sequence)
    if is_graphical:
        print(f"Ciąg {degree_sequence} jest graficzny. Budowanie grafu...")
        graph = construct_graph(degree_sequence)
        title = "Graf sekwencji: " + str(degree_sequence)
        visualize_circular(graph, title)
    else:
        print(f"Podany ciąg {degree_sequence} nie jest graficzny. Powód: {reason}")

