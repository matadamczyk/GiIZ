"""
Zadanie 3: Generowanie losowego silnie spójnego digrafu z losowymi wagami krawędzi
i znajdowanie najkrótszych ścieżek za pomocą algorytmu Bellmana-Forda.
"""

from digraph_representation import DiGraph
from random_digraph import (generate_random_strongly_connected_digraph,
                           ensure_no_negative_cycles)
from bellman_ford import bellman_ford, get_path
from digraph_visualization import visualize_digraph
from zad2 import zad2

def zad3():
    """
    Generuje losowy silnie spójny digraf z losowymi wagami krawędzi i znajduje
    najkrótsze ścieżki za pomocą algorytmu Bellmana-Forda z ustawionymi parametrami do prezentacji.
        
    Returns:
        Tuple (digraph, ds, ps): digraph - wygenerowany digraf, ds - odległości,
            ps - poprzednicy
    """
    n = 7
    p = 0.5
    min_weight = -5
    max_weight = 10
    s = 0
    
    print(f"Generowanie losowego silnie spójnego digrafu z {n} wierzchołkami...")
    digraph = generate_random_strongly_connected_digraph(n, p)
    
    if digraph is None:
        print("Nie udało się wygenerować silnie spójnego digrafu. Spróbuj z większym p.")
        return None, None, None
    
    digraph = ensure_no_negative_cycles(digraph, min_weight, max_weight)
    
    print(f"\nWygenerowano silnie spójny digraf z {n} wierzchołkami i {len(digraph.get_edges())} krawędziami")
    print("Wagi krawędzi:")
    for (u, v), weight in digraph.get_weights().items():
        print(f"({u}, {v}): {weight}")
    
    components, is_sc = zad2(digraph)
    if not is_sc:
        print("UWAGA: Wygenerowany digraf NIE jest silnie spójny!")
    
    visualize_digraph(digraph, title="Silnie spójny digraf z losowymi wagami", 
                    interactive=False, show_weights=True)
    
    print(f"\nNajkrótsze ścieżki od wierzchołka {s}:")
    ds, ps, has_negative_cycle = bellman_ford(digraph, s)
    
    if has_negative_cycle:
        print("UWAGA: Wykryto cykl o ujemnej sumie wag osiągalny z wierzchołka źródłowego!")
        return digraph, ds, ps
    
    for v in range(digraph.V):
        if v == s:
            print(f"d({v}) = 0")
            continue
            
        path = get_path(ps, s, v)
        if path:
            path_str = " -> ".join(str(node) for node in path)
            print(f"d({v}) = {ds[v]}: [{path_str}]")
        else:
            print(f"d({v}) = inf (brak ścieżki)")
    
    return digraph, ds, ps

if __name__ == "__main__":
    digraph, ds, ps = zad3() 