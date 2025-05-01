"""
Zadanie 1: Generowanie losowego digrafu z zespołu G(n, p).
"""

from lab04.digraph_representation import DiGraph
from lab04.random_digraph import generate_random_digraph
from lab04.digraph_visualization import visualize_digraph

def zad1(n=7, p=0.4, interactive=False):
    """
    Generuje losowy digraf z zespołu G(n, p).
    
    Args:
        n: Liczba wierzchołków
        p: Prawdopodobieństwo istnienia krawędzi
        interactive: Czy wyświetlać wykresy interaktywnie
        
    Returns:
        DiGraph: Wygenerowany losowy digraf
    """
    # Generuj losowy digraf
    digraph = generate_random_digraph(n, p)
    
    # Wyświetl informacje o digrafie
    print(f"Wygenerowano losowy digraf z {n} wierzchołkami i {len(digraph.get_edges())} krawędziami")
    
    # Wyświetl reprezentacje digrafu
    print("\nLista sąsiedztwa:")
    for i, neighbors in enumerate(digraph.get_adjacency_list()):
        print(f"{i+1}. {i}: {neighbors}")
    
    print("\nMacierz sąsiedztwa:")
    for i, row in enumerate(digraph.get_adjacency_matrix()):
        print(f"{i}: {row}")
    
    # Wizualizuj digraf
    visualize_digraph(digraph, title="Losowy digraf G(n, p)", interactive=interactive)
    
    return digraph

if __name__ == "__main__":
    # Generuj losowy digraf z 7 wierzchołkami i prawdopodobieństwem p=0.4
    digraph = zad1(7, 0.4, True) 