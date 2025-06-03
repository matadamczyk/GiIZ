"""
Zadanie 4: Algorytm Johnsona dla najkrótszych ścieżek między wszystkimi parami wierzchołków.
"""

from digraph_representation import DiGraph
from johnson import johnson, johnson_with_paths, get_path_from_predecessors
from zad3 import zad3

def zad4(digraph=None):
    """
    Znajduje najkrótsze ścieżki między wszystkimi parami wierzchołków
    za pomocą algorytmu Johnsona.
    
    Args:
        digraph: DiGraph - graf skierowany z wagami (jeśli None, zostanie wygenerowany)
        
    Returns:
        Tuple (distances, paths): distances - macierz odległości, paths - macierz poprzedników
    """
    if digraph is None:
        digraph, _, _ = zad3()
        
        if digraph is None:
            print("Nie udało się wygenerować digrafu.")
            return None, None
    
    distances, paths = johnson_with_paths(digraph)
    
    if distances is None:
        print("Wykryto cykl o ujemnej sumie wag. Algorytm Johnsona nie może być zastosowany.")
        return None, None
    
    print("\nMacierz odległości (algorytm Johnsona):")
    for i, row in enumerate(distances):
        formatted_row = " ".join(f"{d if d != float('inf') else 'inf':3}" for d in row)
        print(f"{i}: {formatted_row}")
    
    return distances, paths

if __name__ == "__main__":
    distances, paths = zad4() 