"""
Moduł do generowania losowych digrafów z różnymi właściwościami.
"""

import random
from digraph_representation import DiGraph

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

def generate_random_strongly_connected_digraph(n, p, min_weight=-5, max_weight=10):
    """
    Generuje losowy silnie spójny digraf z zespołu G(n, p) z wagami na krawędziach.
    
    Args:
        n: Liczba wierzchołków
        p: Prawdopodobieństwo istnienia krawędzi
        min_weight: Minimalna waga krawędzi (domyślnie -5)
        max_weight: Maksymalna waga krawędzi (domyślnie 10)
        
    Returns:
        DiGraph: Silnie spójny digraf z wagami
    """
    if n <= 0:
        raise ValueError("Liczba wierzchołków musi być dodatnia")
    
    if n == 1:
        digraph = DiGraph(n)
        digraph.add_edge(0, 0, random.randint(min_weight, max_weight))
        return digraph
    
    max_attempts = 1000
    
    for attempt in range(max_attempts):
        digraph = generate_random_digraph(n, p)
        
        for i, j in digraph.get_edges():
            weight = random.randint(min_weight, max_weight)
            digraph.set_edge_weight(i, j, weight)
        
        from kosaraju import kosaraju
        components = kosaraju(digraph)
        
        if len(components) == 1:
            return digraph
            
        force_connectivity_with_weights(digraph, components, min_weight, max_weight)
        
        components_after = kosaraju(digraph)
        if len(components_after) == 1:
            return digraph
    
    digraph = create_strongly_connected_digraph_with_weights(n, min_weight, max_weight)
    add_random_edges_with_weights(digraph, p, min_weight, max_weight)
    
    return digraph

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
    digraph = generate_random_strongly_connected_digraph(n, p, min_weight, max_weight)
    
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
    from bellman_ford import has_negative_cycle, find_negative_cycle
    
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

def check_for_negative_cycles_with_weights(digraph, min_weight, max_weight):
    """
    Sprawdza czy digraf ma cykl o ujemnej sumie wag i eliminuje takie cykle.
    
    Args:
        digraph: Digraf do sprawdzenia
        min_weight: Minimalna waga krawędzi
        max_weight: Maksymalna waga krawędzi
    """
    from bellman_ford import has_negative_cycle, find_negative_cycle
    
    while has_negative_cycle(digraph):
        cycle = find_negative_cycle(digraph)
        if not cycle:
            break
            
        for i in range(len(cycle) - 1):
            u, v = cycle[i], cycle[i + 1]
            new_weight = random.randint(1, max_weight)
            digraph.set_edge_weight(u, v, new_weight)

def force_connectivity_with_weights(digraph, components, min_weight, max_weight):
    """
    Wymusza silną spójność digrafu przez dodanie krawędzi między składowymi.
    
    Args:
        digraph: Digraf do modyfikacji
        components: Lista silnie spójnych składowych
        min_weight: Minimalna waga krawędzi
        max_weight: Maksymalna waga krawędzi
    """
    if len(components) <= 1:
        return
    
    for i in range(len(components) - 1):
        u = random.choice(components[i])
        v = random.choice(components[i + 1])
        weight = random.randint(min_weight, max_weight)
        digraph.add_edge(u, v, weight)
    
    last_component = components[-1]
    first_component = components[0]
    u = random.choice(last_component)
    v = random.choice(first_component)
    weight = random.randint(min_weight, max_weight)
    digraph.add_edge(u, v, weight)

def create_strongly_connected_digraph_with_weights(n, min_weight, max_weight):
    """
    Tworzy deterministycznie silnie spójny digraf z wagami.
    
    Args:
        n: Liczba wierzchołków
        min_weight: Minimalna waga krawędzi
        max_weight: Maksymalna waga krawędzi
        
    Returns:
        DiGraph: Silnie spójny digraf
    """
    digraph = DiGraph(n)
    
    for i in range(n):
        next_vertex = (i + 1) % n
        weight = random.randint(min_weight, max_weight)
        digraph.add_edge(i, next_vertex, weight)
    
    return digraph

def add_random_edges_with_weights(digraph, p, min_weight, max_weight):
    """
    Dodaje losowe krawędzie z wagami do digrafu.
    
    Args:
        digraph: Digraf do modyfikacji
        p: Prawdopodobieństwo dodania krawędzi
        min_weight: Minimalna waga krawędzi
        max_weight: Maksymalna waga krawędzi
    """
    n = digraph.V
    
    for u in range(n):
        for v in range(n):
            if not digraph.has_edge(u, v) and random.random() < p:
                weight = random.randint(min_weight, max_weight)
                digraph.add_edge(u, v, weight) 