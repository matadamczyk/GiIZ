# Napisać program do generowania grafów losowych G(n, l) oraz G(n, p)

from graph_representation import Graph
from graph_visualization import visualize_graph
from random_graph_generator import generate_gnm_random_graph, generate_gnp_random_graph

if __name__ == "__main__":
    # Generate a G(n,m) random graph (Erdős–Rényi model 1)
    n = 10  # vertices
    m = 15  # edges
    g1 = generate_gnm_random_graph(n, m)
    print(f"G({n},{m}) random graph has {len(g1.get_edges())} edges")
    
    # Visualize G(n,m) graph
    visualize_graph(g1, title_prefix=f"G({n},{m}) Random Graph")
    
    # Generate a G(n,p) random graph (Erdős–Rényi model 2)
    n = 10  # vertices
    p = 0.3  # probability
    g2 = generate_gnp_random_graph(n, p)
    print(f"G({n},{p}) random graph has {len(g2.get_edges())} edges")
    
    # Visualize G(n,p) graph
    visualize_graph(g2, title_prefix=f"G({n},{p}) Random Graph")