"""
Zadanie 1: Generowanie losowego digrafu z zespołu G(n, p).
"""

from digraph_representation import DiGraph
from random_digraph import generate_random_digraph
from digraph_visualization import visualize_digraph

def zad1():
    """
    Generuje losowy digraf z zespołu G(n, p) z ustawionymi parametrami do prezentacji.
        
    Returns:
        DiGraph: Wygenerowany losowy digraf
    """
    n = 7
    p = 0.4
    
    digraph = generate_random_digraph(n, p)
    
    print(f"Wygenerowano losowy digraf z {n} wierzchołkami i {len(digraph.get_edges())} krawędziami")
    
    print("\nLista sąsiedztwa:")
    for i, neighbors in enumerate(digraph.get_adjacency_list()):
        print(f"{i+1}. {i}: {neighbors}")
    
    print("\nMacierz sąsiedztwa:")
    for i, row in enumerate(digraph.get_adjacency_matrix()):
        print(f"{i}: {row}")
    
    visualize_digraph(digraph, title="Losowy digraf G(n, p)", interactive=False)
    
    return digraph

if __name__ == "__main__":
    digraph = zad1() 