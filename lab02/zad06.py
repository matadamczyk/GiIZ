from graph_representation import Graph
from lab02.graph_visualization import visualize_circular


def is_hamiltonian_util(graph, path, visited, start):
    """Rekurencyjna funkcja do znajdowania cyklu Hamiltona."""
    if len(path) == graph.V:
        # Sprawdzamy, czy istnieje krawędź łącząca ostatni wierzchołek ze startowym
        if start in graph.get_adjacency_list()[path[-1]]:
            path.append(start)
            return True
        else:
            return False

    for neighbor in graph.get_adjacency_list()[path[-1]]:
        if not visited[neighbor]:
            visited[neighbor] = True
            path.append(neighbor)

            if is_hamiltonian_util(graph, path, visited, start):
                return True

            visited[neighbor] = False
            path.pop()

    return False

def find_hamiltonian_cycle(graph):
    """Sprawdza, czy graf zawiera cykl Hamiltona, zwracając go jeśli istnieje."""
    for start in range(graph.V):
        path = [start]
        visited = [False] * graph.V
        visited[start] = True

        if is_hamiltonian_util(graph, path, visited, start):
            return path

    return None

# Przykładowe użycie:
if __name__ == "__main__":
    graph = Graph(8)
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    for u, v in edges:
        graph.add_edge(u, v)

    hamiltonian_cycle = find_hamiltonian_cycle(graph)
    if hamiltonian_cycle:
        print("Znaleziono cykl Hamiltona:", " -> ".join(map(str, hamiltonian_cycle)))
        visualize_circular(graph)
    else:
        print("Graf nie zawiera cyklu Hamiltona.")

    graph = Graph(6)
    edges = [(0,2), (0,4), (0,5), (1,3), (1,4), (1,5), (2,4), (3,4)]

    for u, v in edges:
        graph.add_edge(u, v)

    hamiltonian_cycle = find_hamiltonian_cycle(graph)
    if hamiltonian_cycle:
        print("Znaleziono cykl Hamiltona:", " -> ".join(map(str, hamiltonian_cycle)))
        visualize_circular(graph)
    else:
        print("Graf nie zawiera cyklu Hamiltona.")