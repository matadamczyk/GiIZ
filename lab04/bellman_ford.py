"""
Implementacja algorytmu Bellmana-Forda do znajdowania najkrótszych ścieżek w grafie skierowanym.
Ten algorytm może obsługiwać krawędzie o ujemnych wagach i wykrywać cykle o ujemnej sumie wag.
"""

from lab04.digraph_representation import DiGraph

def init(digraph, s):
    """
    Inicjalizuje atrybuty odległości i poprzedników dla wierzchołków.
    
    Args:
        digraph: DiGraph - graf skierowany
        s: Wierzchołek źródłowy
        
    Returns:
        Tuple (ds, ps): ds - tablica odległości, ps - tablica poprzedników
    """
    n = digraph.V
    ds = [float('inf')] * n  # Odległości
    ps = [None] * n  # Poprzednicy
    ds[s] = 0  # Odległość od źródła do źródła wynosi 0
    
    return ds, ps

def relax(u, v, w, ds, ps):
    """
    Relaksacja krawędzi (u, v) o wadze w.
    
    Args:
        u, v: Wierzchołki końcowe krawędzi
        w: Waga krawędzi
        ds: Tablica odległości
        ps: Tablica poprzedników
        
    Returns:
        bool: True jeśli relaksacja zmniejszyła odległość do v, False w przeciwnym razie
    """
    if ds[v] > ds[u] + w:
        ds[v] = ds[u] + w
        ps[v] = u
        return True
    return False

def bellman_ford(digraph, s):
    """
    Algorytm Bellmana-Forda do znajdowania najkrótszych ścieżek od wierzchołka s.
    
    Args:
        digraph: DiGraph - graf skierowany z wagami
        s: Wierzchołek źródłowy
        
    Returns:
        Tuple (ds, ps, has_negative_cycle): 
            ds - tablica odległości
            ps - tablica poprzedników
            has_negative_cycle - czy wykryto cykl o ujemnej sumie wag osiągalny z s
    """
    # Inicjalizacja
    n = digraph.V
    ds, ps = init(digraph, s)
    
    # Relaksacja każdej krawędzi n-1 razy
    for i in range(n - 1):
        for u, v in digraph.get_edges():
            w = digraph.get_weight(u, v)
            relax(u, v, w, ds, ps)
    
    # Sprawdzenie, czy istnieje cykl o ujemnej sumie wag
    for u, v in digraph.get_edges():
        w = digraph.get_weight(u, v)
        if ds[v] > ds[u] + w:
            return ds, ps, True  # Znaleziono cykl o ujemnej sumie wag
    
    return ds, ps, False

def get_path(ps, s, v):
    """
    Odtwarza ścieżkę od wierzchołka s do v na podstawie tablicy poprzedników.
    
    Args:
        ps: Tablica poprzedników
        s: Wierzchołek źródłowy
        v: Wierzchołek docelowy
        
    Returns:
        Lista wierzchołków tworzących ścieżkę od s do v lub None, jeśli ścieżka nie istnieje
    """
    if v == s:
        return [s]
    
    if ps[v] is None:
        return None
    
    path = get_path(ps, s, ps[v])
    if path:
        path.append(v)
        return path
    
    return None

def has_negative_cycle(digraph):
    """
    Sprawdza, czy digraf zawiera cykl o ujemnej sumie wag.
    
    Args:
        digraph: DiGraph - graf skierowany z wagami
        
    Returns:
        bool: True jeśli istnieje cykl o ujemnej sumie wag, False w przeciwnym razie
    """
    # Dodaj dodatkowy wierzchołek s połączony z wszystkimi innymi
    n = digraph.V
    extended_digraph = DiGraph(n + 1)
    
    # Kopiuj wszystkie istniejące krawędzie
    for u, v in digraph.get_edges():
        weight = digraph.get_weight(u, v)
        extended_digraph.add_edge(u, v, weight)
    
    # Dodaj krawędzie od s (nowy wierzchołek n) do wszystkich innych
    s = n
    for v in range(n):
        extended_digraph.add_edge(s, v, 0)
    
    # Uruchom Bellmana-Forda od s
    _, _, has_cycle = bellman_ford(extended_digraph, s)
    
    return has_cycle

def find_negative_cycle(digraph):
    """
    Znajduje przykładowy cykl o ujemnej sumie wag w grafie.
    
    Args:
        digraph: DiGraph - graf skierowany z wagami
        
    Returns:
        Lista wierzchołków tworzących cykl o ujemnej sumie wag lub None, jeśli taki cykl nie istnieje
    """
    n = digraph.V
    
    # Dla każdego wierzchołka jako źródła
    for s in range(n):
        # Inicjalizacja
        ds, ps = init(digraph, s)
        
        # Relaksacja każdej krawędzi n-1 razy
        for i in range(n - 1):
            for u, v in digraph.get_edges():
                w = digraph.get_weight(u, v)
                relax(u, v, w, ds, ps)
        
        # Sprawdzenie, czy istnieje cykl o ujemnej sumie wag
        for u, v in digraph.get_edges():
            w = digraph.get_weight(u, v)
            if ds[v] > ds[u] + w:
                # Znaleziono krawędź w cyklu o ujemnej sumie wag
                # Znajdź cykl poprzez śledzenie poprzedników
                cycle = []
                visited = [False] * n
                
                # Zaczynamy od v i śledzimy poprzedników
                current = v
                while not visited[current]:
                    visited[current] = True
                    cycle.append(current)
                    current = ps[current]
                    
                    # Jeśli doszliśmy do None, to nie ma cyklu
                    if current is None:
                        break
                
                # Jeśli znaleźliśmy cykl, odwróć go i zwróć
                if current is not None:
                    # Znajdź indeks current w cycle
                    start_idx = cycle.index(current)
                    
                    # Wydobądź cykl (od startu do końca) i odwróć go
                    negative_cycle = cycle[start_idx:] + [current]
                    negative_cycle.reverse()
                    
                    return negative_cycle
    
    return None 