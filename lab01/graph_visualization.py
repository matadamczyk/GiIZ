import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import math
from graph import Graph

def visualize_circular(graph, title="Graph", save_path=None):
    plt.figure(figsize=(10, 10))
    plt.title(title)
    
    num_vertices = graph.V
    
    radius = 5
    angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)
    
    pos = {}
    for i in range(num_vertices):
        pos[i] = (radius * np.cos(angles[i]), radius * np.sin(angles[i]))
    
    for i in range(num_vertices):
        plt.plot(pos[i][0], pos[i][1], 'bo', markersize=10)
        plt.text(pos[i][0] * 1.1, pos[i][1] * 1.1, str(i), fontsize=12, 
                 ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
    
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
    plt.figure(figsize=(10, 10))
    plt.title(title)
    
    G = nx.Graph()
    
    for i in range(graph.V):
        G.add_node(i)
    
    for u, v in graph.get_edges():
        G.add_edge(u, v)
    
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, with_labels=True, node_color='skyblue', 
            node_size=700, font_size=15, width=2, edge_color='gray')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def visualize_graph(graph, circular=True, force_directed=True, 
                   title_prefix="Graph", save_prefix=None):

    if circular:
        title = f"{title_prefix} - Circular Layout"
        save_path = f"{save_prefix}_circular.png" if save_prefix else None
        visualize_circular(graph, title, save_path)
    
    if force_directed:
        title = f"{title_prefix} - Force-Directed Layout"
        save_path = f"{save_prefix}_force.png" if save_prefix else None
        visualize_force_directed(graph, title, save_path)
