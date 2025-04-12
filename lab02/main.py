from lab02.zad01 import is_graphical_sequence, construct_graph, zad01
from lab02.zad02 import randomize_graph, zad02
from lab02.zad03 import is_graph_connected, find_largest_connected_component, zad03
from lab02.zad04 import generate_eulerian_graph, find_eulerian_cycle, zad04
from lab02.zad05 import generate_k_regular_graph, zad05
from lab02.zad06 import zad06

print('\n\n\nzad 1')
# Zadanie 1
# Napisać program do sprawdzania, czy dana sekwencja liczb naturalnych
# jest ciągiem graficznym, i do konstruowania grafu prostego o stopniach
# wierzchołków zadanych przez ciąg graficzny

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

print('\n\n\nzad 2')
# Zadanie 2
# Napisać program do randomizacji grafów prostych o zadanych stopniach wierzchołków.
# Do tego celu wielokrotnie powtórzyć operację zamieniającą losowo wybraną parę
# krawędzi: ab i cd na parę ad i bc

degree_sequence = [1,3,2,3,2,4,1]
zad02(degree_sequence)

print('\n\n\nzad 3')
# Zadanie 3
# Napisać program do znajdowania największej spójnej składowej na grafie.
# Przykładowe użycie:

degree_sequence = [3, 3, 2, 2, 1, 1]
zad03(degree_sequence)

print('\n\n\nzad 4')
# Zadanie 4
# Używając powyższych programów napisać program do
# tworzenia losowego grafu eulerowskiego i
# znajdowania na nim cyklu Eulera.

num_vertices = 6  # Liczba wierzchołków
zad04(num_vertices)

print('\n\n\nzad 5')
# Zadanie 5
# Napisać program do generowania losowych grafów k-regularnych.
n, k = 8, 5  # Liczba wierzchołków i stopień k
zad05(n,k)

print('\n\n\nzad 6')
# Zadanie 6
# Napisać program do sprawdzania (dla małych grafów),
# czy graf jest hamiltonowski.
vertices = 8
edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

zad06(vertices, edges)

vertices = 6
edges = [(0,2), (0,4), (0,5), (1,3), (1,4), (1,5), (2,4), (3,4)]
zad06(vertices, edges)