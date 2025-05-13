"""
Zadanie 4: Wyznaczanie centrum grafu i centrum minimax.

Obliczenia te bazują na macierzy odległości między wszystkimi parami wierzchołków.

Centrum grafu (mediana):
- Jest to wierzchołek v, dla którego suma odległości do wszystkich pozostałych 
  wierzchołków jest minimalna: min_{v} sum_{u} d(v, u)
- Reprezentuje "środek" grafu pod względem sumy odległości
- Optymalne miejsce do umieszczenia pojedynczego obiektu, który ma minimalizować
  sumaryczną odległość do wszystkich innych punktów

Centrum minimax (centrum):
- Jest to wierzchołek v, dla którego maksymalna odległość do najdalszego wierzchołka 
  jest minimalna: min_{v} max_{u} d(v, u)
- Reprezentuje wierzchołek o najmniejszej "najgorszej" odległości
- Optymalne miejsce do umieszczenia usługi, która ma minimalizować maksymalny czas
  dotarcia do dowolnego punktu w sieci
"""

from zad1 import zad1
from zad3 import compute_distance_matrix

def find_graph_center(distance_matrix):
    """
    Znajduje centrum grafu - wierzchołek, którego suma odległości do pozostałych
    wierzchołków jest minimalna.
    
    Algorytm:
    1. Dla każdego wierzchołka v obliczamy sumę odległości do wszystkich innych wierzchołków
    2. Wybieramy wierzchołek z minimalną sumą
    
    Złożoność: O(V²), gdzie V to liczba wierzchołków.
    
    Args:
        distance_matrix: Macierz odległości, gdzie distance_matrix[i][j] to najkrótsza
                         odległość między wierzchołkami i oraz j
        
    Returns:
        Tuple (center_vertex, min_sum): 
        - center_vertex: indeks wierzchołka będącego centrum grafu
        - min_sum: minimalna suma odległości do wszystkich innych wierzchołków
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
    
    Algorytm:
    1. Dla każdego wierzchołka v znajdujemy maksymalną odległość do dowolnego innego wierzchołka
    2. Wybieramy wierzchołek z minimalną wartością tego maksimum
    
    Złożoność: O(V²), gdzie V to liczba wierzchołków.
    
    Args:
        distance_matrix: Macierz odległości, gdzie distance_matrix[i][j] to najkrótsza
                         odległość między wierzchołkami i oraz j
        
    Returns:
        Tuple (center_vertex, min_max_distance): 
        - center_vertex: indeks wierzchołka będącego centrum minimax
        - min_max_distance: minimalna wartość maksymalnej odległości do dowolnego wierzchołka
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
    
    Funkcja ta:
    1. Generuje losowy graf i/lub oblicza macierz odległości, jeśli nie zostały dostarczone
    2. Znajduje centrum grafu (medianę) - wierzchołek o minimalnej sumie odległości
    3. Znajduje centrum minimax (centrum) - wierzchołek o minimalnej maksymalnej odległości
    4. Wyświetla wyniki obliczeń
    
    Zastosowania:
    - Centrum grafu: optymalne umiejscowienie magazynu minimalizującego łączny koszt transportu
    - Centrum minimax: optymalna lokalizacja szpitala minimalizująca maksymalny czas dojazdu
    
    Args:
        graph: Graf wejściowy (obiekt klasy Graph, jeśli None i distance_matrix jest None, 
               zostanie wygenerowany losowy graf)
        distance_matrix: Macierz odległości (jeśli None, zostanie obliczona)
        
    Returns:
        Tuple (center, minimax_center): 
        - center: indeks wierzchołka będącego centrum grafu (medianą)
        - minimax_center: indeks wierzchołka będącego centrum minimax (centrum)
    """
    if distance_matrix is None:
        if graph is None:
            # Generuj losowy graf z 12 wierzchołkami i wagami z zakresu [1, 10]
            graph = zad1(12, 1, 10)
        # Oblicz macierz odległości używając algorytmu z zadania 3
        distance_matrix = compute_distance_matrix(graph)
    
    # Znajdź centrum grafu (medianę)
    center, min_sum = find_graph_center(distance_matrix)
    print(f"Centrum grafu (mediana) = {center} (suma odległości: {min_sum})")
    
    # Znajdź centrum minimax (centrum)
    minimax_center, min_max_distance = find_minimax_center(distance_matrix)
    print(f"Centrum minimax (centrum) = {minimax_center} (odległość od najdalszego: {min_max_distance})")
    
    return center, minimax_center

if __name__ == "__main__":
    # Generuj graf i znajdź centra
    center, minimax_center = zad4() 