"""
Implementacja algorytmu Johnsona do znajdowania najkrótszych ścieżek między wszystkimi parami wierzchołków w grafie skierowanym.
Algorytm może obsługiwać krawędzie o ujemnych wagach, o ile w grafie nie ma cyklu o ujemnej sumie wag.
"""

from lab04.digraph_representation import DiGraph
from lab04.bellman_ford import bellman_ford, init, relax
import heapq

def add_s(digraph):
    """
    Dodaje nowy wierzchołek s połączony krawędziami o wadze 0 z wszystkimi innymi wierzchołkami.
    
    Args:
        digraph: DiGraph - graf skierowany
        
    Returns:
        DiGraph: Poszerzony graf
    """
    n = digraph.V
    G_prime = DiGraph(n + 1)
    
    # Kopiuj istniejące krawędzie
    for u, v in digraph.get_edges():
        weight = digraph.get_weight(u, v)
        G_prime.add_edge(u, v, weight)
    
    # Dodaj krawędzie od s do wszystkich wierzchołków
    s = n
    for v in range(n):
        G_prime.add_edge(s, v, 0)
    
    return G_prime

def dijkstra(digraph, s, h=None):
    """
    Algorytm Dijkstry do znajdowania najkrótszych ścieżek od wierzchołka s.
    Opcjonalnie używa potencjałów wierzchołków h do przeliczenia wag krawędzi.
    
    Args:
        digraph: DiGraph - graf skierowany
        s: Wierzchołek źródłowy
        h: Tablica potencjałów wierzchołków (opcjonalna)
        
    Returns:
        Tuple (ds, ps): ds - tablica odległości, ps - tablica poprzedników
    """
    n = digraph.V
    ds, ps = init(digraph, s)
    
    # Zbiór gotowych wierzchołków
    S = set()
    
    # Kolejka priorytetowa - (odległość, wierzchołek)
    queue = [(0, s)]
    
    while queue and len(S) < n:
        # Wybierz wierzchołek o najmniejszej odległości
        dist_u, u = heapq.heappop(queue)
        
        # Jeśli wierzchołek jest już przetworzony, pomiń go
        if u in S:
            continue
        
        # Dodaj wierzchołek do zbioru przetworzonych
        S.add(u)
        
        # Relaksacja sąsiadów
        for v in digraph.get_out_neighbors(u):
            if v not in S:
                # Pobierz wagę krawędzi
                w = digraph.get_weight(u, v)
                
                # Jeśli używamy potencjałów, przelicz wagę
                if h is not None:
                    w = w + h[u] - h[v]
                
                # Relaksacja
                if ds[v] > ds[u] + w:
                    ds[v] = ds[u] + w
                    ps[v] = u
                    heapq.heappush(queue, (ds[v], v))
    
    return ds, ps

def johnson(digraph):
    """
    Algorytm Johnsona do znajdowania najkrótszych ścieżek między wszystkimi parami wierzchołków.
    
    Args:
        digraph: DiGraph - graf skierowany z wagami
        
    Returns:
        Macierz odległości lub None, jeśli graf zawiera cykl o ujemnej sumie wag
    """
    # Krok 1: Dodaj nowy wierzchołek s
    G_prime = add_s(digraph)
    
    # Krok 2: Uruchom Bellmana-Forda od s
    ds, ps, has_negative_cycle = bellman_ford(G_prime, G_prime.V - 1)
    
    # Jeśli wykryto cykl o ujemnej sumie wag, zakończ
    if has_negative_cycle:
        return None
    
    # Krok 3: Oblicz potencjały wierzchołków
    n = digraph.V
    h = ds[:n]  # Potencjały to odległości od s do wszystkich wierzchołków
    
    # Krok 4: Przelicz wagi krawędzi
    # Tworzymy nową macierz wag
    wb = {}
    for u, v in digraph.get_edges():
        w = digraph.get_weight(u, v)
        wb[(u, v)] = w + h[u] - h[v]
    
    # Krok 5: Dla każdego wierzchołka uruchom Dijkstrę
    D = [[float('inf') for _ in range(n)] for _ in range(n)]
    
    for u in range(n):
        # Stwórz kopię grafu z przeskalowanymi wagami
        G_hat = DiGraph(n)
        for edge_u, edge_v in digraph.get_edges():
            G_hat.add_edge(edge_u, edge_v, wb[(edge_u, edge_v)])
        
        # Uruchom Dijkstrę od u
        d_hat_u, _ = dijkstra(G_hat, u)
        
        # Przelicz rzeczywiste odległości
        for v in range(n):
            if d_hat_u[v] != float('inf'):
                D[u][v] = d_hat_u[v] - h[u] + h[v]
    
    return D

def johnson_with_paths(digraph):
    """
    Algorytm Johnsona do znajdowania najkrótszych ścieżek między wszystkimi parami wierzchołków
    wraz z informacją o ścieżkach.
    
    Args:
        digraph: DiGraph - graf skierowany z wagami
        
    Returns:
        Tuple (D, P): D - macierz odległości, P - macierz poprzedników
            lub (None, None), jeśli graf zawiera cykl o ujemnej sumie wag
    """
    # Krok 1: Dodaj nowy wierzchołek s
    G_prime = add_s(digraph)
    
    # Krok 2: Uruchom Bellmana-Forda od s
    ds, ps, has_negative_cycle = bellman_ford(G_prime, G_prime.V - 1)
    
    # Jeśli wykryto cykl o ujemnej sumie wag, zakończ
    if has_negative_cycle:
        return None, None
    
    # Krok 3: Oblicz potencjały wierzchołków
    n = digraph.V
    h = ds[:n]  # Potencjały to odległości od s do wszystkich wierzchołków
    
    # Krok 4: Przelicz wagi krawędzi
    # Tworzymy nową macierz wag
    wb = {}
    for u, v in digraph.get_edges():
        w = digraph.get_weight(u, v)
        wb[(u, v)] = w + h[u] - h[v]
    
    # Krok 5: Dla każdego wierzchołka uruchom Dijkstrę
    D = [[float('inf') for _ in range(n)] for _ in range(n)]
    P = [[None for _ in range(n)] for _ in range(n)]
    
    for u in range(n):
        # Stwórz kopię grafu z przeskalowanymi wagami
        G_hat = DiGraph(n)
        for edge_u, edge_v in digraph.get_edges():
            G_hat.add_edge(edge_u, edge_v, wb[(edge_u, edge_v)])
        
        # Uruchom Dijkstrę od u
        d_hat_u, p_hat_u = dijkstra(G_hat, u)
        
        # Przelicz rzeczywiste odległości i zapisz poprzedników
        for v in range(n):
            if d_hat_u[v] != float('inf'):
                D[u][v] = d_hat_u[v] - h[u] + h[v]
                P[u][v] = p_hat_u[v]
    
    return D, P

def get_path_from_predecessors(P, u, v):
    """
    Odtwarza ścieżkę od u do v na podstawie macierzy poprzedników.
    
    Args:
        P: Macierz poprzedników
        u: Wierzchołek źródłowy
        v: Wierzchołek docelowy
        
    Returns:
        Lista wierzchołków tworzących ścieżkę od u do v lub None, jeśli ścieżka nie istnieje
    """
    if u == v:
        return [u]
    
    if P[u][v] is None:
        return None
    
    path = []
    current = v
    
    while current != u:
        path.append(current)
        current = P[u][current]
        
        # Jeśli nie ma poprzednika, ścieżka nie istnieje
        if current is None:
            return None
    
    path.append(u)
    path.reverse()
    
    return path 