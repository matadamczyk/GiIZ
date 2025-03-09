"""
Main script for graph generation, representation, and visualization.

This script:
1. Generates 10 random graphs (5 using G(n,m) model and 5 using G(n,p) model)
2. Represents each graph using adjacency matrix, incidence matrix, and adjacency list
3. Visualizes each graph using both circular and force-directed layouts
4. Saves all visualizations to the 'output' directory
"""

import os
import random
from graph_representation import Graph
from graph_visualization import visualize_graph
from random_graph_generator import generate_gnm_random_graph, generate_gnp_random_graph

# Create output directory if it doesn't exist
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def main():
    # Parameters for graph generation
    n = 10  # Number of vertices
    
    # Generate 5 graphs using G(n,m) model (Erdős–Rényi model 1)
    gnm_graphs = []
    for i in range(5):
        # Random number of edges between n and n*(n-1)/4
        max_edges = n * (n - 1) // 2
        m = random.randint(n, max_edges // 2)
        graph = generate_gnm_random_graph(n, m)
        gnm_graphs.append((graph, f"G({n},{m})"))
    
    # Generate 5 graphs using G(n,p) model (Erdős–Rényi model 2)
    gnp_graphs = []
    for i in range(5):
        # Random probability between 0.2 and 0.8
        p = random.uniform(0.2, 0.8)
        p = round(p, 2)  # Round for nicer display
        graph = generate_gnp_random_graph(n, p)
        gnp_graphs.append((graph, f"G({n},{p})"))
    
    # Process all graphs
    all_graphs = gnm_graphs + gnp_graphs
    for i, (graph, label) in enumerate(all_graphs):
        print(f"\nProcessing graph {i+1}: {label}")
        
        # Print representations
        print(f"Graph has {graph.V} vertices and {len(graph.get_edges())} edges")
        print("Adjacency Matrix:")
        for row in graph.get_adjacency_matrix():
            print(row)
        
        print("\nIncidence Matrix:")
        for row in graph.get_incidence_matrix():
            print(row)
        
        print("\nAdjacency List:")
        for j, neighbors in enumerate(graph.get_adjacency_list()):
            print(f"{j}: {neighbors}")
        
        # Visualize and save
        save_prefix = os.path.join(output_dir, f"graph_{i+1}_{label.replace('(', '').replace(')', '').replace(',', '_').replace('.', '_')}")
        visualize_graph(graph, circular=True, force_directed=True, 
                       title_prefix=f"Graph {i+1}: {label}", save_prefix=save_prefix)
        
        print(f"Visualizations saved to {save_prefix}_circular.png and {save_prefix}_force.png")

if __name__ == "__main__":
    main()
    print("\nAll graphs have been generated, represented, and visualized.")
    print(f"Visualizations are saved in the '{output_dir}' directory.") 