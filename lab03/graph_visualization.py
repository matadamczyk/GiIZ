"""
Graph visualization module.
Provides functions to visualize weighted graphs using:
- Circular layout (vertices evenly distributed on a circle)
- Force-directed layout (using NetworkX)
"""

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import math
from lab03.graph_representation import Graph

def visualize_circular(graph, title="Graph - Circular Layout", save_path=None, highlight_edges=None, interactive=True):
    """
    Visualize a weighted graph with vertices evenly distributed on a circle.
    
    Args:
        graph: Graph object to visualize
        title: Title for the plot
        save_path: If provided, save the figure to this path instead of displaying
        highlight_edges: Optional list of edges to highlight (e.g., for MST visualization)
        interactive: Whether to show plot interactively (True) or block (False)
    """
    if not interactive:
        plt.ioff()  # Turn off interactive mode
    
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
    
    # Draw edges with weights
    if highlight_edges is None:
        highlight_edges = []

    for u, v in graph.get_edges():
        edge_color = 'blue' if (u, v) in highlight_edges or (v, u) in highlight_edges else 'black'
        edge_width = 2 if (u, v) in highlight_edges or (v, u) in highlight_edges else 1
        plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], c=edge_color, linewidth=edge_width, alpha=0.6)
        
        # Display the weight
        weight = graph.get_weight(u, v)
        midpoint = ((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2)
        plt.text(midpoint[0], midpoint[1], str(weight), fontsize=10, 
                 ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
    
    plt.axis('equal')
    plt.grid(alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    elif interactive:
        plt.show()
    else:
        plt.draw()
        plt.pause(0.001)  # Pause to update the canvas
        input("Press [Enter] to continue...")
        plt.close()
    
    if not interactive:
        plt.ion()  # Turn on interactive mode again

def visualize_force_directed(graph, title="Graph - Force-Directed Layout", save_path=None, highlight_edges=None, interactive=True):
    """
    Visualize a weighted graph using NetworkX's force-directed layout.
    
    Args:
        graph: Graph object to visualize
        title: Title for the plot
        save_path: If provided, save the figure to this path instead of displaying
        highlight_edges: Optional list of edges to highlight (e.g., for MST visualization)
        interactive: Whether to show plot interactively (True) or block (False)
    """
    if highlight_edges is None:
        highlight_edges = []
        
    if not interactive:
        plt.ioff()  # Turn off interactive mode
    
    plt.figure(figsize=(10, 10))
    plt.title(title)
    
    # Create NetworkX graph
    G = nx.Graph()
    
    # Add nodes
    for i in range(graph.V):
        G.add_node(i)
    
    # Add edges with weights
    for u, v in graph.get_edges():
        weight = graph.get_weight(u, v)
        G.add_edge(u, v, weight=weight)
    
    # Calculate layout
    pos = nx.spring_layout(G, seed=42)  # For reproducibility
    
    # Prepare edge lists for drawing
    normal_edges = [(u, v) for u, v in graph.get_edges() if (u, v) not in highlight_edges and (v, u) not in highlight_edges]
    
    # Draw normal edges
    if normal_edges:
        nx.draw_networkx_edges(G, pos, edgelist=normal_edges, width=1, edge_color='gray')
    
    # Draw highlighted edges
    if highlight_edges:
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, width=2, edge_color='blue')
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=15)
    
    # Draw edge labels (weights)
    edge_labels = {(u, v): graph.get_weight(u, v) for u, v in graph.get_edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
    plt.axis('off')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    elif interactive:
        plt.show()
    else:
        plt.draw()
        plt.pause(0.001)  # Pause to update the canvas
        input("Press [Enter] to continue...")
        plt.close()
    
    if not interactive:
        plt.ion()  # Turn on interactive mode again

def visualize_graph(graph, circular=True, force_directed=True, 
                   title_prefix="Graph", save_prefix=None, highlight_edges=None, interactive=True):
    """
    Visualize a weighted graph using both circular and force-directed layouts.
    
    Args:
        graph: Graph object to visualize
        circular: Whether to create circular layout visualization
        force_directed: Whether to create force-directed layout visualization
        title_prefix: Prefix for the plot titles
        save_prefix: If provided, save figures with this prefix instead of displaying
        highlight_edges: Optional list of edges to highlight (e.g., for MST visualization)
        interactive: Whether to show plot interactively (True) or block (False)
    """
    if highlight_edges is None:
        highlight_edges = []
        
    if circular:
        title = f"{title_prefix} - Circular Layout"
        save_path = f"{save_prefix}_circular.png" if save_prefix else None
        visualize_circular(graph, title, save_path, highlight_edges, interactive)
    
    if force_directed:
        title = f"{title_prefix} - Force-Directed Layout"
        save_path = f"{save_prefix}_force.png" if save_prefix else None
        visualize_force_directed(graph, title, save_path, highlight_edges, interactive) 