from collections import deque

from lab05 import FlowNetwork


def bfs(residual, s, t):
    # Trzymanie poprzedników
    parent = {s: None}

    # Kolejka FIFO zaczynająca od s
    queue = deque([s])

    while queue:
        # Przeszukanie wszerz
        u = queue.popleft()
        # Przeglądamy sąsiadów
        for v in residual.get(u, {}):
            # Czy przepustowość na krawędzi >0
            # Czy v jeszcze nie odwiedzony, nie ma rodzica
            if residual[u][v] > 0 and v not in parent:
                # Zapamiętaj że z u doszliśmy do v
                parent[v] = u
                # Jeśli ujście to buduj ścieżkę
                if v == t:
                    path = []
                    # Cofaj do początku, tworząc listę krawędzi
                    while v != s:
                        path.append((parent[v], v))
                        v = parent[v]
                    # Odwróć kolejność żeby mieć ścieżkę z s do t
                    path.reverse()
                    # Zwróć ścieżkę powiększającą
                    return path
                # Jeśli to nie ujście, dodaj v do kolejki do dalszego przeszukiwania
                queue.append(v)
    return None  # Jeśli nie ma ścieżki z s do t, zwróć None

def edmonds_karp(network: FlowNetwork, s='s', t='v'):
    flow = {}
    capacity = {}

    # inicjalizacja, przepływ zerowy na każdej krawędzi
    # zapisanie przepustowości
    for u, v, c in network.edges:
        flow[(u, v)] = 0
        capacity[(u, v)] = c

    # Funkcja pomocniczna budująca sieć rezydualną
    # na podstawie aktualnego przeyływu i przepustowości
    def build_residual():
        residual = {}
        for (u, v), f in flow.items():
            cap = capacity[(u, v)]
            # ile możemy jeszcze przesłać
            residual.setdefault(u, {})[v] = cap - f
            # ile możemy cofnąć
            residual.setdefault(v, {})[u] = f
        return residual

    max_flow = 0 # Zmienna przechowująca sumaryczny maksymalny przepływ

    while True:
        # Buduje sieć
        residual = build_residual()
        # Znajdź najkrótszą ścieżkę w sieci
        path = bfs(residual, s, t)

        # Jeśli nie ma ścieżki, zakończ pętlę
        if not path:
            break

        # Znajdujemy minimalną przepustowość rezydualną na znalezionej ścieżce
        cf_p = min(residual[u][v] for u, v in path)

        # Aktualizujemy przepływ na każdej krawędzi ścieżki
        for u, v in path:
            if (u, v) in flow:
                # Jeśli to krawędź oryginalna, dodajemy przepływ
                flow[(u, v)] += cf_p
            else:
                # Jeśli krawędź jest rezydualna w przeciwnym kierunku, zmniejszamy przepływ
                flow[(v, u)] -= cf_p
        max_flow += cf_p

    return max_flow, flow, capacity
    # max_flow maksymalny przepływ w sieci
    # flow słownik z przepływami na krawędziach
    # capacity słownik z przepustowościami krawędzi