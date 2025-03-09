# Napisać program do wizualizacji grafów prostych używający reprezen- tacji, 
# w której wierzchołki grafu są równomiernie rozłożone na okręgu.

from graph_representation import Graph
from graph_visualization import visualize_graph, visualize_circular, visualize_force_directed

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
    
    # Visualize with circular layout (vertices on a circle)
    visualize_circular(g, title="Simple Graph - Circular Layout")
    
    # Visualize with force-directed layout
    visualize_force_directed(g, title="Simple Graph - Force-Directed Layout")
    
    # Visualize with both layouts
    visualize_graph(g, title_prefix="Simple Graph")