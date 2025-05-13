# Laboratorium 3: Algorytmy Grafowe

Pakiet zawiera implementacje i wizualizacje klasycznych algorytmów grafowych, takich jak algorytm Dijkstry, znajdowanie centrum grafu oraz minimalne drzewo rozpinające.

## Spis treści

1. [Struktura projektu](#struktura-projektu)
2. [Instalacja i uruchomienie](#instalacja-i-uruchomienie)
3. [Opis zadań](#opis-zadań)
4. [Przykład użycia](#przykład-użycia)

## Struktura projektu

```
lab03/
├── __init__.py                 # Deklaracja pakietu
├── graph_representation.py     # Klasa Graph - reprezentacja grafu ważonego
├── graph_visualization.py      # Funkcje do wizualizacji grafów
├── random_weighted_graph.py    # Generator losowych grafów spójnych
├── zad1.py                     # Zadanie 1: Generowanie grafu losowego
├── zad2.py                     # Zadanie 2: Algorytm Dijkstry
├── zad3.py                     # Zadanie 3: Macierz odległości
├── zad4.py                     # Zadanie 4: Centrum grafu i centrum minimax
├── zad5.py                     # Zadanie 5: Minimalne drzewo rozpinające
├── test_specific_graph.py      # Testy na konkretnym grafie
└── main.py                     # Główny plik uruchamiający wszystkie zadania
```

## Instalacja i uruchomienie

Aby uruchomić projekt, należy mieć zainstalowanego Pythona 3.6+ oraz biblioteki:

- matplotlib
- numpy
- networkx (opcjonalnie, do wizualizacji)

Uruchomienie wszystkich zadań:

```
python3 main.py
```

Uruchomienie testu na konkretnym grafie:

```
python3 test_specific_graph.py
```

## Opis zadań

### Zadanie 1: Generowanie grafu losowego

Implementacja generatora losowych grafów spójnych z losowymi wagami krawędzi.

### Zadanie 2: Algorytm Dijkstry

Implementacja algorytmu Dijkstry do znajdowania najkrótszych ścieżek od wybranego wierzchołka źródłowego do wszystkich innych wierzchołków w grafie.

### Zadanie 3: Macierz odległości

Obliczanie macierzy odległości między wszystkimi parami wierzchołków w grafie.

### Zadanie 4: Centrum grafu

Znajdowanie centrum grafu (wierzchołek o najmniejszej sumie odległości do pozostałych wierzchołków) oraz centrum minimax (wierzchołek o najmniejszej maksymalnej odległości do najdalszego wierzchołka).

### Zadanie 5: Minimalne drzewo rozpinające

Implementacja algorytmów Prima i Kruskala do znajdowania minimalnego drzewa rozpinającego grafu.

## Przykład użycia

```python
from lab03.graph_representation import Graph
from lab03.zad2 import dijkstra, get_path

# Tworzenie grafu
graph = Graph(5)  # Graf z 5 wierzchołkami
graph.add_edge(0, 1, 3)  # Dodajemy krawędź między wierzchołkami 0 i 1 o wadze 3
graph.add_edge(0, 2, 1)
graph.add_edge(1, 2, 7)
graph.add_edge(1, 3, 5)
graph.add_edge(1, 4, 1)
graph.add_edge(2, 3, 2)
graph.add_edge(3, 4, 7)

# Uruchomienie algorytmu Dijkstry od wierzchołka 0
distances, predecessors = dijkstra(graph, 0)

# Wypisanie najkrótszych ścieżek
for v in range(graph.V):
    path = get_path(predecessors, 0, v)
    if path:
        print(f"Najkrótsza ścieżka od 0 do {v}: {path}, odległość = {distances[v]}")
```
