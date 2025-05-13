"""
Zadanie 1: Generowanie spójnego grafu losowego z wagami.
"""

from random_weighted_graph import generate_random_weighted_connected_graph
from graph_visualization import visualize_graph

def zad1(n=12, min_weight=1, max_weight=10, interactive=False):
    """
    Generuje losowy spójny graf o n wierzchołkach i przypisuje każdej krawędzi
    losową wagę z zakresu [min_weight, max_weight].
    
    Args:
        n: Liczba wierzchołków
        min_weight: Minimalna waga krawędzi (włącznie)
        max_weight: Maksymalna waga krawędzi (włącznie)
        interactive: Czy wykresy mają być wyświetlane interaktywnie
        
    Returns:
        Wygenerowany graf z losowymi wagami
    """
    # Generuj losowy spójny graf z losowymi wagami
    graph = generate_random_weighted_connected_graph(n, min_weight, max_weight)
    
    # Wyświetl informacje o grafie
    print(f"Wygenerowano spójny graf losowy z {n} wierzchołkami i {len(graph.get_edges())} krawędziami")
    print("Wagi krawędzi:")
    for edge, weight in graph.get_weights().items():
        print(f"Krawędź {edge}: {weight}")
    
    # Wizualizuj graf
    visualize_graph(graph, title_prefix="Spójny graf losowy z wagami", interactive=interactive)
    
    return graph

if __name__ == "__main__":
    # Generuj graf z 12 wierzchołkami i wagami z zakresu [1, 10]
    graph = zad1(12, 1, 10, True) 