"""
Zadanie 2: Znajdowanie silnie spójnych składowych w digrafie.
"""

from digraph_representation import DiGraph
from kosaraju import kosaraju, is_strongly_connected
from digraph_visualization import visualize_digraph_with_components
from zad1 import zad1

def zad2(digraph=None):
    """
    Znajduje silnie spójne składowe w digrafie za pomocą algorytmu Kosaraju.
    
    Args:
        digraph: DiGraph - graf skierowany (jeśli None, zostanie wygenerowany)
        
    Returns:
        Tuple (components, is_sc): components - lista silnie spójnych składowych,
            is_sc - czy digraf jest silnie spójny
    """
    if digraph is None:
        digraph = zad1()
    
    components = kosaraju(digraph)
    
    is_sc = is_strongly_connected(digraph)
    
    print("\nSilnie spójne składowe:")
    for i, component in enumerate(components):
        print(f"Składowa {i+1}: {component}")
    
    print(f"\nDigraf jest{'jest silnie spójny' if is_sc else ' NIE jest silnie spójny'}")
    
    visualize_digraph_with_components(digraph, components, 
                                    title="Silnie spójne składowe digrafu", 
                                    interactive=False)
    
    return components, is_sc

if __name__ == "__main__":
    components, is_sc = zad2() 