import random
import numpy as np
from collections import defaultdict

def build_graph(adj_list):
    """
    KROK 1: Budowanie struktury grafu z listy sąsiedztwa
    - Tworzymy słownik graph gdzie każdy węzeł ma listę swoich sąsiadów
    - Zbieramy wszystkie węzły w zbiorze nodes
    """
    graph = defaultdict(list)
    nodes = set()
    for u, vs in adj_list.items():
        for v in vs:
            graph[u].append(v)  # Dodajemy krawędź u -> v
            nodes.update([u, v])  # Dodajemy oba węzły do zbioru
    return graph, list(nodes)

def pagerank_random_walk(graph, nodes, d=0.15, steps=1_000_000):
    """
    METODA (A): PageRank przez błądzenie przypadkowe z teleportacją
    
    ALGORYTM:
    1. Zaczynamy od losowego węzła
    2. W każdym kroku:
       - Z prawdopodobieństwem d: teleportujemy się losowo (restart)
       - Z prawdopodobieństwem (1-d): idziemy do losowego sąsiada
    3. Zliczamy odwiedziny każdego węzła
    4. PageRank = częstość odwiedzin
    """
    print("=== ROZPOCZYNAMY BŁĄDZENIE PRZYPADKOWE ===")
    visits = defaultdict(int)  # Licznik odwiedzin każdego węzła
    node = random.choice(nodes)  # Losowy węzeł startowy
    print(f"Startujemy z węzła: {node}")
    
    for step in range(steps):
        if random.random() < d or not graph[node]:
            # TELEPORTACJA
            node = random.choice(nodes)
            if step % 100000 == 0:
                print(f"Krok {step}: TELEPORTACJA do węzła {node}")
        else:
            # PRZEJŚCIE DO SĄSIADA
            node = random.choice(graph[node])
            if step % 100000 == 0:
                print(f"Krok {step}: Przejście do sąsiada {node}")
        
        visits[node] += 1
    
    total = sum(visits.values())
    pagerank_scores = {k: v / total for k, v in visits.items()}
    
    print(f"=== ZAKOŃCZONO PO {steps} KROKACH ===")
    return pagerank_scores

def pagerank_power_iteration(graph, nodes, d=0.15, max_iter=100, tolerance=1e-6):
    """
    METODA (B): PageRank przez iterację wektora obsadzeń
    
    ALGORYTM:
    1. Budujemy macierz przejścia P = (1-d)*A + (d/n)*J
    2. Zaczynamy od wektora p_0 = (1/n, ..., 1/n)
    3. Iterujemy: p_{t+1} = P * p_t
    4. Kończymy gdy ||p_{t+1} - p_t|| < tolerance
    """
    print("=== ROZPOCZYNAMY ITERACJĘ WEKTORA OBSADZEŃ ===")
    n = len(nodes)
    index = {node: i for i, node in enumerate(nodes)}  # Mapowanie węzeł -> indeks
    
    print(f"Liczba węzłów: {n}")
    print("KROK 1: Budowanie macierzy przejścia A")
    
    # BUDOWA MACIERZY PRZEJŚCIA A
    A = np.zeros((n, n))
    for node in nodes:
        j = index[node]  # Kolumna (węzeł źródłowy)
        neighbors = graph[node]  # Sąsiedzi węzła
        
        if neighbors:
            # Węzeł ma wychodzące krawędzie
            print(f"  Węzeł {node} -> {len(neighbors)} sąsiadów: {neighbors}")
            for neighbor in neighbors:
                i = index[neighbor]  # Wiersz (węzeł docelowy)
                A[i, j] = 1 / len(neighbors)  # Równomierne prawdopodobieństwo
        else:
            # Węzeł nie ma wychodzących krawędzi - "teleportacja" do wszystkich
            print(f"  Węzeł {node} -> brak sąsiadów, równomierne rozłożenie")
            for i in range(n):
                A[i, j] = 1 / n
    
    print("KROK 2: Obliczanie macierzy PageRank P = (1-d)*A + (d/n)*J")
    # MACIERZ PAGERANK: P = (1-d)*A + (d/n)*J
    # J = macierz jedynek (reprezentuje teleportację)
    P = (1 - d) * A + d / n * np.ones((n, n))
    
    print("KROK 3: Iteracje wektora obsadzeń")
    # WEKTOR POCZĄTKOWY: równomierne rozłożenie
    p = np.ones(n) / n
    print(f"Wektor początkowy p_0 = [{', '.join([f'{x:.3f}' for x in p[:5]])}...]")
    
    # ITERACJE
    for iteration in range(max_iter):
        p_new = P @ p  # Mnożymy macierz P przez wektor p
        
        # SPRAWDZENIE ZBIEŻNOŚCI
        difference = np.linalg.norm(p_new - p, 1)  # Norma L1
        print(f"  Iteracja {iteration + 1}: różnica = {difference:.8f}")
        
        if difference < tolerance:
            print(f"=== ZBIEŻNOŚĆ OSIĄGNIĘTA PO {iteration + 1} ITERACJACH ===")
            break
        
        p = p_new  # Aktualizujemy wektor
    
    # KONWERSJA Z WEKTORA NA SŁOWNIK
    return {nodes[i]: p[i] for i in range(n)}

def print_results(rank, method_name):
    """
    WYŚWIETLANIE WYNIKÓW: Sortowanie malejąco według wartości PageRank
    """
    print(f"\n=== WYNIKI: {method_name} ===")
    sorted_rank = sorted(rank.items(), key=lambda x: x[1], reverse=True)
    
    for i, (node, value) in enumerate(sorted_rank, 1):
        print(f"{i:2d}. Węzeł {node} ==> PageRank = {value:.5f}")

def main():
  print("=== INICJALIZACJA DANYCH ===")
  adj_list = {
      'A': ['E', 'F', 'I'], 
      'B': ['A', 'C', 'F'],    
      'C': ['B', 'D', 'E', 'L'],
      'D': ['C', 'E', 'H', 'I', 'K'],  
      'E': ['C', 'G', 'H', 'I'],  
      'F': ['B', 'G'],      
      'G': ['E', 'F', 'H'],   
      'H': ['D', 'G', 'I', 'L'],
      'I': ['D', 'E', 'H', 'J'], 
      'J': ['I'],               
      'K': ['D', 'I'],           
      'L': ['A', 'H'],           
  }

  # BUDOWANIE STRUKTURY GRAFU
  graph, nodes = build_graph(adj_list)
  print(f"Graf zawiera {len(nodes)} węzłów: {sorted(nodes)}")

  # USTAWIENIE ZIARNA DLA POWTARZALNOŚCI WYNIKÓW
  random.seed(42)
  np.random.seed(42)
  print("Ustawiono ziarno losowości na 42 dla powtarzalnych wyników")

  print("\n" + "="*60)
  print("METODA (A): BŁĄDZENIE PRZYPADKOWE Z TELEPORTACJĄ")
  print("="*60)
  rank_a = pagerank_random_walk(graph, nodes, d=0.15, steps=1_000_000)

  print("\n" + "="*60)
  print("METODA (B): ITERACJA WEKTORA OBSADZEŃ") 
  print("="*60)
  rank_b = pagerank_power_iteration(graph, nodes, d=0.15, max_iter=100)

  print_results(rank_a, "METODA A - Błądzenie przypadkowe (N=1,000,000 kroków)")
  print_results(rank_b, "METODA B - Iteracja wektora obsadzeń")

  print("\n" + "="*60)
  print("PORÓWNANIE WYNIKÓW OBU METOD")
  print("="*60)
  print(f"{'Węzeł':<5} {'Metoda A':<12} {'Metoda B':<12} {'Różnica':<10}")
  print("-" * 45)
  for node in sorted(nodes):
      diff = abs(rank_a[node] - rank_b[node])
      print(f"{node:<5} {rank_a[node]:<12.5f} {rank_b[node]:<12.5f} {diff:<10.5f}")

if __name__ == "__main__":
    main()