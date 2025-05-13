from graph_representation import Graph
from lab02.graph_visualization import visualize_circular


def is_graphical_sequence(sequence):
    # Sprawdzenie ilości nieparzystych wierzchołków
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

        # Sprawdzenie czy można skonstruować graf
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

    # Stworzenie krotek i sortowanie
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

# Zadanie 1
# Napisać program do sprawdzania, czy dana sekwencja liczb naturalnych
# jest ciągiem graficznym, i do konstruowania grafu prostego o stopniach
# wierzchołków zadanych przez ciąg graficzny
if __name__ == "__main__":
    # Przykładowe sekwencje liczb naturalnych
    degree_sequences = [
        [1,3,2,3,2,4,1],
        [1,3,3,4,2,3,1],
        [1,3,3,7,2,3,1],
        [2,2,6,4,4,6,6]
    ]

    # Dla każdej sekwencji sprawdzamy czy jest ona ciągiem graficznym
    # Następnie jeżeli jest, to konstruujemy graf na tej podstawie
    # Argumentem wywołania jest ciąg graficzny
    for degree_sequence in degree_sequences:
        zad01(degree_sequence)