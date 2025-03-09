# Napisać program kodujący grafy proste za pomocą macierzy sąsiedz- twa, macierzy incydencji i list sąsiędztwa. 
# Stworzyć moduł do zmiany danego kodowania na pozostałe.

from graph_representation import Graph

if __name__ == "__main__":
    # Create a graph with 5 vertices
    g = Graph(5)
    
    # Add some edges
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    
    # Print the graph representations
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
    
    # Create a graph from an adjacency list
    adj_list = [
        [1, 2],
        [0, 2, 3],
        [0, 1, 3],
        [1, 2, 4],
        [3]
    ]
    g3 = Graph(5, 'adjacency_list', adj_list)
    print("\nGraph created from adjacency list:")
    print(g3)