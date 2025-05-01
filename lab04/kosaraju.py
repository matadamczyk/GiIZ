"""
Implementacja algorytmu Kosaraju do znajdowania silnie spójnych składowych w grafie skierowanym.
"""

from lab04.digraph_representation import DiGraph

def kosaraju(digraph):
    """
    Algorytm Kosaraju do znajdowania silnie spójnych składowych w grafie skierowanym.
    
    Args:
        digraph: DiGraph - graf skierowany
        
    Returns:
        Lista list wierzchołków, gdzie każda lista to jedna silnie spójna składowa
    """
    # Inicjalizacja
    n = digraph.V
    d = [-1] * n  # Czas odwiedzenia
    f = [-1] * n  # Czas przetworzenia
    comp = [-1] * n  # Numer silnie spójnej składowej dla wierzchołka
    t = [0]  # Używamy listy jako obiektu mutowalnego, aby był dostępny w DFS_visit
    
    # Pierwsze przeszukiwanie w głąb (DFS)
    stack = []  # Stos wierzchołków posortowanych wg malejących czasów przetworzenia
    
    # Odwiedź wszystkie wierzchołki
    for v in range(n):
        if d[v] == -1:
            DFS_visit(v, digraph, d, f, t, stack)
    
    # Stwórz transpozycję grafu (odwrócenie krawędzi)
    G_T = digraph.transpose()
    
    # Drugie przeszukiwanie w głąb (DFS) na transpozycji
    nr = 0  # Numer silnie spójnej składowej
    components = []  # Lista silnie spójnych składowych
    
    # Oznacz wszystkie wierzchołki jako nieodwiedzone
    for v in range(n):
        comp[v] = -1
    
    # Przetwarzaj wierzchołki w kolejności malejących czasów przetworzenia
    while stack:
        v = stack.pop()
        if comp[v] == -1:
            # Nowa silnie spójna składowa
            nr += 1
            comp[v] = nr
            current_component = [v]
            components_r(nr, v, G_T, comp, current_component)
            components.append(current_component)
    
    return components

def DFS_visit(v, digraph, d, f, t, stack):
    """
    Przeszukiwanie w głąb (DFS) zaczynające od wierzchołka v.
    
    Args:
        v: Wierzchołek startowy
        digraph: DiGraph - graf skierowany
        d: Tablica czasów odwiedzenia
        f: Tablica czasów przetworzenia
        t: Czas [w formie jednoelementowej listy]
        stack: Stos wierzchołków posortowanych wg malejących czasów przetworzenia
    """
    t[0] += 1
    d[v] = t[0]
    
    # Przejście po wszystkich sąsiadach v
    for u in digraph.get_out_neighbors(v):
        if d[u] == -1:
            DFS_visit(u, digraph, d, f, t, stack)
    
    t[0] += 1
    f[v] = t[0]
    stack.append(v)  # Dodaj v do stosu po przetworzeniu

def components_r(nr, v, G_T, comp, current_component):
    """
    Funkcja rekurencyjna do znajdowania wierzchołków w silnie spójnej składowej.
    
    Args:
        nr: Numer silnie spójnej składowej
        v: Aktualny wierzchołek
        G_T: Transponowany digraf
        comp: Tablica przyporządkowująca wierzchołki do silnie spójnych składowych
        current_component: Lista wierzchołków w bieżącej silnie spójnej składowej
    """
    # Przejście po wszystkich sąsiadach v w transponowanym grafie
    for u in G_T.get_out_neighbors(v):
        if comp[u] == -1:
            comp[u] = nr
            current_component.append(u)
            components_r(nr, u, G_T, comp, current_component)

def is_strongly_connected(digraph):
    """
    Sprawdza, czy digraf jest silnie spójny.
    
    Args:
        digraph: DiGraph - graf skierowany
        
    Returns:
        bool: True jeśli digraf jest silnie spójny, False w przeciwnym razie
    """
    components = kosaraju(digraph)
    return len(components) == 1 