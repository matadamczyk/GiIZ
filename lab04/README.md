# Laboratorium 4 - Grafy skierowane i algorytmy grafowe

Ten projekt implementuje podstawowe algorytmy dla grafów skierowanych (digrafów).

## Zaimplementowane algorytmy

1. **Generowanie losowego digrafu** - z zespołu G(n, p)
2. **Algorytm Kosaraju** - znajdowanie silnie spójnych składowych
3. **Algorytm Bellmana-Forda** - najkrótsze ścieżki z obsługą ujemnych wag
4. **Algorytm Johnsona** - najkrótsze ścieżki między wszystkimi parami wierzchołków

## Struktura plików

- `digraph_representation.py` - Klasa DiGraph z różnymi reprezentacjami
- `random_digraph.py` - Generatory losowych digrafów
- `kosaraju.py` - Algorytm Kosaraju
- `bellman_ford.py` - Algorytm Bellmana-Forda
- `johnson.py` - Algorytm Johnsona
- `digraph_visualization.py` - Wizualizacja digrafów
- `zad1.py` - Zadanie 1: Generator losowych digrafów
- `zad2.py` - Zadanie 2: Silnie spójne składowe
- `zad3.py` - Zadanie 3: Digraf z wagami + Bellman-Ford
- `zad4.py` - Zadanie 4: Algorytm Johnsona
- `main.py` - Główny plik uruchamiający wszystkie zadania

## Uruchomienie

### Pojedyncze zadania

```bash
cd lab04
python3 zad1.py    # Zadanie 1
python3 zad2.py    # Zadanie 2
python3 zad3.py    # Zadanie 3
python3 zad4.py    # Zadanie 4
```

### Wszystkie zadania naraz

```bash
cd lab04
python3 main.py    # Uruchom wszystkie zadania
```

## Funkcjonalności

### Klasa DiGraph

- Obsługa trzech reprezentacji: macierz sąsiedztwa, lista sąsiedztwa, macierz incydencji
- Automatyczna synchronizacja między reprezentacjami
- Obsługa wag krawędzi
- Transpozycja grafu

### Generatory

- Losowy digraf G(n, p)
- Losowy silnie spójny digraf z wagami
- Automatyczne usuwanie cykli o ujemnej sumie wag

### Wizualizacja

- Rysowanie digrafów z strzałkami
- Kolorowanie silnie spójnych składowych
- Wyświetlanie wag krawędzi
- Obsługa krawędzi dwukierunkowych (łuki)

### Algorytmy

- **Kosaraju**: O(V + E) - silnie spójne składowe
- **Bellman-Ford**: O(VE) - najkrótsze ścieżki z wykrywaniem ujemnych cykli
- **Johnson**: O(V²logV + VE) - wszystkie pary najkrótszych ścieżek

## Uwagi techniczne

### Parametry do prezentacji

Wszystkie zadania używają ustawionych na stałe parametrów optymalnych do prezentacji:

- Liczba wierzchołków: 7
- Prawdopodobieństwo krawędzi: 0.4-0.5
- Wagi krawędzi: od -5 do 10
- Wierzchołek źródłowy: 0

### Obsługa ujemnych cykli

Algorytmy automatycznie wykrywają i eliminują cykle o ujemnej sumie wag:

- Bellman-Ford zgłasza obecność takich cykli
- Johnson kończy działanie jeśli wykryje ujemny cykl
- Generator silnie spójnych digrafów modyfikuje wagi, aby uniknąć ujemnych cykli
