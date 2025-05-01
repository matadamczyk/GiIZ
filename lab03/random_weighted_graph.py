"""
Random weighted graph generator module.
Implements generation of connected random graphs with random weights.
"""

import random
import math
from lab03.graph_representation import Graph

def generate_random_connected_graph(n, p=None):
    """
    Generate a random connected graph with n vertices.
    
    Args:
        n: Number of vertices
        p: Probability of edge creation (if None, calculated automatically)
        
    Returns:
        Graph object with n vertices that is connected
    """
    if n < 1:
        raise ValueError("Number of vertices must be at least 1")
    
    # If p is not provided, calculate a reasonable value
    if p is None:
        # For small n, use higher probability to ensure connectivity
        if n <= 10:
            p = 0.4
        else:
            # For larger n, we can use a lower probability
            # lim p = ln(n)/n as n → ∞ for connectivity
            p = max(0.1, 2 * math.log(n) / n)
    
    # Create a graph with n vertices
    graph = Graph(n)
    
    # First, ensure the graph is connected by adding a spanning tree
    for i in range(1, n):
        # Connect i to a random vertex from [0, i-1]
        j = random.randint(0, i-1)
        graph.add_edge(i, j)
    
    # Add additional edges with probability p
    for i in range(n):
        for j in range(i + 1, n):
            # Skip if the edge already exists
            if (i, j) in graph.get_edges() or (j, i) in graph.get_edges():
                continue
                
            if random.random() < p:
                graph.add_edge(i, j)
    
    return graph

def assign_random_weights(graph, min_weight=1, max_weight=10):
    """
    Assign random weights to all edges in the graph.
    
    Args:
        graph: Graph object
        min_weight: Minimum weight (inclusive)
        max_weight: Maximum weight (inclusive)
        
    Returns:
        The same graph with updated weights
    """
    for edge in graph.get_edges():
        u, v = edge
        weight = random.randint(min_weight, max_weight)
        
        # Update the weight in the graph
        graph.weights[edge] = weight
    
    return graph

def generate_random_weighted_connected_graph(n, min_weight=1, max_weight=10, p=None):
    """
    Generate a random connected graph with n vertices and random weights.
    
    Args:
        n: Number of vertices
        min_weight: Minimum weight (inclusive)
        max_weight: Maximum weight (inclusive)
        p: Probability of edge creation (if None, calculated automatically)
        
    Returns:
        Graph object with n vertices, connected, with random weights
    """
    graph = generate_random_connected_graph(n, p)
    return assign_random_weights(graph, min_weight, max_weight)


# Example usage
if __name__ == "__main__":
    n = 10
    g = generate_random_weighted_connected_graph(n)
    print(f"Generated a connected weighted graph with {n} vertices and {len(g.get_edges())} edges")
    print("Weights:", g.get_weights()) 