"""
Reprezentacja grafu skierowanego (digrafu).
Implementuje digraf za pomocą:
- Macierzy sąsiedztwa
- Listy sąsiedztwa
- Macierzy incydencji
Umożliwia konwersję między tymi reprezentacjami.
"""

class DiGraph:
    def __init__(self, vertices, representation_type=None, data=None):
        """
        Inicjalizuje graf skierowany z określoną liczbą wierzchołków.
        
        Args:
            vertices: Liczba wierzchołków w grafie
            representation_type: Typ początkowej reprezentacji ('adjacency_matrix', 'adjacency_list', 'incidence_matrix')
            data: Dane początkowe dla określonego typu reprezentacji
        """
        self.V = vertices
        
        # Inicjalizacja pustych reprezentacji
        self.adjacency_matrix = [[0] * vertices for _ in range(vertices)]
        self.adjacency_list = [[] for _ in range(vertices)]
        self.incidence_matrix = []
        self.edges = []  # Lista krawędzi (u, v)
        self.weights = {}  # Słownik wag: (u, v) -> waga
        
        # Jeśli podano dane początkowe, użyj ich do inicjalizacji grafu
        if representation_type and data:
            if representation_type == 'adjacency_matrix':
                self.adjacency_matrix = data
                self._from_adjacency_matrix()
            elif representation_type == 'adjacency_list':
                self.adjacency_list = data
                self._from_adjacency_list()
            elif representation_type == 'incidence_matrix':
                self.incidence_matrix = data
                self._from_incidence_matrix()
    
    def add_edge(self, u, v, weight=0):
        """
        Dodaje krawędź skierowaną od wierzchołka u do v z określoną wagą.
        
        Args:
            u: Wierzchołek źródłowy
            v: Wierzchołek docelowy
            weight: Waga krawędzi
        """
        if u >= self.V or v >= self.V or u < 0 or v < 0:
            raise ValueError(f"Indeksy wierzchołków muszą być z zakresu 0-{self.V-1}")
        
        # Aktualizuj macierz sąsiedztwa
        self.adjacency_matrix[u][v] = 1
        
        # Aktualizuj listę sąsiedztwa (unikaj duplikatów)
        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)
        
        # Aktualizuj listę krawędzi (unikaj duplikatów)
        edge = (u, v)
        if edge not in self.edges:
            self.edges.append(edge)
        
        # Zapisz wagę
        self.weights[edge] = weight
        
        # Aktualizuj macierz incydencji
        self._update_incidence_matrix()
    
    def get_weight(self, u, v):
        """Zwraca wagę krawędzi od u do v, lub None jeśli krawędź nie istnieje."""
        edge = (u, v)
        return self.weights.get(edge)
    
    def transpose(self):
        """
        Tworzy graf transponowany (odwrócenie kierunku wszystkich krawędzi).
        
        Returns:
            DiGraph: Transponowany graf
        """
        G_T = DiGraph(self.V)
        
        for u, v in self.edges:
            weight = self.get_weight(u, v)
            G_T.add_edge(v, u, weight)  # Odwróć kierunek krawędzi
        
        return G_T
    
    def _update_incidence_matrix(self):
        """Aktualizuje macierz incydencji na podstawie obecnych krawędzi."""
        num_edges = len(self.edges)
        self.incidence_matrix = [[0] * num_edges for _ in range(self.V)]
        
        # Dla każdej krawędzi (u, v), ustaw 1 dla wierzchołka u (wyjście) i -1 dla wierzchołka v (wejście)
        for edge_idx, (u, v) in enumerate(self.edges):
            self.incidence_matrix[u][edge_idx] = 1
            self.incidence_matrix[v][edge_idx] = -1
    
    def _from_adjacency_matrix(self):
        """Konwertuje z macierzy sąsiedztwa do innych reprezentacji."""
        # Wyczyść istniejące dane
        self.adjacency_list = [[] for _ in range(self.V)]
        self.edges = []
        self.weights = {}
        
        # Aktualizuj listę sąsiedztwa i krawędzie
        for u in range(self.V):
            for v in range(self.V):
                if self.adjacency_matrix[u][v] == 1:
                    self.adjacency_list[u].append(v)
                    self.edges.append((u, v))
                    self.weights[(u, v)] = 0  # Domyślna waga
        
        # Aktualizuj macierz incydencji
        self._update_incidence_matrix()
    
    def _from_adjacency_list(self):
        """Konwertuje z listy sąsiedztwa do innych reprezentacji."""
        # Wyczyść istniejące dane
        self.adjacency_matrix = [[0] * self.V for _ in range(self.V)]
        self.edges = []
        self.weights = {}
        
        # Aktualizuj macierz sąsiedztwa i krawędzie
        for u in range(self.V):
            for v in self.adjacency_list[u]:
                self.adjacency_matrix[u][v] = 1
                edge = (u, v)
                if edge not in self.edges:
                    self.edges.append(edge)
                    self.weights[edge] = 0  # Domyślna waga
        
        # Aktualizuj macierz incydencji
        self._update_incidence_matrix()
    
    def _from_incidence_matrix(self):
        """Konwertuje z macierzy incydencji do innych reprezentacji."""
        # Wyczyść istniejące dane
        self.adjacency_matrix = [[0] * self.V for _ in range(self.V)]
        self.adjacency_list = [[] for _ in range(self.V)]
        self.edges = []
        self.weights = {}
        
        # Dla każdej kolumny (krawędzi) w macierzy incydencji
        for edge_idx in range(len(self.incidence_matrix[0])):
            # Znajdź wierzchołek źródłowy (1) i docelowy (-1)
            source = None
            target = None
            for v in range(self.V):
                if self.incidence_matrix[v][edge_idx] == 1:
                    source = v
                elif self.incidence_matrix[v][edge_idx] == -1:
                    target = v
            
            if source is not None and target is not None:
                # Aktualizuj macierz sąsiedztwa
                self.adjacency_matrix[source][target] = 1
                
                # Aktualizuj listę sąsiedztwa
                if target not in self.adjacency_list[source]:
                    self.adjacency_list[source].append(target)
                
                # Aktualizuj krawędzie
                edge = (source, target)
                self.edges.append(edge)
                self.weights[edge] = 0  # Domyślna waga
    
    def get_out_neighbors(self, v):
        """Zwraca listę wierzchołków, do których prowadzą krawędzie z v."""
        return self.adjacency_list[v]
    
    def get_in_neighbors(self, v):
        """Zwraca listę wierzchołków, z których prowadzą krawędzie do v."""
        in_neighbors = []
        for u in range(self.V):
            if v in self.adjacency_list[u]:
                in_neighbors.append(u)
        return in_neighbors
    
    def has_edge(self, u, v):
        """Sprawdza, czy istnieje krawędź od u do v."""
        return v in self.adjacency_list[u]
    
    def get_adjacency_matrix(self):
        """Zwraca macierz sąsiedztwa."""
        return self.adjacency_matrix
    
    def get_adjacency_list(self):
        """Zwraca listę sąsiedztwa."""
        return self.adjacency_list
    
    def get_incidence_matrix(self):
        """Zwraca macierz incydencji."""
        return self.incidence_matrix
    
    def get_edges(self):
        """Zwraca listę krawędzi."""
        return self.edges
    
    def get_weights(self):
        """Zwraca słownik wag krawędzi."""
        return self.weights
    
    def add_vertex(self):
        """Dodaje nowy wierzchołek do grafu."""
        self.V += 1
        
        # Aktualizuj macierz sąsiedztwa
        for row in self.adjacency_matrix:
            row.append(0)
        self.adjacency_matrix.append([0] * self.V)
        
        # Aktualizuj listę sąsiedztwa
        self.adjacency_list.append([])
        
        # Aktualizuj macierz incydencji
        if self.incidence_matrix:
            self.incidence_matrix.append([0] * len(self.incidence_matrix[0]))
    
    def __str__(self):
        """Zwraca tekstową reprezentację grafu."""
        result = f"Graf skierowany z {self.V} wierzchołkami i {len(self.edges)} krawędziami\n"
        
        result += "Lista sąsiedztwa:\n"
        for i, neighbors in enumerate(self.adjacency_list):
            result += f"{i}: {neighbors}\n"
        
        result += "\nMacierz sąsiedztwa:\n"
        for row in self.adjacency_matrix:
            result += str(row) + "\n"
        
        result += "\nMacierz incydencji:\n"
        for row in self.incidence_matrix:
            result += str(row) + "\n"
        
        result += "\nWagi krawędzi:\n"
        for edge, weight in self.weights.items():
            result += f"{edge}: {weight}\n"
        
        return result 