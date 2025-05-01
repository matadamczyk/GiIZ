"""
Generator losowych digrafów (skierowanych grafów) z zespołu G(n, p).
"""

import random
from lab04.digraph_representation import DiGraph

def generate_random_digraph(n, p):
    """
    Generuje losowy digraf z zespołu G(n, p).
    
    Args:
        n: Liczba wierzchołków
        p: Prawdopodobieństwo istnienia krawędzi między dowolną parą wierzchołków
        
    Returns:
        DiGraph: Wygenerowany losowy digraf
    """
    if p < 0 or p > 1:
        raise ValueError("Prawdopodobieństwo p musi być z zakresu [0, 1]")
    
    # Stwórz pusty digraf z n wierzchołkami
    digraph = DiGraph(n)
    
    # Dla każdej pary wierzchołków, dodaj krawędź z prawdopodobieństwem p
    for u in range(n):
        for v in range(n):
            if u != v and random.random() < p:
                digraph.add_edge(u, v)
    
    return digraph

def assign_random_weights(digraph, min_weight=-5, max_weight=10):
    """
    Przypisuje losowe wagi krawędziom digrafu.
    
    Args:
        digraph: DiGraph, któremu mają być przypisane wagi
        min_weight: Minimalna wartość wagi
        max_weight: Maksymalna wartość wagi
        
    Returns:
        DiGraph: Graf z przypisanymi wagami
    """
    for u, v in digraph.get_edges():
        weight = random.randint(min_weight, max_weight)
        digraph.weights[(u, v)] = weight
    
    return digraph

def generate_random_weighted_digraph(n, p, min_weight=-5, max_weight=10):
    """
    Generuje losowy digraf z losowymi wagami krawędzi.
    
    Args:
        n: Liczba wierzchołków
        p: Prawdopodobieństwo istnienia krawędzi
        min_weight: Minimalna wartość wagi
        max_weight: Maksymalna wartość wagi
        
    Returns:
        DiGraph: Wygenerowany losowy ważony digraf
    """
    digraph = generate_random_digraph(n, p)
    assign_random_weights(digraph, min_weight, max_weight)
    return digraph

def generate_random_strongly_connected_digraph(n, p, max_attempts=100):
    """
    Generuje losowy silnie spójny digraf.
    Próbuje wygenerować digraf tak długo, aż będzie silnie spójny.
    
    Args:
        n: Liczba wierzchołków
        p: Prawdopodobieństwo istnienia krawędzi
        max_attempts: Maksymalna liczba prób wygenerowania
        
    Returns:
        DiGraph: Wygenerowany losowy silnie spójny digraf lub None, jeśli nie udało się po max_attempts próbach
    """
    from lab04.kosaraju import kosaraju
    
    for _ in range(max_attempts):
        digraph = generate_random_digraph(n, p)
        components = kosaraju(digraph)
        
        # Jeśli digraf ma tylko jedną silnie spójną składową, jest silnie spójny
        if len(components) == 1:
            return digraph
    
    return None

def generate_random_weighted_strongly_connected_digraph(n, p, min_weight=-5, max_weight=10, max_attempts=100):
    """
    Generuje losowy silnie spójny digraf z losowymi wagami.
    
    Args:
        n: Liczba wierzchołków
        p: Prawdopodobieństwo istnienia krawędzi
        min_weight: Minimalna wartość wagi
        max_weight: Maksymalna wartość wagi
        max_attempts: Maksymalna liczba prób wygenerowania
        
    Returns:
        DiGraph: Wygenerowany losowy silnie spójny ważony digraf lub None, jeśli nie udało się
    """
    digraph = generate_random_strongly_connected_digraph(n, p, max_attempts)
    
    if digraph:
        assign_random_weights(digraph, min_weight, max_weight)
        return digraph
    
    return None

def ensure_no_negative_cycles(digraph, min_weight=-4, max_weight=10):
    """
    Modyfikuje wagi digrafu tak, aby nie zawierał cykli o ujemnej sumie wag.
    
    Strategia:
    1. Znajdź wszystkie cykle w digrafie
    2. Dla każdego cyklu, sprawdź czy ma ujemną sumę wag
    3. Jeśli tak, losowo zwiększ wagi niektórych krawędzi w cyklu
    
    Args:
        digraph: DiGraph do modyfikacji
        min_weight: Nowa minimalna wartość wagi (dla krawędzi w ujemnych cyklach)
        max_weight: Nowa maksymalna wartość wagi (dla krawędzi w ujemnych cyklach)
        
    Returns:
        DiGraph: Zmodyfikowany digraf bez ujemnych cykli
    """
    from lab04.bellman_ford import has_negative_cycle, find_negative_cycle
    
    # Dopóki graf ma ujemne cykle
    while has_negative_cycle(digraph):
        # Znajdź przykładowy ujemny cykl
        cycle = find_negative_cycle(digraph)
        
        if not cycle:
            break
        
        # Dla każdej krawędzi w cyklu, zwiększ jej wagę
        for i in range(len(cycle) - 1):
            u, v = cycle[i], cycle[i + 1]
            old_weight = digraph.get_weight(u, v)
            
            # Przypisz nową, większą wagę
            new_weight = random.randint(min(0, min_weight), max_weight)
            if new_weight <= 0:
                new_weight = 1  # Zapewnij, że waga nie będzie ujemna
                
            digraph.weights[(u, v)] = new_weight
    
    return digraph 