import numpy as np
import random
import math
import matplotlib.pyplot as plt

def load_points(filename):
    """
    KROK 1: Wczytywanie punktów z pliku
    """
    print(f"=== WCZYTYWANIE DANYCH Z PLIKU {filename} ===")
    points = []
    try:
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    x, y = map(float, line.split())
                    points.append((x, y))
                    if line_num <= 5:
                        print(f"  Punkt {line_num}: ({x:.2f}, {y:.2f})")
        print(f"Wczytano {len(points)} punktów")
    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku {filename}")
        return []
    return points

def distance(p1, p2):
    """
    OBLICZANIE ODLEGŁOŚCI EUKLIDESOWEJ między dwoma punktami
    d = sqrt((x1-x2)² + (y1-y2)²)
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def total_distance(tour, points):
    """
    OBLICZANIE CAŁKOWITEJ DŁUGOŚCI CYKLU (trasy TSP)
    Sumujemy odległości między kolejnymi punktami w trasie
    + odległość z ostatniego punktu z powrotem do pierwszego
    """
    total = 0
    n = len(tour)
    for i in range(n):
        # Dodajemy odległość od punktu i do punktu (i+1) mod n
        current_point = points[tour[i]]
        next_point = points[tour[(i + 1) % n]]  # % n zapewnia powrót do początku
        dist = distance(current_point, next_point)
        total += dist
    return total

def two_opt_swap(tour, i, k):
    """
    OPERACJA 2-OPT: Odwrócenie fragmentu trasy między pozycjami i a k
    """
    new_tour = tour[:]  # Kopia oryginalnej trasy
    new_tour[i:k+1] = reversed(new_tour[i:k+1])  # Odwracamy fragment
    return new_tour

def nearest_neighbor_heuristic(points, start=0):
    """
    HEURYSTYKA NAJBLIŻSZEGO SĄSIADA - tworzy dobre rozwiązanie początkowe
    
    ALGORYTM:
    1. Zacznij od punktu startowego
    2. W każdym kroku idź do najbliższego nieodwiedzonego punktu
    3. Kontynuuj aż odwiedzisz wszystkie punkty
    """
    n = len(points)
    unvisited = set(range(n))
    tour = [start]
    unvisited.remove(start)
    current = start
    
    while unvisited:
        # Znajdujemy najbliższy nieodwiedzony punkt
        nearest = min(unvisited, key=lambda x: distance(points[current], points[x]))
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    
    return tour

def random_tour_generator(points):
    """
    GENERATOR LOSOWEJ TRASY - dla różnorodności rozwiązań początkowych
    """
    tour = list(range(len(points)))
    random.shuffle(tour)
    return tour

def get_best_initial_solution(points, num_trials=10):
    """
    ZNAJDOWANIE NAJLEPSZEGO ROZWIĄZANIA POCZĄTKOWEGO
    Próbujemy różne metody i wybieramy najlepszą trasę
    """
    print("--- Szukanie najlepszego rozwiązania początkowego ---")
    best_tour = None
    best_distance = float('inf')
    
    # PRÓBA 1: Różne punkty startowe dla heurystyki najbliższego sąsiada
    print("Testowanie heurystyki najbliższego sąsiada...")
    for start in range(min(num_trials, len(points))):
        tour = nearest_neighbor_heuristic(points, start)
        dist = total_distance(tour, points)
        print(f"  Start z punktu {start}: długość = {dist:.3f}")
        if dist < best_distance:
            best_distance = dist
            best_tour = tour
    
    # PRÓBA 2: Losowe rozwiązania
    print("Testowanie losowych rozwiązań...")
    for trial in range(num_trials):
        tour = random_tour_generator(points)
        dist = total_distance(tour, points)
        if trial < 3:
            print(f"  Losowa trasa {trial + 1}: długość = {dist:.3f}")
        if dist < best_distance:
            best_distance = dist
            best_tour = tour
    
    print(f"Najlepsze rozwiązanie początkowe: {best_distance:.3f}")
    return best_tour, best_distance

def simulated_annealing_advanced(points, T_start=10000.0, T_end=1e-10, 
                                cooling_schedule='exponential', max_iter=500000):
    """
    ALGORYTM SYMULOWANEGO WYŻARZANIA
    
    PARAMETRY:
    - T_start: temperatura początkowa (wysoka = akceptujemy złe ruchy)
    - T_end: temperatura końcowa (niska = akceptujemy tylko dobre ruchy)
    - max_iter: maksymalna liczba iteracji
    
    ALGORYTM:
    1. Zacznij od rozwiązania początkowego
    2. W każdej iteracji:
       a) Wykonaj operację 2-opt (zmień trasę)
       b) Oblicz zmianę długości trasy (Δ)
       c) Jeśli Δ < 0: zaakceptuj (poprawa)
       d) Jeśli Δ ≥ 0: zaakceptuj z prawdopodobieństwem exp(-Δ/T)
    3. Stopniowo zmniejszaj temperaturę T
    """
    print("=== ROZPOCZYNAMY SYMULOWANE WYŻARZANIE ===")
    n = len(points)
    
    # KROK 1: Znajdujemy najlepsze rozwiązanie początkowe
    current, current_dist = get_best_initial_solution(points, num_trials=20)
    print(f"Rozwiązanie początkowe: {current_dist:.3f}")
    
    # INICJALIZACJA ZMIENNYCH
    best = current[:]  # Najlepsza trasa dotychczas
    best_dist = current_dist  # Najlepsza długość dotychczas
    T = T_start  # Temperatura bieżąca
    
    # STATYSTYKI
    accepted_moves = 0  # Liczba zaakceptowanych ruchów
    total_moves = 0     # Liczba wszystkich ruchów
    improvements = 0    # Liczba ulepszeń
    
    # Historia dla analizy
    temperature_history = []
    distance_history = []
    
    print(f"Parametry: T_start={T_start}, T_end={T_end}, max_iter={max_iter}")
    print("Rozpoczynamy iteracje...")
    
    # GŁÓWNA PĘTLA ALGORYTMU
    for iteration in range(max_iter):
        if T < T_end:
            print(f"Osiągnięto temperaturę końcową T={T:.2e}")
            break
        
        # KROK 1: Wybieramy dwie pozycje dla operacji 2-opt
        i = random.randint(0, n - 1)
        k = random.randint(0, n - 1)
        
        # Upewniamy się, że i < k i że są odpowiednio oddalone
        if i > k:
            i, k = k, i
        
        if k - i < 2:  # Za mały fragment do odwrócenia
            continue
            
        # STRATEGIA EKSPLORACJI: Czasami wybieramy punkty daleko od siebie
        if random.random() < 0.3 and iteration < max_iter // 2:
            min_distance = max(2, n // 10)
            max_distance = min(n // 2, n - 1)
            if k - i < min_distance:
                k = min(i + random.randint(min_distance, max_distance), n - 1)
        
        # KROK 2: Wykonujemy operację 2-opt
        new_tour = two_opt_swap(current, i, k)
        new_dist = total_distance(new_tour, points)
        
        # KROK 3: Obliczamy zmianę długości trasy
        delta = new_dist - current_dist
        total_moves += 1
        
        # KROK 4: KRYTERIUM AKCEPTACJI METROPOLISA
        accept = False
        if delta < 0:
            # POPRAWY: zawsze akceptujemy
            accept = True
            improvements += 1
        elif T > 0:
            # POGORSZENIE: akceptujemy z prawdopodobieństwem exp(-Δ/T)
            probability = math.exp(-delta / T)
            if random.random() < probability:
                accept = True
        
        # KROK 5: Aktualizujemy rozwiązanie jeśli zaakceptowane
        if accept:
            current = new_tour
            current_dist = new_dist
            accepted_moves += 1
            
            # Aktualizujemy najlepsze rozwiązanie
            if current_dist < best_dist:
                best = current[:]
                best_dist = current_dist
        
        # KROK 6: CHŁODZENIE (zmniejszanie temperatury)
        if cooling_schedule == 'exponential':
            alpha = 0.99995  # Współczynnik chłodzenia (bardzo wolne)
            T *= alpha
        elif cooling_schedule == 'linear':
            T = T_start * (1 - iteration / max_iter)
        elif cooling_schedule == 'logarithmic':
            T = T_start / math.log(iteration + 2)
        
        # ZAPISUJEMY HISTORIĘ
        if iteration % 1000 == 0:
            temperature_history.append(T)
            distance_history.append(best_dist)
        
        # RAPORT POSTĘPU)
        if iteration % 50000 == 0:
            acceptance_rate = accepted_moves / max(total_moves, 1) * 100
            improvement_rate = improvements / max(total_moves, 1) * 100
            print(f"Iteracja {iteration:6d}: T={T:.6f}, Najlepsza={best_dist:.1f}, "
                  f"Akceptacja={acceptance_rate:.1f}%, Poprawa={improvement_rate:.1f}%")
    
    # PODSUMOWANIE
    print(f"\n=== ZAKOŃCZONO SYMULOWANE WYŻARZANIE ===")
    print(f"Wykonano {iteration + 1} iteracji")
    print(f"Końcowa temperatura: {T:.2e}")
    print(f"Całkowita liczba ruchów: {total_moves}")
    print(f"Zaakceptowane ruchy: {accepted_moves} ({accepted_moves/total_moves*100:.1f}%)")
    print(f"Poprawy: {improvements} ({improvements/total_moves*100:.1f}%)")
    
    return best, best_dist, temperature_history, distance_history

def plot_comparison(points, initial_tour, best_tour):
    """
    WIZUALIZACJA: Porównanie cyklu początkowego i wyjściowego
    Tworzymy dwa wykresy obok siebie
    """
    print("=== TWORZENIE WIZUALIZACJI ===")
    
    # Obliczamy długości tras
    initial_dist = total_distance(initial_tour, points)
    best_dist = total_distance(best_tour, points)
    
    print(f"Przygotowywanie wykresów...")
    print(f"  Cykl początkowy: {initial_dist:.3f}")
    print(f"  Cykl wyjściowy: {best_dist:.3f}")
    
    # Tworzymy subplot z 2 wykresami
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    tours_data = [
        (initial_tour, initial_dist, "Cykl początkowy", "red"), 
        (best_tour, best_dist, "Cykl wyjściowy", "red")
    ]
    
    for i, (tour, distance, title, color) in enumerate(tours_data):
        print(f"  Rysowanie wykresu {i+1}: {title}")
        
        # Współrzędne trasy
        x_coords = [points[j][0] for j in tour] + [points[tour[0]][0]]
        y_coords = [points[j][1] for j in tour] + [points[tour[0]][1]]
        
        # Rysowanie trasy
        axes[i].plot(x_coords, y_coords, 'o-', color=color, markersize=3, 
                    linewidth=1.5, alpha=0.8, label='Trasa')
        
        # Rysowanie wszystkich punktów
        axes[i].scatter([points[j][0] for j in range(len(points))], 
                       [points[j][1] for j in range(len(points))], 
                       c='red', s=15, zorder=5, alpha=0.7, label='Miasta')
        
        axes[i].set_title(f"({chr(97+i)}) {title}. Długość cyklu: {distance:.3f}")
        axes[i].set_xlabel("x")
        axes[i].set_ylabel("y")
        axes[i].grid(True, alpha=0.3)
        axes[i].set_aspect('equal')
    
    plt.tight_layout()
    print("Wyświetlanie wykresów...")
    plt.show()


if __name__ == "__main__":
    print("="*60)
    print("ALGORYTM SYMULOWANEGO WYŻARZANIA DLA PROBLEMU KOMIWOJAŻERA")
    print("="*60)
    
    # KROK 1: Wczytanie danych
    filename = "xqf131.dat"
    points = load_points(filename)
    
    if not points:
        print("BŁĄD: Nie udało się wczytać danych.")
        exit(1)
    
    # KROK 2: Stworzenie cyklu początkowego (losowego)
    print(f"\n=== TWORZENIE CYKLU POCZĄTKOWEGO ===")
    random.seed(42)  # Dla powtarzalności wyników
    initial_tour = random_tour_generator(points)
    initial_distance = total_distance(initial_tour, points)
    print(f"Cykl początkowy (losowy): {initial_distance:.3f}")
    
    # KROK 3: Uruchomienie symulowanego wyżarzania
    print(f"\n" + "="*60)
    print("URUCHAMIANIE ALGORYTMU SYMULOWANEGO WYŻARZANIA")
    print("="*60)
    
    best_tour, best_distance, temp_hist, dist_hist = simulated_annealing_advanced(points)
    
    # KROK 4: Podsumowanie wyników
    print(f"\n" + "="*60)
    print("KOŃCOWE WYNIKI")
    print("="*60)
    print(f"Cykl początkowy:     {initial_distance:.3f}")
    print(f"Cykl wyjściowy:      {best_distance:.3f}")
    print(f"Poprawa:             {initial_distance - best_distance:.3f}")
    print(f"Poprawa (%):         {(initial_distance - best_distance)/initial_distance*100:.1f}%")
    
    # KROK 5: Wizualizacja
    print(f"\n=== GENEROWANIE WIZUALIZACJI ===")
    plot_comparison(points, initial_tour, best_tour)
    
    print("\n=== KONIEC PROGRAMU ===")