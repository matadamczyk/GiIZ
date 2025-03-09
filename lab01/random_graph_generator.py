"""
Random graph generator module.
Implements two Erdős–Rényi random graph models:
- G(n, m): Generate a random graph with n vertices and m edges
- G(n, p): Generate a random graph with n vertices where each edge exists with probability p
"""

import random
import math
from graph_representation import Graph

def generate_gnm_random_graph(n, m):
    """
    Generate a random graph with n vertices and m edges (Erdős–Rényi model 1).
    
    Args:
        n: Number of vertices
        m: Number of edges
        
    Returns:
        Graph object with n vertices and m randomly placed edges
    """
    if n < 1:
        raise ValueError("Number of vertices must be at least 1")
    
    # Maximum number of edges in a simple graph with n vertices
    max_edges = n * (n - 1) // 2
    
    if m > max_edges:
        raise ValueError(f"Too many edges. Maximum is {max_edges} for {n} vertices")
    
    # Create a graph with n vertices
    graph = Graph(n)
    
    # Generate all possible edges
    all_edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    
    # Randomly select m edges
    selected_edges = random.sample(all_edges, m)
    
    # Add the selected edges to the graph
    for u, v in selected_edges:
        graph.add_edge(u, v)
    
    return graph

def generate_gnp_random_graph(n, p):
    """
    Generate a random graph with n vertices where each edge exists with probability p
    (Erdős–Rényi model 2).
    
    Args:
        n: Number of vertices
        p: Probability of edge creation (0 <= p <= 1)
        
    Returns:
        Graph object with n vertices and randomly placed edges
    """
    if n < 1:
        raise ValueError("Number of vertices must be at least 1")
    
    if p < 0 or p > 1:
        raise ValueError("Probability must be between 0 and 1")
    
    # Create a graph with n vertices
    graph = Graph(n)
    
    # For each possible edge, add it with probability p
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                graph.add_edge(i, j)
    
    return graph

def estimate_p_for_expected_edges(n, expected_edges):
    """
    Estimate the probability p needed for G(n,p) model to have an expected number of edges.
    
    Args:
        n: Number of vertices
        expected_edges: Expected number of edges
        
    Returns:
        Probability p
    """
    max_edges = n * (n - 1) // 2
    return min(1.0, expected_edges / max_edges)


# Example usage
if __name__ == "__main__":
    # Generate a G(n,m) random graph
    n = 10
    m = 15
    g1 = generate_gnm_random_graph(n, m)
    print(f"G({n},{m}) random graph has {len(g1.get_edges())} edges")
    
    # Generate a G(n,p) random graph
    n = 10
    p = 0.3
    g2 = generate_gnp_random_graph(n, p)
    print(f"G({n},{p}) random graph has {len(g2.get_edges())} edges")
    
    # Estimate p for expected number of edges
    n = 10
    expected_edges = 15
    p = estimate_p_for_expected_edges(n, expected_edges)
    print(f"To get approximately {expected_edges} edges in a graph with {n} vertices, use p ≈ {p:.4f}") 