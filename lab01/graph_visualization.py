"""
Graph visualization module.
Provides functions to visualize graphs using:
- Circular layout (vertices evenly distributed on a circle)
- Force-directed layout (using NetworkX)
"""

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import math
from graph_representation import Graph

def visualize_circular(graph, title="Graph - Circular Layout", save_path=None):
    """
    Visualize a graph with vertices evenly distributed on a circle.
    
    Args:
        graph: Graph object to visualize
        title: Title for the plot
        save_path: If provided, save the figure to this path instead of displaying
    """
    plt.figure(figsize=(10, 10))
    plt.title(title)
    
    # Get number of vertices
    num_vertices = graph.V
    
    # Calculate positions on the circle
    radius = 5
    angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)
    
    # Calculate coordinates
    pos = {}
    for i in range(num_vertices):
        pos[i] = (radius * np.cos(angles[i]), radius * np.sin(angles[i]))
    
    # Draw vertices
    for i in range(num_vertices):
        plt.plot(pos[i][0], pos[i][1], 'bo', markersize=10)
        plt.text(pos[i][0] * 1.1, pos[i][1] * 1.1, str(i), fontsize=12, 
                 ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
    
    # Draw edges
    for u, v in graph.get_edges():
        plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 'k-', alpha=0.6)
    
    plt.axis('equal')
    plt.grid(alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def visualize_force_directed(graph, title="Graph - Force-Directed Layout", save_path=None):
    """
    Visualize a graph using NetworkX's force-directed layout.
    
    Args:
        graph: Graph object to visualize
        title: Title for the plot
        save_path: If provided, save the figure to this path instead of displaying
    """
    plt.figure(figsize=(10, 10))
    plt.title(title)
    
    # Create NetworkX graph
    G = nx.Graph()
    
    # Add nodes
    for i in range(graph.V):
        G.add_node(i)
    
    # Add edges
    for u, v in graph.get_edges():
        G.add_edge(u, v)
    
    # Calculate layout
    pos = nx.spring_layout(G, seed=42)  # For reproducibility
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='skyblue', 
            node_size=700, font_size=15, width=2, edge_color='gray')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def visualize_graph(graph, circular=True, force_directed=True, 
                   title_prefix="Graph", save_prefix=None):
    """
    Visualize a graph using both circular and force-directed layouts.
    
    Args:
        graph: Graph object to visualize
        circular: Whether to create circular layout visualization
        force_directed: Whether to create force-directed layout visualization
        title_prefix: Prefix for the plot titles
        save_prefix: If provided, save figures with this prefix instead of displaying
    """
    if circular:
        title = f"{title_prefix} - Circular Layout"
        save_path = f"{save_prefix}_circular.png" if save_prefix else None
        visualize_circular(graph, title, save_path)
    
    if force_directed:
        title = f"{title_prefix} - Force-Directed Layout"
        save_path = f"{save_prefix}_force.png" if save_prefix else None
        visualize_force_directed(graph, title, save_path)


# Example usage
if __name__ == "__main__":
    # Create a sample graph
    g = Graph(6)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 0)
    
    # Visualize with both layouts
    visualize_graph(g, title_prefix="Sample Graph") 