"""
Zadanie 3: Wyznaczanie macierzy odległości między wszystkimi parami wierzchołków.
"""

from zad1 import zad1
from zad2 import dijkstra

def compute_distance_matrix(graph):
    """
    Wyznacza macierz odległości dla grafu.
    
    Args:
        graph: Graf wejściowy
        
    Returns:
        Macierz odległości (lista list)
    """
    n = graph.V
    distance_matrix = [[0] * n for _ in range(n)]
    
    # Dla każdego wierzchołka jako źródłowego
    for s in range(n):
        # Uruchom algorytm Dijkstry
        ds, ps = dijkstra(graph, s)
        
        # Zapisz odległości w macierzy
        for v in range(n):
            distance_matrix[s][v] = ds[v]
    
    return distance_matrix

def zad3(graph=None):
    """
    Wyznacza i wyświetla macierz odległości dla grafu.
    
    Args:
        graph: Graf wejściowy (jeśli None, zostanie wygenerowany)
        
    Returns:
        Macierz odległości
    """
    if graph is None:
        graph = zad1(12, 1, 10)
    
    # Oblicz macierz odległości
    distance_matrix = compute_distance_matrix(graph)
    
    # Wyświetl macierz
    print("Macierz odległości:")
    for row in distance_matrix:
        print(" ".join(str(dist) for dist in row))
    
    return distance_matrix

if __name__ == "__main__":
    # Generuj graf i oblicz macierz odległości
    distance_matrix = zad3() 