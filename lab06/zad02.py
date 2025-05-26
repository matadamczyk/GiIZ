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

def nearest_neighbor_heuristic(points, start=0):
    """Heurystyka najbliższego sąsiada"""
    n = len(points)
    unvisited = set(range(n))
    tour = [start]
    unvisited.remove(start)
    current = start
    
    while unvisited:
        nearest = min(unvisited, key=lambda x: distance(points[current], points[x]))
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    
    return tour

def random_tour_generator(points):
    """Generuje losową trasę"""
    tour = list(range(len(points)))
    random.shuffle(tour)
    return tour

def get_best_initial_solution(points, num_trials=10):
    """Znajdź najlepsze rozwiązanie początkowe spośród kilku prób"""
    best_tour = None
    best_distance = float('inf')
    
    # Próbuj różne punkty startowe dla nearest neighbor
    for start in range(min(num_trials, len(points))):
        tour = nearest_neighbor_heuristic(points, start)
        dist = total_distance(tour, points)
        if dist < best_distance:
            best_distance = dist
            best_tour = tour
    
    # Próbuj też kilka losowych rozwiązań
    for _ in range(num_trials):
        tour = random_tour_generator(points)
        dist = total_distance(tour, points)
        if dist < best_distance:
            best_distance = dist
            best_tour = tour
    
    return best_tour, best_distance

def simulated_annealing_advanced(points, T_start=10000.0, T_end=1e-10, 
                                cooling_schedule='exponential', max_iter=500000):
    """
    Zaawansowany algorytm symulowanego wyżarzania z różnymi strategiami chłodzenia
    """
    n = len(points)
    
    # Znajdź najlepsze rozwiązanie początkowe
    print("Szukanie najlepszego rozwiązania początkowego...")
    current, current_dist = get_best_initial_solution(points, num_trials=20)
    print(f"Najlepsze rozwiązanie początkowe: {current_dist:.3f}")
    
    best = current[:]
    best_dist = current_dist
    T = T_start
    
    accepted_moves = 0
    total_moves = 0
    improvements = 0
    
    # Historia dla analizy
    temperature_history = []
    distance_history = []
    
    for iteration in range(max_iter):
        if T < T_end:
            break
        
        # Wybór dwóch różnych pozycji dla operacji 2-opt
        i = random.randint(0, n - 1)
        k = random.randint(0, n - 1)
        
        # Upewnij się, że i < k i że są odpowiednio oddalone
        if i > k:
            i, k = k, i
        
        # Sprawdź czy pozycje są odpowiednio oddalone
        if k - i < 2:
            continue
            
        # Czasami wybierz punkty daleko od siebie dla większej eksploracji
        if random.random() < 0.3 and iteration < max_iter // 2:
            # W pierwszej połowie algorytmu preferuj większe zmiany
            min_distance = max(2, n // 10)
            max_distance = min(n // 2, n - 1)
            if k - i < min_distance:
                k = min(i + random.randint(min_distance, max_distance), n - 1)
        
        # Wykonanie operacji 2-opt
        new_tour = two_opt_swap(current, i, k)
        new_dist = total_distance(new_tour, points)
        
        delta = new_dist - current_dist
        total_moves += 1
        
        # Kryterium akceptacji Metropolisa
        accept = False
        if delta < 0:
            accept = True
            improvements += 1
        elif T > 0:
            probability = math.exp(-delta / T)
            if random.random() < probability:
                accept = True
        
        if accept:
            current = new_tour
            current_dist = new_dist
            accepted_moves += 1
            
            # Aktualizacja najlepszego rozwiązania
            if current_dist < best_dist:
                best = current[:]
                best_dist = current_dist
        
        # Strategia chłodzenia
        if cooling_schedule == 'exponential':
            alpha = 0.99995  # Bardzo wolne chłodzenie
            T *= alpha
        elif cooling_schedule == 'linear':
            T = T_start * (1 - iteration / max_iter)
        elif cooling_schedule == 'logarithmic':
            T = T_start / math.log(iteration + 2)
        
        # Zapisz historię
        if iteration % 1000 == 0:
            temperature_history.append(T)
            distance_history.append(best_dist)
        
        # Informacja o postępie
        if iteration % 50000 == 0:
            acceptance_rate = accepted_moves / max(total_moves, 1) * 100
            improvement_rate = improvements / max(total_moves, 1) * 100
            print(f"Iteracja {iteration}: T={T:.8f}, Najlepsza={best_dist:.3f}, "
                  f"Akceptacja={acceptance_rate:.1f}%, Poprawa={improvement_rate:.1f}%")
    
    print(f"Zakończono po {iteration + 1} iteracjach")
    print(f"Końcowa temperatura: {T:.10f}")
    print(f"Całkowita liczba ruchów: {total_moves}")
    print(f"Zaakceptowane ruchy: {accepted_moves}")
    print(f"Poprawy: {improvements}")
    
    return best, best_dist, temperature_history, distance_history

def multiple_runs_sa(points, num_runs=3):
    """Uruchom algorytm kilka razy i wybierz najlepszy wynik"""
    best_overall = None
    best_distance_overall = float('inf')
    all_results = []
    
    print(f"\n=== Uruchamianie {num_runs} niezależnych prób ===")
    
    for run in range(num_runs):
        print(f"\nPróba {run + 1}/{num_runs}")
        # Różne ziarna dla każdej próby
        random.seed(42 + run * 100)
        np.random.seed(42 + run * 100)
        
        # Różne parametry dla różnorodności
        T_start = random.uniform(8000, 12000)
        max_iter = random.randint(400000, 600000)
        
        tour, distance, temp_hist, dist_hist = simulated_annealing_advanced(
            points, 
            T_start=T_start,
            max_iter=max_iter
        )
        
        all_results.append((tour, distance))
        print(f"Wynik próby {run + 1}: {distance:.3f}")
        
        if distance < best_distance_overall:
            best_distance_overall = distance
            best_overall = tour
    
    print(f"\nNajlepszy wynik ze wszystkich prób: {best_distance_overall:.3f}")
    return best_overall, best_distance_overall, all_results

def plot_comparison(points, initial_tour, best_tour):
    """Porównanie cyklu początkowego i wyjściowego"""
    
    # Oblicz długości tras
    initial_dist = total_distance(initial_tour, points)
    best_dist = total_distance(best_tour, points)
    
    # Utwórz subplot z 2 wykresami
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    tours_data = [
        (initial_tour, initial_dist, "Cykl początkowy", "red"), 
        (best_tour, best_dist, "Cykl wyjściowy", "red")
    ]
    
    for i, (tour, distance, title, color) in enumerate(tours_data):
        # Współrzędne trasy
        x_coords = [points[j][0] for j in tour] + [points[tour[0]][0]]
        y_coords = [points[j][1] for j in tour] + [points[tour[0]][1]]
        
        # Rysowanie trasy
        axes[i].plot(x_coords, y_coords, 'o-', color=color, markersize=3, linewidth=1.5, alpha=0.8)
        
        # Rysowanie wszystkich punktów
        axes[i].scatter([points[j][0] for j in range(len(points))], 
                       [points[j][1] for j in range(len(points))], 
                       c='red', s=15, zorder=5, alpha=0.7)
        
        axes[i].set_title(f"({chr(97+i)}) {title}. Długość cyklu: {distance:.3f}")
        axes[i].set_xlabel("x")
        axes[i].set_ylabel("y")
        axes[i].grid(True, alpha=0.3)
        axes[i].set_aspect('equal')
    
    plt.tight_layout()
    plt.show()


# Główny program
if __name__ == "__main__":
    # Wczytanie danych
    filename = "xqf131.dat"
    points = load_points(filename)
    
    if not points:
        print("Nie udało się wczytać danych.")
        exit(1)
    
    print(f"Wczytano {len(points)} punktów z pliku {filename}")
    
    # Cykl początkowy - losowy (jak na obrazku a)
    random.seed(42)
    initial_tour = random_tour_generator(points)
    initial_distance = total_distance(initial_tour, points)
    print(f"Cykl początkowy (losowy): {initial_distance:.3f}")
    
    # Pojedyncze uruchomienie symulowanego wyżarzania
    print("\n=== Uruchamianie symulowanego wyżarzania ===")
    best_tour, best_distance, temp_hist, dist_hist = simulated_annealing_advanced(points)
    
    print(f"\n=== KOŃCOWE WYNIKI ===")
    print(f"Cykl początkowy: {initial_distance:.3f}")
    print(f"Cykl wyjściowy: {best_distance:.3f}")
    print(f"Poprawa: {initial_distance - best_distance:.3f}")
    print(f"Oczekiwany wynik (z obrazka): 567.203")
    print(f"Różnica od oczekiwanego: {abs(best_distance - 567.203):.3f}")
    
    # Wizualizacja porównania
    print("\nGenerowanie wizualizacji...")
    plot_comparison(points, initial_tour, best_tour)