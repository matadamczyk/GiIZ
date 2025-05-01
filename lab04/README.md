# Laboratorium 4: Grafy Skierowane i Algorytmy

Pakiet zawiera implementacje i wizualizacje algorytmów dla grafów skierowanych (digrafów), takich jak algorytm Kosaraju do znajdowania silnie spójnych składowych, algorytm Bellmana-Forda do znajdowania najkrótszych ścieżek w grafie z ujemnymi wagami oraz algorytm Johnsona do znajdowania najkrótszych ścieżek między wszystkimi parami wierzchołków.

## Spis treści

1. [Struktura projektu](#struktura-projektu)
2. [Instalacja i uruchomienie](#instalacja-i-uruchomienie)
3. [Opis zadań](#opis-zadań)
4. [Przykład użycia](#przykład-użycia)

## Struktura projektu

```
lab04/
├── __init__.py                    # Deklaracja pakietu
├── digraph_representation.py      # Klasa DiGraph - reprezentacja grafu skierowanego
├── digraph_visualization.py       # Funkcje do wizualizacji grafów skierowanych
├── random_digraph.py              # Generator losowych digrafów
├── kosaraju.py                    # Implementacja algorytmu Kosaraju
├── bellman_ford.py                # Implementacja algorytmu Bellmana-Forda
├── johnson.py                     # Implementacja algorytmu Johnsona
├── zad1.py                        # Zadanie 1: Generowanie losowego digrafu
├── zad2.py                        # Zadanie 2: Znajdowanie silnie spójnych składowych
├── zad3.py                        # Zadanie 3: Algorytm Bellmana-Forda
├── zad4.py                        # Zadanie 4: Algorytm Johnsona
├── test_specific_graph.py         # Testy na konkretnym grafie z przykładu
└── main.py                        # Główny plik uruchamiający wszystkie zadania
```

## Instalacja i uruchomienie

Aby uruchomić projekt, należy mieć zainstalowanego Pythona 3.6+ oraz biblioteki:

- matplotlib
- numpy

Uruchomienie wszystkich zadań:

```
python -m lab04.main --interactive
```

Uruchomienie testu dla konkretnego grafu z przykładu:

```
python -m lab04.main --test-specific
```

Uruchomienie wybranych zadań:

```
python -m lab04.main --tasks 1,3 --n 10 --p 0.5
```

## Opis zadań

### Zadanie 1: Generowanie losowego digrafu

Implementacja generatora losowych grafów skierowanych z zespołu G(n, p), gdzie n to liczba wierzchołków, a p to prawdopodobieństwo istnienia krawędzi między dowolną parą wierzchołków.

### Zadanie 2: Algorytm Kosaraju

Implementacja algorytmu Kosaraju do znajdowania silnie spójnych składowych w grafie skierowanym. Algorytm wykorzystuje dwa przeszukiwania w głąb (DFS).

### Zadanie 3: Generowanie silnie spójnego digrafu i algorytm Bellmana-Forda

Generowanie losowego silnie spójnego digrafu z losowymi wagami krawędzi z zakresu [-5, 10] oraz implementacja algorytmu Bellmana-Forda do znajdowania najkrótszych ścieżek od danego wierzchołka. Algorytm potrafi obsługiwać krawędzie o ujemnych wagach.

### Zadanie 4: Algorytm Johnsona

Implementacja algorytmu Johnsona do znajdowania najkrótszych ścieżek między wszystkimi parami wierzchołków w grafie skierowanym. Algorytm może obsługiwać krawędzie o ujemnych wagach, o ile w grafie nie ma cyklu o ujemnej sumie wag.

## Przykład użycia

```python
from lab04.digraph_representation import DiGraph
from lab04.bellman_ford import bellman_ford, get_path

# Tworzenie grafu
digraph = DiGraph(4)
digraph.add_edge(0, 1, 3)   # Krawędź 0->1 o wadze 3
digraph.add_edge(0, 2, -2)  # Krawędź 0->2 o wadze -2
digraph.add_edge(1, 3, 5)   # Krawędź 1->3 o wadze 5
digraph.add_edge(2, 1, 4)   # Krawędź 2->1 o wadze 4
digraph.add_edge(2, 3, 1)   # Krawędź 2->3 o wadze 1

# Uruchomienie algorytmu Bellmana-Forda od wierzchołka 0
ds, ps, has_negative_cycle = bellman_ford(digraph, 0)

if not has_negative_cycle:
    # Wypisanie najkrótszych ścieżek
    for v in range(digraph.V):
        path = get_path(ps, 0, v)
        if path:
            path_str = " -> ".join(str(node) for node in path)
            print(f"Najkrótsza ścieżka od 0 do {v}: [{path_str}], odległość = {ds[v]}")
        else:
            print(f"Brak ścieżki od 0 do {v}")
else:
    print("Wykryto cykl o ujemnej sumie wag!")
```
