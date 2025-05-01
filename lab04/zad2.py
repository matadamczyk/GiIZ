"""
Zadanie 2: Znajdowanie silnie spójnych składowych za pomocą algorytmu Kosaraju.
"""

from lab04.digraph_representation import DiGraph
from lab04.kosaraju import kosaraju, is_strongly_connected
from lab04.digraph_visualization import visualize_digraph_with_components
from lab04.zad1 import zad1

def zad2(digraph=None, interactive=False):
    """
    Znajduje silnie spójne składowe w digrafie za pomocą algorytmu Kosaraju.
    
    Args:
        digraph: DiGraph - graf skierowany (jeśli None, zostanie wygenerowany)
        interactive: Czy wyświetlać wykresy interaktywnie
        
    Returns:
        Tuple (components, is_sc): components - lista silnie spójnych składowych,
            is_sc - czy digraf jest silnie spójny
    """
    if digraph is None:
        # Generuj losowy digraf
        digraph = zad1(7, 0.4, interactive)
    
    # Znajdź silnie spójne składowe
    components = kosaraju(digraph)
    
    # Sprawdź, czy digraf jest silnie spójny
    is_sc = is_strongly_connected(digraph)
    
    # Wyświetl informacje o silnie spójnych składowych
    print("\nSilnie spójne składowe:")
    for i, component in enumerate(components):
        print(f"Składowa {i+1}: {component}")
    
    print(f"\nDigraf jest{'jest silnie spójny' if is_sc else ' NIE jest silnie spójny'}")
    
    # Wizualizuj digraf z kolorowanymi składowymi
    visualize_digraph_with_components(digraph, components, 
                                    title="Silnie spójne składowe digrafu", 
                                    interactive=interactive)
    
    return components, is_sc

if __name__ == "__main__":
    # Znajdź silnie spójne składowe w losowym digrafie
    components, is_sc = zad2(interactive=True) 