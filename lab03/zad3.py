"""
Zadanie 3: Wyznaczanie macierzy odległości między wszystkimi parami wierzchołków.

Macierz odległości D to macierz n×n, gdzie
D[i][j] oznacza najkrótszą odległość między wierzchołkami i oraz j.

Algorytm wykorzystuje podejście naiwne (złożoność O(V³ log V)):
1. Dla każdego wierzchołka s w grafie wykonujemy algorytm Dijkstry
2. Zapisujemy odległości z wierzchołka s do wszystkich innych w odpowiednim wierszu macierzy
3. W rezultacie otrzymujemy pełną macierz odległości

Macierz odległości ma wiele zastosowań, m.in.:
- Znajdowanie centrów grafu
- Analizowanie dostępności wierzchołków
- Obliczanie średniego dystansu w grafie
"""

from zad1 import zad1
from zad2 import dijkstra

def compute_distance_matrix(graph):
    """
    Wyznacza macierz odległości dla grafu.
    
    Dla każdego wierzchołka źródłowego s, funkcja uruchamia algorytm Dijkstry
    i zapisuje odległości od s do wszystkich pozostałych wierzchołków w wierszu
    macierzy odległości. Wynikowa macierz D ma właściwość, że D[i][j] to najkrótsza
    odległość między wierzchołkami i oraz j.
    
    Złożoność: O(V³ log V), gdzie V to liczba wierzchołków, ponieważ:
    - Wykonujemy V razy algorytm Dijkstry
    - Każde wykonanie Dijkstry ma złożoność O(V² log V) dla implementacji z kolejką priorytetową
    
    Args:
        graph: Graf wejściowy (obiekt klasy Graph)
        
    Returns:
        Macierz odległości (lista list), gdzie macierz[i][j] to najkrótsza odległość 
        z wierzchołka i do wierzchołka j
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
    
    Funkcja ta:
    1. Generuje losowy graf, jeśli nie dostarczono grafu
    2. Oblicza macierz odległości używając algorytmu Dijkstry dla każdego wierzchołka
    3. Wyświetla wynikową macierz odległości w formie tekstowej
    
    Args:
        graph: Graf wejściowy (obiekt klasy Graph, jeśli None, zostanie wygenerowany losowy graf)
        
    Returns:
        Macierz odległości - lista list zawierająca najkrótsze odległości między każdą parą wierzchołków
    """
    if graph is None:
        # Generuj losowy graf z 12 wierzchołkami i wagami z zakresu [1, 10]
        graph = zad1(12, 1, 10)
    
    # Oblicz macierz odległości
    distance_matrix = compute_distance_matrix(graph)
    
    # Wyświetl macierz w formacie tekstowym
    print("Macierz odległości:")
    for row in distance_matrix:
        print(" ".join(str(dist) for dist in row))
    
    return distance_matrix

if __name__ == "__main__":
    # Generuj graf i oblicz macierz odległości
    distance_matrix = zad3() 