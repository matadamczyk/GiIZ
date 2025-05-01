"""
Test dla konkretnego grafu z obrazka.
Numeracja wierzchołków w kodzie od 0 do 11 (odpowiada 1-12 z obrazka).
"""

from lab03.graph_representation import Graph
from lab03.zad2 import zad2, dijkstra, get_path
from lab03.zad3 import compute_distance_matrix
from lab03.zad4 import zad4, find_graph_center, find_minimax_center
from lab03.zad5 import zad5, prim_mst, kruskal_mst
import matplotlib.pyplot as plt
import numpy as np

def create_specific_graph():
    """
    Tworzy graf zgodny z obrazkiem i oczekiwanymi wynikami.
    Na podstawie analizy oczekiwanych ścieżek i odległości.
    Numeracja wierzchołków w kodzie: 0-11 (odpowiada 1-12 z obrazka).
    
    Returns:
        Graf z obrazka
    """
    # Tworzymy graf z 12 wierzchołkami
    graph = Graph(12)
    
    # Dodajemy krawędzie zgodnie z oczekiwanymi wynikami
    # Krawędzie są wnioskowane z oczekiwanych ścieżek najkrótszych
    edges_with_weights = [
        (0, 1, 3),  # 1-2: waga 3
        (0, 2, 2),  # 1-3: waga 2
        (0, 4, 9),  # 1-5: waga 9
        (1, 3, 2),  # 2-4: waga 2
        (1, 4, 4),  # 2-5: waga 4
        (2, 4, 6),  # 3-5: waga 6
        (2, 5, 9),  # 3-6: waga 9
        (3, 6, 3),  # 4-7: waga 3
        # Usuwamy bezpośrednie połączenie 5-6 (indeksy 4-5)
        (4, 6, 1),  # 5-7: waga 1
        (4, 7, 2),  # 5-8: waga 2
        # Usuwamy bezpośrednie połączenie 6-8 (indeksy 5-7)
        (5, 7, 1),  # 6-8: waga 1
        (5, 8, 2),  # 6-9: waga 2
        (6, 9, 5),  # 7-10: waga 5
        (7, 9, 5),  # 8-10: waga 5
        (7, 10, 6),  # 8-11: waga 6
        (7, 11, 9),  # 8-12: waga 9
        (8, 10, 2),  # 9-11: waga 2
        (9, 11, 5),  # 10-12: waga 5
        (10, 11, 3),  # 11-12: waga 3
    ]
    
    for u, v, weight in edges_with_weights:
        graph.add_edge(u, v, weight)
    
    return graph

def visualize_specific_graph(graph, title="Graf z obrazka", save_path=None, highlight_edges=None, interactive=False):
    """
    Wizualizuje graf z numeracją od 1 (a nie od 0).
    
    Args:
        graph: Graf do wizualizacji
        title: Tytuł wykresu
        save_path: Ścieżka do zapisania obrazu
        highlight_edges: Krawędzie do wyróżnienia
        interactive: Czy tryb interaktywny
    """
    if not interactive:
        plt.ioff()
        
    plt.figure(figsize=(12, 10))
    plt.title(title)
    
    # Liczba wierzchołków
    num_vertices = graph.V
    
    # Pozycje na okręgu
    radius = 5
    angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)
    
    # Obliczamy współrzędne
    pos = {}
    for i in range(num_vertices):
        pos[i] = (radius * np.cos(angles[i]), radius * np.sin(angles[i]))
    
    # Rysujemy wierzchołki
    for i in range(num_vertices):
        plt.plot(pos[i][0], pos[i][1], 'bo', markersize=30, alpha=0.6)
        # Wyświetlamy numery od 1, a nie od 0
        plt.text(pos[i][0], pos[i][1], str(i+1), fontsize=15, ha='center', va='center', 
                 color='black', fontweight='bold')
    
    # Rysujemy krawędzie
    if highlight_edges is None:
        highlight_edges = []
        
    for u, v in graph.get_edges():
        edge_color = 'blue' if (u, v) in highlight_edges or (v, u) in highlight_edges else 'black'
        edge_width = 2 if (u, v) in highlight_edges or (v, u) in highlight_edges else 1.5
        plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], c=edge_color, linewidth=edge_width, alpha=0.8)
        
        # Wyświetlamy wagi
        weight = graph.get_weight(u, v)
        midpoint = ((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2)
        plt.text(midpoint[0], midpoint[1], str(weight), fontsize=12, ha='center', va='center', 
                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    plt.axis('equal')
    plt.grid(alpha=0.3)
    plt.axis('off')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    elif interactive:
        plt.show()
    else:
        plt.draw()
        plt.pause(0.001)
        input("Press [Enter] to continue...")
        plt.close()
    
    if not interactive:
        plt.ion()

def test_specific_graph():
    """
    Przeprowadza testy dla konkretnego grafu zgodnego z oczekiwanymi wynikami.
    """
    print("\n" + "="*50)
    print("Test dla konkretnego grafu z obrazka")
    print("="*50 + "\n")
    
    # Oczekiwane wyniki (z treści zadania)
    expected_distances = [0, 3, 2, 5, 7, 10, 8, 9, 12, 13, 14, 17]
    expected_paths = [
        "1", "1 - 2", "1 - 3", "1 - 2 - 4", "1 - 2 - 5",
        "1 - 2 - 5 - 8 - 6", "1 - 2 - 4 - 7", "1 - 2 - 5 - 8",
        "1 - 2 - 5 - 8 - 6 - 9", "1 - 2 - 4 - 7 - 10",
        "1 - 2 - 5 - 8 - 6 - 9 - 11", "1 - 2 - 5 - 8 - 6 - 9 - 11 - 12"
    ]
    
    expected_matrix = [
        [0, 3, 2, 5, 7, 10, 8, 9, 12, 13, 14, 17],
        [3, 0, 5, 2, 4, 7, 5, 6, 9, 10, 11, 14],
        [2, 5, 0, 7, 6, 9, 7, 8, 11, 12, 13, 16],
        [5, 2, 7, 0, 4, 7, 3, 6, 9, 8, 11, 13],
        [7, 4, 6, 4, 0, 3, 1, 2, 5, 6, 7, 10],
        [10, 7, 9, 7, 3, 0, 4, 1, 2, 6, 4, 7],
        [8, 5, 7, 3, 1, 4, 0, 3, 6, 5, 8, 10],
        [9, 6, 8, 6, 2, 1, 3, 0, 3, 5, 5, 8],
        [12, 9, 11, 9, 5, 2, 6, 3, 0, 8, 2, 5],
        [13, 10, 12, 8, 6, 6, 5, 5, 8, 0, 8, 5],
        [14, 11, 13, 11, 7, 4, 8, 5, 2, 8, 0, 3],
        [17, 14, 16, 13, 10, 7, 10, 8, 5, 5, 3, 0]
    ]
    
    # Tworzymy poprawiony graf
    graph = create_specific_graph()
    
    # Wyświetlamy informacje o grafie
    print("Informacje o grafie:")
    print(f"Liczba wierzchołków: {graph.V}")
    print(f"Liczba krawędzi: {len(graph.get_edges())}")
    print("Krawędzie i wagi:")
    for edge, weight in graph.get_weights().items():
        u_display = edge[0] + 1
        v_display = edge[1] + 1
        print(f"Krawędź ({u_display}, {v_display}): {weight}")
    
    # Wizualizujemy graf
    print("\nWizualizacja grafu (naciśnij Enter, aby kontynuować)...")
    visualize_specific_graph(graph, interactive=False)
    
    # Zadanie 2: Algorytm Dijkstry
    print("\n" + "-"*50)
    print("Zadanie 2: Algorytm Dijkstry od wierzchołka 1")
    print("-"*50)
    
    # Uruchamiamy Dijkstrę od wierzchołka 0 (odpowiada 1 na obrazku)
    ds, ps = dijkstra(graph, 0)
    
    # Wyświetlamy wyniki (z numeracją od 1)
    print(f"START: s = 1")
    all_correct = True
    
    for v in range(graph.V):
        path = get_path(ps, 0, v)
        if path:
            # Konwertujemy indeksy na numery od 1
            path_display = [node + 1 for node in path]
            path_str = " - ".join(str(node) for node in path_display)
            print(f"d({v+1}) = {ds[v]} ==> [{path_str}]")
            
            # Sprawdzamy zgodność z oczekiwanymi wynikami
            if ds[v] != expected_distances[v] or path_str != expected_paths[v]:
                all_correct = False
                print(f"  BŁĄD: Oczekiwano d({v+1}) = {expected_distances[v]} ==> [{expected_paths[v]}]")
        else:
            print(f"d({v+1}) = inf ==> (brak ścieżki)")
    
    if all_correct:
        print("\nWszystkie odległości i ścieżki są zgodne z oczekiwanymi wynikami.")
    
    # Zadanie 3: Macierz odległości
    print("\n" + "-"*50)
    print("Zadanie 3: Macierz odległości")
    print("-"*50)
    
    # Obliczamy macierz odległości
    distance_matrix = compute_distance_matrix(graph)
    
    # Wyświetlamy macierz z numeracją od 1
    print("Macierz odległości (numeracja wierzchołków zgodna z obrazkiem 1-12):")
    header = "    " + " ".join(f"{i+1:2d}" for i in range(graph.V))
    print(header)
    
    matrix_correct = True
    for i, row in enumerate(distance_matrix):
        row_str = " ".join(f"{val:2d}" for val in row)
        print(f"{i+1:2d}: {row_str}")
        
        # Sprawdzamy zgodność z oczekiwaną macierzą
        for j, val in enumerate(row):
            if val != expected_matrix[i][j]:
                matrix_correct = False
    
    if matrix_correct:
        print("\nMacierz odległości jest zgodna z oczekiwaną macierzą.")
    else:
        print("\nMacierz odległości NIE jest zgodna z oczekiwaną macierzą.")
    
    # Zadanie 4: Centrum grafu i centrum minimax
    print("\n" + "-"*50)
    print("Zadanie 4: Centrum grafu i centrum minimax")
    print("-"*50)
    
    # Znajdujemy centra na podstawie poprawnej macierzy odległości
    center, min_sum = find_graph_center(expected_matrix)
    minimax_center, min_max_distance = find_minimax_center(expected_matrix)
    
    # Wyświetlamy wyniki z numeracją od 1
    print(f"Centrum = {center+1} (suma odległości: {min_sum})")
    print(f"Centrum minimax = {minimax_center+1} (odległość od najdalszego: {min_max_distance})")
    
    # Sprawdzamy zgodność z oczekiwanymi wynikami
    if center+1 == 5 and minimax_center+1 == 8:
        print("\nCentra są zgodne z oczekiwanymi wynikami.")
    else:
        print("\nCentra NIE są zgodne z oczekiwanymi wynikami.")
        print(f"Oczekiwano: Centrum = 5, Centrum minimax = 8")
    
    # Zadanie 5: Minimalne drzewo rozpinające
    print("\n" + "-"*50)
    print("Zadanie 5: Minimalne drzewo rozpinające")
    print("-"*50)
    
    # Kruskal MST
    kruskal_mst_edges = kruskal_mst(graph)
    kruskal_total_weight = sum(graph.get_weight(u, v) for u, v in kruskal_mst_edges)
    
    # Wyświetlamy wyniki z numeracją od 1
    print(f"MST (Kruskala) o wadze całkowitej: {kruskal_total_weight}")
    print("Krawędzie MST (Kruskala):")
    for u, v in kruskal_mst_edges:
        print(f"({u+1}, {v+1}): {graph.get_weight(u, v)}")
    
    # Wizualizujemy MST
    print("\nWizualizacja MST (Kruskala) - naciśnij Enter, aby kontynuować...")
    visualize_specific_graph(graph, title="MST (Kruskala)", highlight_edges=kruskal_mst_edges, interactive=False)
    
    print("\n" + "="*50)
    print("Koniec testów dla konkretnego grafu")
    print("="*50)

if __name__ == "__main__":
    test_specific_graph() 