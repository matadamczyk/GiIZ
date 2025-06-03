"""
Główny plik do uruchomienia wszystkich zadań z laboratorium 4 (wersja prezentacyjna).
"""

from zad1 import zad1
from zad2 import zad2
from zad3 import zad3
from zad4 import zad4

def main():
    """
    Główna funkcja uruchamiająca wszystkie zadania z laboratorium 4.
    """
    print("\n" + "="*50)
    print("Laboratorium 4 - Grafy skierowane i algorytmy grafowe")
    print("="*50)
    
    digraph = None
    
    print("\n" + "-"*50)
    print("Zadanie 1: Generowanie losowego digrafu")
    print("-"*50)
    
    digraph = zad1()
    
    print("\n" + "-"*50)
    print("Zadanie 2: Znajdowanie silnie spójnych składowych")
    print("-"*50)
    
    components, is_sc = zad2(digraph)
    
    print("\n" + "-"*50)
    print("Zadanie 3: Silnie spójny digraf z wagami i algorytm Bellmana-Forda")
    print("-"*50)
    
    digraph, ds, ps = zad3()
    
    print("\n" + "-"*50)
    print("Zadanie 4: Algorytm Johnsona")
    print("-"*50)
    
    distances, paths = zad4(digraph)
    
    print("\n" + "="*50)
    print("Koniec laboratorium 4")
    print("="*50)

if __name__ == "__main__":
    main() 