import numpy as np
import random
import math
import matplotlib.pyplot as plt

def load_points(filename):
    """Wczytanie punktów z pliku"""
    points = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    x, y = map(float, line.split())
                    points.append((x, y))
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {filename}")
        return []
    return points

def distance(p1, p2):
    """Obliczanie odległości euklidesowej między dwoma punktami"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def total_distance(tour, points):
    """Obliczanie całkowitej długości cyklu"""
    total = 0
    n = len(tour)
    for i in range(n):
        total += distance(points[tour[i]], points[tour[(i + 1) % n]])
    return total

def two_opt_swap(tour, i, k):
    """Operacja 2-opt: odwrócenie fragmentu trasy między pozycjami i a k"""
    new_tour = tour[:]
    new_tour[i:k+1] = reversed(new_tour[i:k+1])
    return new_tour

def nearest_neighbor_heuristic(points):
    """Heurystyka najbliższego sąsiada dla lepszego rozwiązania początkowego"""
    n = len(points)
    unvisited = set(range(1, n))
    tour = [0]  # Zaczynamy od punktu 0
    current = 0
    
    while unvisited:
        nearest = min(unvisited, key=lambda x: distance(points[current], points[x]))
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    
    return tour

def simulated_annealing(points, T_start=1000.0, T_end=1e-6, alpha=0.99, max_iter=100000):
    """
    Algorytm symulowanego wyżarzania dla TSP
    Używa operacji 2-opt zgodnie z algorytmem Metropolisa-Hastingsa
    """
    n = len(points)
    
    # Lepsze rozwiązanie początkowe - heurystyka najbliższego sąsiada
    current = nearest_neighbor_heuristic(points)
    current_dist = total_distance(current, points)
    
    best = current[:]
    best_dist = current_dist
    T = T_start
    
    accepted_moves = 0
    total_moves = 0
    
    for iteration in range(max_iter):
        if T < T_end:
            break
            
        # Losowy wybór dwóch pozycji dla operacji 2-opt
        i = random.randint(0, n - 1)
        k = random.randint(0, n - 1)
        
        # Upewniamy się, że i < k i że są odpowiednio oddalone
        if i > k:
            i, k = k, i
        if k - i < 2:
            continue
            
        # Wykonanie operacji 2-opt
        new_tour = two_opt_swap(current, i, k)
        new_dist = total_distance(new_tour, points)
        
        delta = new_dist - current_dist
        total_moves += 1
        
        # Kryterium akceptacji Metropolisa
        if delta < 0 or (T > 0 and random.random() < math.exp(-delta / T)):
            current = new_tour
            current_dist = new_dist
            accepted_moves += 1
            
            # Aktualizacja najlepszego rozwiązania
            if current_dist < best_dist:
                best = current[:]
                best_dist = current_dist
        
        # Schładzanie
        T *= alpha
        
        # Informacja o postępie co 10000 iteracji
        if iteration % 10000 == 0:
            acceptance_rate = accepted_moves / max(total_moves, 1) * 100
            print(f"Iteracja {iteration}: T={T:.6f}, Najlepsza długość={best_dist:.3f}, "
                  f"Akceptacja={acceptance_rate:.1f}%")
    
    print(f"Zakończono po {iteration + 1} iteracjach")
    print(f"Końcowa temperatura: {T:.6f}")
    print(f"Całkowita liczba ruchów: {total_moves}")
    print(f"Zaakceptowane ruchy: {accepted_moves}")
    
    return best, best_dist

def plot_tour(points, tour, title="Cykl Hamiltona"):
    """Wizualizacja znalezionego cyklu"""
    if not points or not tour:
        print("Brak danych do wyświetlenia")
        return
        
    x_coords = [points[i][0] for i in tour] + [points[tour[0]][0]]
    y_coords = [points[i][1] for i in tour] + [points[tour[0]][1]]
    
    plt.figure(figsize=(12, 8))
    plt.plot(x_coords, y_coords, 'o-', color='red', markersize=4, linewidth=1)
    plt.scatter([points[i][0] for i in range(len(points))], 
                [points[i][1] for i in range(len(points))], 
                c='blue', s=20, zorder=5)
    
    plt.title(f"{title}\nDługość cyklu: {total_distance(tour, points):.3f}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def compare_initial_solutions(points):
    """Porównanie różnych rozwiązań początkowych"""
    print("\n=== Porównanie rozwiązań początkowych ===")
    
    # Rozwiązanie losowe
    random_tour = list(range(len(points)))
    random.shuffle(random_tour)
    random_dist = total_distance(random_tour, points)
    print(f"Rozwiązanie losowe: {random_dist:.3f}")
    
    # Heurystyka najbliższego sąsiada
    nn_tour = nearest_neighbor_heuristic(points)
    nn_dist = total_distance(nn_tour, points)
    print(f"Najbliższy sąsiad: {nn_dist:.3f}")
    
    return random_tour, nn_tour

# Główny program
if __name__ == "__main__":
    # Ustawienie ziarna dla powtarzalności
    random.seed(42)
    np.random.seed(42)
    
    # Wczytanie danych
    filename = "xqf131.dat"  # Zgodnie z poleceniem
    points = load_points(filename)
    
    if not points:
        print("Nie udało się wczytać danych. Sprawdź czy plik xqf131.dat istnieje.")
        exit(1)
    
    print(f"Wczytano {len(points)} punktów z pliku {filename}")
    
    # Porównanie rozwiązań początkowych
    random_tour, nn_tour = compare_initial_solutions(points)
    
    print("\n=== Symulowane wyżarzanie ===")
    
    # Algorytm symulowanego wyżarzania z lepszymi parametrami
    best_tour, best_distance = simulated_annealing(
        points, 
        T_start=1000.0,    # Wyższa temperatura początkowa
        T_end=1e-8,        # Niższa temperatura końcowa
        alpha=0.9995,      # Wolniejsze chłodzenie
        max_iter=200000    # Więcej iteracji
    )
    
    print(f"\n=== WYNIKI ===")
    print(f"Najkrótsza znaleziona droga: {best_distance:.3f}")
    print(f"Kolejność odwiedzin: {best_tour}")
    
    # Wizualizacja wyników
    plot_tour(points, best_tour, "Najlepszy cykl znaleziony przez symulowane wyżarzanie")
    
    # Dodatkowa wizualizacja porównawcza
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Cykl początkowy (najbliższy sąsiad)
    x1 = [points[i][0] for i in nn_tour] + [points[nn_tour[0]][0]]
    y1 = [points[i][1] for i in nn_tour] + [points[nn_tour[0]][1]]
    ax1.plot(x1, y1, 'o-', color='blue', markersize=3, linewidth=1)
    ax1.set_title(f"Cykl początkowy\nDługość: {total_distance(nn_tour, points):.3f}")
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # Najlepszy cykl
    x2 = [points[i][0] for i in best_tour] + [points[best_tour[0]][0]]
    y2 = [points[i][1] for i in best_tour] + [points[best_tour[0]][1]]
    ax2.plot(x2, y2, 'o-', color='red', markersize=3, linewidth=1)
    ax2.set_title(f"Cykl wyjściowy\nDługość: {best_distance:.3f}")
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    plt.tight_layout()
    plt.show()