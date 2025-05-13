"""
Zadanie 2: Implementacja algorytmu Dijkstry.

Algorytm Dijkstry działa następująco:
1. Inicjalizacja odległości od źródła:
   - Dla wierzchołka źródłowego s: d[s] = 0
   - Dla pozostałych wierzchołków: d[v] = nieskończoność
   - Inicjalizacja tablicy poprzedników: p[v] = None dla wszystkich wierzchołków
2. Tworzenie zbioru S wierzchołków o ustalonych najkrótszych ścieżkach
3. W każdej iteracji:
   - Wybierz wierzchołek u o minimalnej odległości, który nie należy do S
   - Dodaj u do S
   - Zaktualizuj odległości do sąsiadów u (operacja relaksacji)
4. Algorytm kończy się, gdy wszystkie wierzchołki zostaną dodane do S

Struktura grafu:
- Klasa Graph z pliku graph_representation.py implementuje nieskierowany graf ważony
- Graf przechowuje wierzchołki numerowane od 0 do V-1
- Krawędzie są reprezentowane jako pary (u, v), gdzie u < v
- Wagi są przechowywane w słowniku weights, gdzie klucz to krawędź (u, v)
"""

import heapq
from zad1 import zad1

def init(graph, s):
    """
    Inicjalizacja atrybutów d i p dla wierzchołków grafu.
    
    To jest pierwszy krok algorytmu Dijkstry, gdzie:
    - ds[v] przechowuje szacunkową odległość od źródła s do wierzchołka v
    - ps[v] przechowuje poprzednika wierzchołka v na najkrótszej ścieżce z s do v
    
    Args:
        graph: Graf wejściowy (obiekt klasy Graph)
        s: Wierzchołek źródłowy (indeks)
        
    Returns:
        Tuple (ds, ps): 
        - ds: tablica odległości [d₀, d₁, ..., d_{n-1}], gdzie d_i to odległość od s do i
        - ps: tablica poprzedników [p₀, p₁, ..., p_{n-1}], gdzie p_i to poprzednik i na najkrótszej ścieżce
    """
    n = graph.V
    ds = [float('inf')] * n  # Inicjalizacja wszystkich odległości jako nieskończoność
    ps = [None] * n          # Inicjalizacja wszystkich poprzedników jako None
    ds[s] = 0                # Odległość od źródła do samego siebie wynosi 0
    return ds, ps

def relax(u, v, w, ds, ps):
    """
    Relaksacja krawędzi (u, v).
    
    Operacja relaksacji sprawdza, czy możemy znaleźć krótszą ścieżkę do v przechodząc przez u.
    Jeśli aktualna odległość do v jest większa niż odległość do u plus waga krawędzi (u, v),
    to aktualizujemy odległość do v i ustawiamy u jako poprzednika v.
    
    Args:
        u, v: Wierzchołki połączone krawędzią (u, v)
        w: Waga krawędzi (u, v)
        ds: Tablica odległości
        ps: Tablica poprzedników
        
    Returns:
        True jeśli relaksacja zaktualizowała odległość (znaleziono lepszą ścieżkę), 
        False w przeciwnym razie
    """
    if ds[v] > ds[u] + w:
        ds[v] = ds[u] + w
        ps[v] = u
        return True
    return False

def dijkstra(graph, s):
    """
    Algorytm Dijkstry do znajdowania najkrótszych ścieżek z wierzchołka s.
    
    Algorytm używa kolejki priorytetowej, aby efektywnie wybierać wierzchołek 
    o najmniejszej odległości w każdej iteracji. Złożoność czasowa wynosi O((V+E)log V),
    gdzie V to liczba wierzchołków, a E to liczba krawędzi.
    
    Args:
        graph: Graf wejściowy (obiekt klasy Graph)
        s: Wierzchołek źródłowy (indeks)
        
    Returns:
        Tuple (ds, ps): 
        - ds: tablica finalnych odległości od s do wszystkich wierzchołków
        - ps: tablica poprzedników dla odtworzenia najkrótszych ścieżek
    """
    n = graph.V
    ds, ps = init(graph, s)
    
    # Zbiór S wierzchołków o ustalonych najkrótszych ścieżkach (na początku pusty)
    S = set()
    
    # Kolejka priorytetowa - pary (odległość, wierzchołek)
    # heapq automatycznie sortuje według pierwszego elementu krotki (odległości)
    queue = [(0, s)]
    
    while queue and len(S) < n:
        # Wybierz wierzchołek o najmniejszej odległości używając kolejki priorytetowej
        dist_u, u = heapq.heappop(queue)
        
        # Jeśli wierzchołek jest już w zbiorze S, pomiń go (możliwe duplikaty w kolejce)
        if u in S:
            continue
        
        # Dodaj wierzchołek do zbioru S (wierzchołek ma już ustaloną najkrótszą ścieżkę)
        S.add(u)
        
        # Relaksacja wszystkich krawędzi wychodzących z u
        for v in range(n):
            # Sprawdź czy (u, v) jest krawędzią w grafie
            # W grafie nieskierowanym krawędzie są przechowywane jako (min(u,v), max(u,v))
            edge = (min(u, v), max(u, v))
            
            # Relaksuj tylko jeśli krawędź istnieje i wierzchołek docelowy nie jest w S
            if edge in graph.get_weights() and v not in S:
                weight = graph.get_weight(u, v)
                
                # Jeśli znaleziono lepszą ścieżkę, dodaj wierzchołek do kolejki z nową odległością
                if relax(u, v, weight, ds, ps):
                    heapq.heappush(queue, (ds[v], v))
    
    return ds, ps

def get_path(ps, s, v):
    """
    Odzyskuje ścieżkę z wierzchołka s do v na podstawie tablicy poprzedników.
    
    Funkcja ta rekonstruuje najkrótszą ścieżkę od źródła s do wierzchołka v
    przechodząc wstecz przez tablicę poprzedników ps. Ścieżka jest zwracana
    jako lista wierzchołków w kolejności od s do v.
    
    Args:
        ps: Tablica poprzedników (wynik algorytmu Dijkstry)
        s: Wierzchołek źródłowy (indeks)
        v: Wierzchołek docelowy (indeks)
        
    Returns:
        Lista wierzchołków tworzących najkrótszą ścieżkę od s do v,
        lub None jeśli nie ma ścieżki (wierzchołek v jest niedostępny z s)
    """
    path = []
    current = v
    
    # Przechodzimy wstecz od wierzchołka v do s używając tablicy poprzedników
    while current is not None:
        path.append(current)
        current = ps[current]  # Przejście do poprzednika
    
    # Odwróć ścieżkę, aby była w kolejności od s do v
    path.reverse()
    
    # Sprawdź czy ścieżka zaczyna się od wierzchołka źródłowego s
    # Jeśli nie, oznacza to, że nie ma ścieżki od s do v
    if path and path[0] == s:
        return path
    return None  # Nie ma ścieżki z s do v

def zad2(graph=None, start_vertex=0):
    """
    Znajduje najkrótsze ścieżki od danego wierzchołka do pozostałych wierzchołków
    za pomocą algorytmu Dijkstry.
    
    Funkcja ta:
    1. Generuje losowy graf, jeśli nie dostarczono grafu
    2. Uruchamia algorytm Dijkstry z podanego wierzchołka startowego
    3. Wyświetla wyniki (odległości i ścieżki)
    4. Zwraca wynikowe tablice odległości i poprzedników
    
    Args:
        graph: Graf wejściowy (obiekt klasy Graph, jeśli None, zostanie wygenerowany losowy graf)
        start_vertex: Wierzchołek startowy (indeks)
        
    Returns:
        Tuple (ds, ps, graph): 
        - ds: tablica finalnych odległości od start_vertex do wszystkich wierzchołków
        - ps: tablica poprzedników dla odtworzenia najkrótszych ścieżek
        - graph: używany graf (wygenerowany lub przekazany jako argument)
    """
    if graph is None:
        # Generuj losowy graf z 12 wierzchołkami i wagami z zakresu [1, 10]
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
            # Przekształć ścieżkę na string dla czytelności
            path_str = " - ".join(str(node) for node in path)
            print(f"d({v}) = {ds[v]} ==> [{path_str}]")
        else:
            print(f"d({v}) = inf ==> (brak ścieżki)")
    
    return ds, ps, graph

if __name__ == "__main__":
    # Generuj graf i uruchom algorytm Dijkstry z wierzchołka 0
    ds, ps, graph = zad2() 