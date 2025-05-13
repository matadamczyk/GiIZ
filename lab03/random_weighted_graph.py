"""
Moduł generatora losowych grafów ważonych.
Implementuje generowanie połączonych losowych grafów z losowymi wagami.
"""

import random
import math
from graph_representation import Graph

def generate_random_connected_graph(n, p=None):
    """
    Generuje losowy spójny graf z n wierzchołkami.
    
    Argumenty:
        n: Liczba wierzchołków
        p: Prawdopodobieństwo utworzenia krawędzi (jeśli None, obliczane automatycznie)
        
    Zwraca:
        Obiekt Graph z n wierzchołkami, który jest spójny
    """
    if n < 1:
        raise ValueError("Liczba wierzchołków musi wynosić co najmniej 1")
    
    # Jeśli p nie jest podane, oblicz rozsądną wartość
    if p is None:
        # Dla małych n używamy wyższego prawdopodobieństwa, aby zapewnić spójność
        if n <= 10:
            p = 0.4
        else:
            # Dla większych n możemy użyć niższego prawdopodobieństwa
            # lim p = ln(n)/n gdy n → ∞ dla spójności
            p = max(0.1, 2 * math.log(n) / n)
    
    # Utwórz graf z n wierzchołkami
    graph = Graph(n)
    
    # Najpierw zapewnij, że graf jest spójny, dodając drzewo rozpinające
    for i in range(1, n):
        # Połącz i z losowym wierzchołkiem z zakresu [0, i-1]
        j = random.randint(0, i-1)
        graph.add_edge(i, j)
    
    # Dodaj dodatkowe krawędzie z prawdopodobieństwem p
    for i in range(n):
        for j in range(i + 1, n):
            # Pomiń, jeśli krawędź już istnieje
            if (i, j) in graph.get_edges() or (j, i) in graph.get_edges():
                continue
                
            if random.random() < p:
                graph.add_edge(i, j)
    
    return graph

def assign_random_weights(graph, min_weight=1, max_weight=10):
    """
    Przypisuje losowe wagi do wszystkich krawędzi w grafie.
    
    Argumenty:
        graph: Obiekt Graph
        min_weight: Minimalna waga (włącznie)
        max_weight: Maksymalna waga (włącznie)
        
    Zwraca:
        Ten sam graf z zaktualizowanymi wagami
    """
    for edge in graph.get_edges():
        u, v = edge
        weight = random.randint(min_weight, max_weight)
        
        # Aktualizuj wagę w grafie
        graph.weights[edge] = weight
    
    return graph

def generate_random_weighted_connected_graph(n, min_weight=1, max_weight=10, p=None):
    """
    Generuje losowy spójny graf z n wierzchołkami i losowymi wagami.
    
    Argumenty:
        n: Liczba wierzchołków
        min_weight: Minimalna waga (włącznie)
        max_weight: Maksymalna waga (włącznie)
        p: Prawdopodobieństwo utworzenia krawędzi (jeśli None, obliczane automatycznie)
        
    Zwraca:
        Obiekt Graph z n wierzchołkami, spójny, z losowymi wagami
    """
    graph = generate_random_connected_graph(n, p)
    return assign_random_weights(graph, min_weight, max_weight)


# Przykład użycia
if __name__ == "__main__":
    n = 10
    g = generate_random_weighted_connected_graph(n)
    print(f"Wygenerowano spójny graf ważony z {n} wierzchołkami i {len(g.get_edges())} krawędziami")
    print("Wagi:", g.get_weights()) 