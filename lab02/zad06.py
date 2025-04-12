from graph_representation import Graph
from lab02.graph_visualization import visualize_circular


def is_hamiltonian_util(graph, path, visited, start):
    """Rekurencyjna funkcja do znajdowania cyklu Hamiltona."""
    if len(path) == graph.V:
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

def zad06(vertices, edges):
    graph = Graph(vertices)


    for u, v in edges:
        graph.add_edge(u, v)

    hamiltonian_cycle = find_hamiltonian_cycle(graph)
    if hamiltonian_cycle:
        print("Znaleziono cykl Hamiltona:", " -> ".join(map(str, hamiltonian_cycle)))
        visualize_circular(graph)
    else:
        print("Graf nie zawiera cyklu Hamiltona.")