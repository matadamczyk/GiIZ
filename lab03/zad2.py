"""
Zadanie 2: Implementacja algorytmu Dijkstry.
"""

import heapq
from zad1 import zad1

def init(graph, s):
    """
    Inicjalizacja atrybutów d i p dla wierzchołków grafu.
    
    Args:
        graph: Graf wejściowy
        s: Wierzchołek źródłowy
        
    Returns:
        Tuple (ds, ps): ds - tablica odległości, ps - tablica poprzedników
    """
    n = graph.V
    ds = [float('inf')] * n
    ps = [None] * n
    ds[s] = 0
    return ds, ps

def relax(u, v, w, ds, ps):
    """
    Relaksacja krawędzi (u, v).
    
    Args:
        u, v: Wierzchołki połączone krawędzią (u, v)
        w: Waga krawędzi (u, v)
        ds: Tablica odległości
        ps: Tablica poprzedników
        
    Returns:
        True jeśli relaksacja zaktualizowała odległość, False w przeciwnym razie
    """
    if ds[v] > ds[u] + w:
        ds[v] = ds[u] + w
        ps[v] = u
        return True
    return False

def dijkstra(graph, s):
    """
    Algorytm Dijkstry do znajdowania najkrótszych ścieżek z wierzchołka s.
    
    Args:
        graph: Graf wejściowy
        s: Wierzchołek źródłowy
        
    Returns:
        Tuple (ds, ps): ds - tablica odległości, ps - tablica poprzedników
    """
    n = graph.V
    ds, ps = init(graph, s)
    
    # Zbiór gotowych wierzchołków (na początku pusty)
    S = set()
    
    # Kolejka priorytetowa - (odległość, wierzchołek)
    queue = [(0, s)]
    
    while queue and len(S) < n:
        # Wybierz wierzchołek o najmniejszej odległości
        dist_u, u = heapq.heappop(queue)
        
        # Jeśli wierzchołek jest już gotowy, pomiń go
        if u in S:
            continue
        
        # Dodaj wierzchołek do zbioru gotowych
        S.add(u)
        
        # Relaksacja sąsiadów
        for v in range(n):
            # Sprawdź czy (u, v) jest krawędzią
            edge = (min(u, v), max(u, v))
            if edge in graph.get_weights() and v not in S:
                weight = graph.get_weight(u, v)
                if relax(u, v, weight, ds, ps):
                    heapq.heappush(queue, (ds[v], v))
    
    return ds, ps

def get_path(ps, s, v):
    """
    Odzyskuje ścieżkę z wierzchołka s do v na podstawie tablicy poprzedników.
    
    Args:
        ps: Tablica poprzedników
        s: Wierzchołek źródłowy
        v: Wierzchołek docelowy
        
    Returns:
        Lista wierzchołków tworzących ścieżkę od s do v
    """
    path = []
    current = v
    
    while current is not None:
        path.append(current)
        current = ps[current]
    
    path.reverse()
    
    # Sprawdź czy ścieżka zaczyna się od wierzchołka źródłowego
    if path and path[0] == s:
        return path
    return None  # Nie ma ścieżki

def zad2(graph=None, start_vertex=0):
    """
    Znajduje najkrótsze ścieżki od danego wierzchołka do pozostałych wierzchołków
    za pomocą algorytmu Dijkstry.
    
    Args:
        graph: Graf wejściowy (jeśli None, zostanie wygenerowany)
        start_vertex: Wierzchołek startowy
        
    Returns:
        Tuple (ds, ps, graph): ds - tablica odległości, ps - tablica poprzedników, graph - używany graf
    """
    if graph is None:
        graph = zad1(12, 1, 10)
    
    # Sprawdź poprawność wierzchołka startowego
    if start_vertex < 0 or start_vertex >= graph.V:
        raise ValueError(f"Wierzchołek startowy musi być w zakresie 0-{graph.V-1}")
    
    # Uruchom algorytm Dijkstry
    ds, ps = dijkstra(graph, start_vertex)
    
    # Wyświetl wyniki
    print(f"START: s = {start_vertex}")
    for v in range(graph.V):
        path = get_path(ps, start_vertex, v)
        if path:
            path_str = " - ".join(str(node) for node in path)
            print(f"d({v}) = {ds[v]} ==> [{path_str}]")
        else:
            print(f"d({v}) = inf ==> (brak ścieżki)")
    
    return ds, ps, graph

if __name__ == "__main__":
    # Generuj graf i uruchom algorytm Dijkstry z wierzchołka 0
    ds, ps, graph = zad2() 