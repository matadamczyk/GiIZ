"""
Zadanie 5: Wyznaczanie minimalnego drzewa rozpinającego.
"""

from zad1 import zad1
from graph_representation import Graph
from graph_visualization import visualize_graph

def prim_mst(graph):
    """
    Algorytm Prima do znajdowania minimalnego drzewa rozpinającego.
    
    Args:
        graph: Graf wejściowy
        
    Returns:
        Lista krawędzi należących do MST
    """
    n = graph.V
    
    # Inicjalizacja zbioru wierzchołków w MST i zbioru krawędzi MST
    vertices_in_mst = {0}  # Zaczynamy od wierzchołka 0
    mst_edges = []
    
    # Dopóki nie dodamy wszystkich wierzchołków do MST
    while len(vertices_in_mst) < n:
        min_weight = float('inf')
        min_edge = None
        
        # Dla każdej krawędzi (u, v) gdzie u jest w MST, a v nie jest
        for u in vertices_in_mst:
            for v in range(n):
                if v not in vertices_in_mst:
                    edge = (min(u, v), max(u, v))
                    if edge in graph.get_weights():
                        weight = graph.get_weight(u, v)
                        if weight < min_weight:
                            min_weight = weight
                            min_edge = edge
        
        # Jeśli nie znaleziono żadnej krawędzi, graf nie jest spójny
        if min_edge is None:
            break
        
        # Dodaj krawędź do MST i dodaj nowy wierzchołek do zbioru
        mst_edges.append(min_edge)
        vertices_in_mst.add(min_edge[0])
        vertices_in_mst.add(min_edge[1])
    
    return mst_edges

class DisjointSet:
    """Implementacja struktury zbiorów rozłącznych (Union-Find)."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Kompresja ścieżki
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return
        
        # Łączenie według rangi
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1

def kruskal_mst(graph):
    """
    Algorytm Kruskala do znajdowania minimalnego drzewa rozpinającego.
    
    Args:
        graph: Graf wejściowy
        
    Returns:
        Lista krawędzi należących do MST
    """
    n = graph.V
    
    # Inicjalizacja zbioru rozłącznego dla każdego wierzchołka
    ds = DisjointSet(n)
    
    # Lista krawędzi MST
    mst_edges = []
    
    # Sortuj krawędzie według wagi
    edges = []
    for edge in graph.get_edges():
        weight = graph.get_weight(edge[0], edge[1])
        edges.append((weight, edge))
    
    edges.sort()  # Sortowanie według wagi
    
    # Dodawaj krawędzie do MST, jeśli nie tworzą cyklu
    for weight, edge in edges:
        u, v = edge
        
        # Jeśli u i v są już w tym samym zbiorze, dodanie tej krawędzi tworzy cykl
        if ds.find(u) != ds.find(v):
            mst_edges.append(edge)
            ds.union(u, v)
        
        # Jeśli mamy już n-1 krawędzi, kończymy
        if len(mst_edges) == n - 1:
            break
    
    return mst_edges

def create_mst_graph(original_graph, mst_edges):
    """
    Tworzy nowy graf zawierający tylko krawędzie z MST.
    
    Args:
        original_graph: Oryginalny graf
        mst_edges: Lista krawędzi MST
        
    Returns:
        Nowy graf z krawędziami MST
    """
    mst_graph = Graph(original_graph.V)
    
    for edge in mst_edges:
        u, v = edge
        weight = original_graph.get_weight(u, v)
        mst_graph.add_edge(u, v, weight)
    
    return mst_graph

def zad5(graph=None, algorithm="both", interactive=False):
    """
    Wyznacza minimalne drzewo rozpinające przy użyciu algorytmu Prima lub Kruskala.
    
    Args:
        graph: Graf wejściowy (jeśli None, zostanie wygenerowany)
        algorithm: Algorytm do użycia ("prim", "kruskal" lub "both")
        interactive: Czy wykresy mają być wyświetlane interaktywnie
        
    Returns:
        Tuple (prim_mst_edges, kruskal_mst_edges): krawędzie MST dla obu algorytmów
    """
    if graph is None:
        graph = zad1(12, 1, 10, interactive)
    
    prim_mst_edges = None
    kruskal_mst_edges = None
    
    # Algorytm Prima
    if algorithm in ["prim", "both"]:
        prim_mst_edges = prim_mst(graph)
        prim_total_weight = sum(graph.get_weight(u, v) for u, v in prim_mst_edges)
        print(f"MST (Prima) o wadze całkowitej: {prim_total_weight}")
        print("Krawędzie MST (Prima):", prim_mst_edges)
        
        # Wizualizuj MST z algorytmu Prima
        visualize_graph(graph, force_directed=False, title_prefix="MST (Prima)", 
                        highlight_edges=prim_mst_edges, interactive=interactive)
    
    # Algorytm Kruskala
    if algorithm in ["kruskal", "both"]:
        kruskal_mst_edges = kruskal_mst(graph)
        kruskal_total_weight = sum(graph.get_weight(u, v) for u, v in kruskal_mst_edges)
        print(f"MST (Kruskala) o wadze całkowitej: {kruskal_total_weight}")
        print("Krawędzie MST (Kruskala):", kruskal_mst_edges)
        
        # Wizualizuj MST z algorytmu Kruskala
        visualize_graph(graph, force_directed=False, title_prefix="MST (Kruskala)", 
                        highlight_edges=kruskal_mst_edges, interactive=interactive)
    
    return prim_mst_edges, kruskal_mst_edges

if __name__ == "__main__":
    # Generuj graf i znajdź MST
    prim_mst, kruskal_mst = zad5(interactive=True) 