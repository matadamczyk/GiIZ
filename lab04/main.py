"""
Główny plik do uruchomienia wszystkich zadań z laboratorium 4.
"""

import argparse
from lab04.zad1 import zad1
from lab04.zad2 import zad2
from lab04.zad3 import zad3
from lab04.zad4 import zad4, verify_specific_graph
from lab04.test_specific_graph import test_specific_graph

def main():
    """
    Główna funkcja uruchamiająca wszystkie zadania z laboratorium 4.
    """
    parser = argparse.ArgumentParser(description='Laboratorium 4 - Grafy skierowane i algorytmy grafowe')
    
    parser.add_argument('--n', type=int, default=7, help='Liczba wierzchołków digrafu')
    parser.add_argument('--p', type=float, default=0.4, help='Prawdopodobieństwo istnienia krawędzi')
    parser.add_argument('--min-weight', type=int, default=-5, help='Minimalna waga krawędzi')
    parser.add_argument('--max-weight', type=int, default=10, help='Maksymalna waga krawędzi')
    parser.add_argument('--s', type=int, default=0, help='Wierzchołek źródłowy')
    parser.add_argument('--interactive', action='store_true', help='Tryb interaktywny dla wykresów')
    parser.add_argument('--test-specific', action='store_true', help='Uruchom test dla konkretnego grafu z przykładu')
    parser.add_argument('--tasks', type=str, default='all', 
                      help='Zadania do uruchomienia (all, 1, 2, 3, 4 lub kombinacja, np. 1,3)')
    
    args = parser.parse_args()
    
    # Jeśli wybrano test konkretnego grafu, uruchom go i zakończ
    if args.test_specific:
        test_specific_graph()
        return
    
    # Określ, które zadania mają zostać uruchomione
    tasks_to_run = []
    if args.tasks == 'all':
        tasks_to_run = [1, 2, 3, 4]
    else:
        try:
            tasks_to_run = [int(task) for task in args.tasks.split(',')]
        except ValueError:
            print(f"Nieprawidłowy format zadań: {args.tasks}")
            return
    
    print("\n" + "="*50)
    print("Laboratorium 4 - Grafy skierowane i algorytmy grafowe")
    print("="*50)
    
    digraph = None
    
    # Zadanie 1: Generowanie losowego digrafu
    if 1 in tasks_to_run:
        print("\n" + "-"*50)
        print("Zadanie 1: Generowanie losowego digrafu")
        print("-"*50)
        
        digraph = zad1(args.n, args.p, args.interactive)
    
    # Zadanie 2: Znajdowanie silnie spójnych składowych
    if 2 in tasks_to_run:
        print("\n" + "-"*50)
        print("Zadanie 2: Znajdowanie silnie spójnych składowych")
        print("-"*50)
        
        components, is_sc = zad2(digraph, args.interactive)
    
    # Zadanie 3: Generowanie silnie spójnego digrafu z wagami i algorytm Bellmana-Forda
    if 3 in tasks_to_run:
        print("\n" + "-"*50)
        print("Zadanie 3: Silnie spójny digraf z wagami i algorytm Bellmana-Forda")
        print("-"*50)
        
        digraph, ds, ps = zad3(args.n, args.p, args.min_weight, args.max_weight, args.s, args.interactive)
    
    # Zadanie 4: Algorytm Johnsona
    if 4 in tasks_to_run:
        print("\n" + "-"*50)
        print("Zadanie 4: Algorytm Johnsona")
        print("-"*50)
        
        # Jeśli mamy już digraf z zadania 3, użyj go
        # W przeciwnym razie zad4 wygeneruje nowy
        distances, paths = zad4(digraph, args.interactive)
        
        # Dodatkowo weryfikujemy przykładowy graf z zadania
        if args.interactive:
            verify_specific_graph()
    
    print("\n" + "="*50)
    print("Koniec laboratorium 4")
    print("="*50)

if __name__ == "__main__":
    main() 