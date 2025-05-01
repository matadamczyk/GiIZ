"""
Zadanie 3: Generowanie losowego silnie spójnego digrafu z losowymi wagami krawędzi
i znajdowanie najkrótszych ścieżek za pomocą algorytmu Bellmana-Forda.
"""

from lab04.digraph_representation import DiGraph
from lab04.random_digraph import (generate_random_strongly_connected_digraph, 
                                assign_random_weights, ensure_no_negative_cycles)
from lab04.bellman_ford import bellman_ford, get_path
from lab04.digraph_visualization import visualize_digraph
from lab04.zad2 import zad2

def zad3(n=7, p=0.4, min_weight=-5, max_weight=10, s=0, interactive=False):
    """
    Generuje losowy silnie spójny digraf z losowymi wagami krawędzi i znajduje
    najkrótsze ścieżki za pomocą algorytmu Bellmana-Forda.
    
    Args:
        n: Liczba wierzchołków
        p: Prawdopodobieństwo istnienia krawędzi
        min_weight: Minimalna waga krawędzi
        max_weight: Maksymalna waga krawędzi
        s: Wierzchołek źródłowy
        interactive: Czy wyświetlać wykresy interaktywnie
        
    Returns:
        Tuple (digraph, ds, ps): digraph - wygenerowany digraf, ds - odległości,
            ps - poprzednicy
    """
    # Generuj losowy silnie spójny digraf
    print(f"Generowanie losowego silnie spójnego digrafu z {n} wierzchołkami...")
    digraph = generate_random_strongly_connected_digraph(n, p)
    
    if digraph is None:
        print("Nie udało się wygenerować silnie spójnego digrafu. Spróbuj z większym p.")
        return None, None, None
    
    # Przypisz losowe wagi
    assign_random_weights(digraph, min_weight, max_weight)
    
    # Usuń ujemne cykle, jeśli istnieją
    digraph = ensure_no_negative_cycles(digraph, min_weight, max_weight)
    
    # Wyświetl informacje o digrafie
    print(f"\nWygenerowano silnie spójny digraf z {n} wierzchołkami i {len(digraph.get_edges())} krawędziami")
    print("Wagi krawędzi:")
    for (u, v), weight in digraph.get_weights().items():
        print(f"({u}, {v}): {weight}")
    
    # Sprawdź, czy digraf jest silnie spójny
    components, is_sc = zad2(digraph, False)
    if not is_sc:
        print("UWAGA: Wygenerowany digraf NIE jest silnie spójny!")
    
    # Wizualizuj digraf z wagami
    visualize_digraph(digraph, title="Silnie spójny digraf z losowymi wagami", 
                    interactive=interactive, show_weights=True)
    
    # Uruchom algorytm Bellmana-Forda
    print(f"\nNajkrótsze ścieżki od wierzchołka {s}:")
    ds, ps, has_negative_cycle = bellman_ford(digraph, s)
    
    if has_negative_cycle:
        print("UWAGA: Wykryto cykl o ujemnej sumie wag osiągalny z wierzchołka źródłowego!")
        return digraph, ds, ps
    
    # Wyświetl najkrótsze ścieżki
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
    # Generuj losowy silnie spójny digraf z losowymi wagami i znajdź najkrótsze ścieżki
    digraph, ds, ps = zad3(7, 0.5, -5, 10, 0, True) 