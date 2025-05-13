import random
from graph_representation import Graph
from graph_visualization import visualize_circular
from zad01 import is_graphical_sequence, construct_graph

def randomize_graph(graph, iterations=10):
    edges = graph.get_edges()
    num_edges = len(edges)

    for _ in range(iterations):
        if num_edges < 2:
            break

        while True:
            (a, b), (c, d) = random.sample(edges, 2)

            if (a, d) not in edges and (c, b) not in edges and a != d and c != b:
                edges.remove((a, b))
                edges.remove((c, d))
                edges.append((a, d))
                edges.append((c, b))
                print(f"Zamieniono krawędzie: ({a}, {b}) i ({c}, {d}) na ({a}, {d}) i ({c}, {b})")
                break

    randomized_graph = Graph(graph.V)
    for u, v in edges:
        randomized_graph.add_edge(u, v)

    return randomized_graph

def zad02(degree_sequence):
    is_graphical, reason = is_graphical_sequence(degree_sequence)
    if is_graphical:
        print("Ciąg jest graficzny. Budowanie i randomizacja grafu...")
        graph = construct_graph(degree_sequence)
        visualize_circular(graph, title="Oryginalny graf")
        graph = randomize_graph(graph, iterations=1)
        visualize_circular(graph, title=f"Randomizacja")
    else:
        print(f"Podany ciąg nie jest graficzny. Powód: {reason}")

# Zadanie 2
# Napisać program do randomizacji grafów prostych o zadanych stopniach wierzchołków.
# Do tego celu wielokrotnie powtórzyć operację zamieniającą losowo wybraną parę
# krawędzi: ab i cd na parę ad i bc

if __name__ == "__main__":
    degree_sequence = [1,3,2,3,2,4,1]
    zad02(degree_sequence)