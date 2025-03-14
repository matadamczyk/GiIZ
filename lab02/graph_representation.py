"""
Graph representation module.
Implements simple graph encoding using:
- Adjacency matrix
- Incidence matrix
- Adjacency list
And provides conversion between these representations.
"""

class Graph:
    def __init__(self, vertices, representation_type=None, data=None):
        """
        Initialize a graph with a given number of vertices.
        
        Args:
            vertices: Number of vertices in the graph
            representation_type: Type of initial representation ('adjacency_matrix', 'incidence_matrix', 'adjacency_list')
            data: Initial data for the specified representation type
        """
        self.V = vertices
        
        # Initialize empty representations
        self.adjacency_matrix = [[0] * vertices for _ in range(vertices)]
        self.incidence_matrix = []
        self.adjacency_list = [[] for _ in range(vertices)]
        self.edges = []
        
        # If initial data is provided, use it to populate the graph
        if representation_type and data:
            if representation_type == 'adjacency_matrix':
                self.adjacency_matrix = data
                self._from_adjacency_matrix()
            elif representation_type == 'incidence_matrix':
                self.incidence_matrix = data
                self._from_incidence_matrix()
            elif representation_type == 'adjacency_list':
                self.adjacency_list = data
                self._from_adjacency_list()
    
    def add_edge(self, u, v):
        """Add an edge between vertices u and v."""
        if u >= self.V or v >= self.V or u < 0 or v < 0:
            raise ValueError(f"Vertex indices must be between 0 and {self.V-1}")
        
        if u == v:
            raise ValueError("Self-loops are not allowed in simple graphs")
            
        # Update adjacency matrix
        self.adjacency_matrix[u][v] = 1
        self.adjacency_matrix[v][u] = 1
        
        # Update adjacency list (avoid duplicates)
        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)
        if u not in self.adjacency_list[v]:
            self.adjacency_list[v].append(u)
        
        # Update edges list (avoid duplicates)
        edge = (min(u, v), max(u, v))
        if edge not in self.edges:
            self.edges.append(edge)
            
        # Update incidence matrix
        self._update_incidence_matrix()
    
    def _update_incidence_matrix(self):
        """Update the incidence matrix based on the current edges."""
        self.incidence_matrix = [[0] * len(self.edges) for _ in range(self.V)]
        for edge_idx, (u, v) in enumerate(self.edges):
            self.incidence_matrix[u][edge_idx] = 1
            self.incidence_matrix[v][edge_idx] = 1
    
    def _from_adjacency_matrix(self):
        """Convert from adjacency matrix to other representations."""
        # Clear existing data
        self.adjacency_list = [[] for _ in range(self.V)]
        self.edges = []
        
        # Update adjacency list and edges
        for i in range(self.V):
            for j in range(i + 1, self.V):  # Only consider upper triangle to avoid duplicates
                if self.adjacency_matrix[i][j] == 1:
                    self.adjacency_list[i].append(j)
                    self.adjacency_list[j].append(i)
                    self.edges.append((i, j))
        
        # Update incidence matrix
        self._update_incidence_matrix()
    
    def _from_incidence_matrix(self):
        """Convert from incidence matrix to other representations."""
        # Clear existing data
        self.adjacency_matrix = [[0] * self.V for _ in range(self.V)]
        self.adjacency_list = [[] for _ in range(self.V)]
        self.edges = []
        
        # Process each column (edge) in the incidence matrix
        for edge_idx in range(len(self.incidence_matrix[0])):
            # Find the two vertices connected by this edge
            vertices = [v for v in range(self.V) if self.incidence_matrix[v][edge_idx] == 1]
            if len(vertices) == 2:
                u, v = vertices
                # Update adjacency matrix
                self.adjacency_matrix[u][v] = 1
                self.adjacency_matrix[v][u] = 1
                
                # Update adjacency list
                if v not in self.adjacency_list[u]:
                    self.adjacency_list[u].append(v)
                if u not in self.adjacency_list[v]:
                    self.adjacency_list[v].append(u)
                
                # Update edges
                self.edges.append((min(u, v), max(u, v)))
    
    def _from_adjacency_list(self):
        """Convert from adjacency list to other representations."""
        # Clear existing data
        self.adjacency_matrix = [[0] * self.V for _ in range(self.V)]
        self.edges = []
        
        # Update adjacency matrix and edges
        for u in range(self.V):
            for v in self.adjacency_list[u]:
                self.adjacency_matrix[u][v] = 1
                # Only add each edge once
                if u < v and (u, v) not in self.edges:
                    self.edges.append((u, v))
        
        # Update incidence matrix
        self._update_incidence_matrix()
    
    def get_adjacency_matrix(self):
        """Return the adjacency matrix representation."""
        return self.adjacency_matrix
    
    def get_incidence_matrix(self):
        """Return the incidence matrix representation."""
        return self.incidence_matrix
    
    def get_adjacency_list(self):
        """Return the adjacency list representation."""
        return self.adjacency_list
    
    def get_edges(self):
        """Return the list of edges."""
        return self.edges
    
    def __str__(self):
        """String representation of the graph."""
        result = f"Graph with {self.V} vertices and {len(self.edges)} edges\n"
        result += "Adjacency Matrix:\n"
        for row in self.adjacency_matrix:
            result += str(row) + "\n"
        
        result += "\nIncidence Matrix:\n"
        for row in self.incidence_matrix:
            result += str(row) + "\n"
        
        result += "\nAdjacency List:\n"
        for i, neighbors in enumerate(self.adjacency_list):
            result += f"{i}: {neighbors}\n"
        
        return result


# Example usage
if __name__ == "__main__":
    # Create a graph with 5 vertices
    g = Graph(5)
    
    # Add some edges
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    
    print(g)
    
    # Create a graph from an adjacency matrix
    adj_matrix = [
        [0, 1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0]
    ]
    g2 = Graph(5, 'adjacency_matrix', adj_matrix)
    print("\nGraph created from adjacency matrix:")
    print(g2) 