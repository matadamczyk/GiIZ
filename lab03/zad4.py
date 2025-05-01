"""
Zadanie 4: Wyznaczanie centrum grafu i centrum minimax.
"""

from lab03.zad1 import zad1
from lab03.zad3 import compute_distance_matrix

def find_graph_center(distance_matrix):
    """
    Znajduje centrum grafu - wierzchołek, którego suma odległości do pozostałych
    wierzchołków jest minimalna.
    
    Args:
        distance_matrix: Macierz odległości
        
    Returns:
        Tuple (center_vertex, min_sum): centrum grafu i suma odległości
    """
    n = len(distance_matrix)
    min_sum = float('inf')
    center_vertex = None
    
    for v in range(n):
        # Oblicz sumę odległości od wierzchołka v do wszystkich innych
        distance_sum = sum(distance_matrix[v])
        
        # Jeśli znaleziono mniejszą sumę, zaktualizuj centrum
        if distance_sum < min_sum:
            min_sum = distance_sum
            center_vertex = v
    
    return center_vertex, min_sum

def find_minimax_center(distance_matrix):
    """
    Znajduje centrum minimax grafu - wierzchołek, którego odległość do najdalszego
    wierzchołka jest minimalna.
    
    Args:
        distance_matrix: Macierz odległości
        
    Returns:
        Tuple (center_vertex, min_max_distance): centrum minimax i maksymalna odległość
    """
    n = len(distance_matrix)
    min_max_distance = float('inf')
    center_vertex = None
    
    for v in range(n):
        # Znajdź maksymalną odległość od wierzchołka v do innego wierzchołka
        max_distance = max(distance_matrix[v])
        
        # Jeśli znaleziono mniejsze maksimum, zaktualizuj centrum minimax
        if max_distance < min_max_distance:
            min_max_distance = max_distance
            center_vertex = v
    
    return center_vertex, min_max_distance

def zad4(graph=None, distance_matrix=None):
    """
    Wyznacza centrum grafu i centrum minimax.
    
    Args:
        graph: Graf wejściowy (jeśli None i distance_matrix jest None, zostanie wygenerowany)
        distance_matrix: Macierz odległości (jeśli None, zostanie obliczona)
        
    Returns:
        Tuple (center, minimax_center): centrum grafu i centrum minimax
    """
    if distance_matrix is None:
        if graph is None:
            graph = zad1(12, 1, 10)
        distance_matrix = compute_distance_matrix(graph)
    
    # Znajdź centrum grafu
    center, min_sum = find_graph_center(distance_matrix)
    print(f"Centrum = {center} (suma odległości: {min_sum})")
    
    # Znajdź centrum minimax
    minimax_center, min_max_distance = find_minimax_center(distance_matrix)
    print(f"Centrum minimax = {minimax_center} (odległość od najdalszego: {min_max_distance})")
    
    return center, minimax_center

if __name__ == "__main__":
    # Generuj graf i znajdź centra
    center, minimax_center = zad4() 