"""
Główny plik do uruchomienia wszystkich zadań z laboratorium 3.
"""

import argparse
from lab03.zad1 import zad1
from lab03.zad2 import zad2
from lab03.zad3 import zad3
from lab03.zad4 import zad4
from lab03.zad5 import zad5

def main():
    """
    Główna funkcja uruchamiająca wszystkie zadania z laboratorium 3.
    """
    parser = argparse.ArgumentParser(description='Laboratorium 3 - Algorytmy grafowe')
    parser.add_argument('--n', type=int, default=12, help='Liczba wierzchołków grafu')
    parser.add_argument('--min-weight', type=int, default=1, help='Minimalna waga krawędzi')
    parser.add_argument('--max-weight', type=int, default=10, help='Maksymalna waga krawędzi')
    parser.add_argument('--start-vertex', type=int, default=0, help='Wierzchołek startowy dla algorytmu Dijkstry')
    parser.add_argument('--mst-algorithm', choices=['prim', 'kruskal', 'both'], default='both',
                      help='Algorytm do znalezienia MST')
    parser.add_argument('--interactive', action='store_true', help='Tryb interaktywny dla wykresów')
    
    args = parser.parse_args()
    
    print("\n" + "="*50)
    print("Laboratorium 3 - Algorytmy grafowe")
    print("="*50 + "\n")
    
    # Zadanie 1: Generowanie spójnego grafu losowego z wagami
    print("\n" + "-"*50)
    print("Zadanie 1: Generowanie spójnego grafu losowego z wagami")
    print("-"*50)
    graph = zad1(args.n, args.min_weight, args.max_weight, args.interactive)
    
    # Zadanie 2: Algorytm Dijkstry
    print("\n" + "-"*50)
    print("Zadanie 2: Algorytm Dijkstry")
    print("-"*50)
    ds, ps, _ = zad2(graph, args.start_vertex)
    
    # Zadanie 3: Macierz odległości
    print("\n" + "-"*50)
    print("Zadanie 3: Macierz odległości")
    print("-"*50)
    distance_matrix = zad3(graph)
    
    # Zadanie 4: Centrum grafu i centrum minimax
    print("\n" + "-"*50)
    print("Zadanie 4: Centrum grafu i centrum minimax")
    print("-"*50)
    center, minimax_center = zad4(graph, distance_matrix)
    
    # Zadanie 5: Minimalne drzewo rozpinające
    print("\n" + "-"*50)
    print("Zadanie 5: Minimalne drzewo rozpinające")
    print("-"*50)
    prim_mst, kruskal_mst = zad5(graph, args.mst_algorithm, args.interactive)
    
    print("\n" + "="*50)
    print("Koniec laboratorium 3")
    print("="*50 + "\n")

if __name__ == "__main__":
    main() 