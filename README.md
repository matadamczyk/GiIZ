# Graph Theory Lab

This repository contains implementations for graph representation, visualization, and random graph generation.

## Requirements

- Python 3.6+
- Required packages: matplotlib, numpy, networkx

Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

- `lab01/graph_representation.py`: Module for graph representation (adjacency matrix, incidence matrix, adjacency list)
- `lab01/graph_visualization.py`: Module for graph visualization (circular and force-directed layouts)
- `lab01/random_graph_generator.py`: Module for random graph generation (Erdős–Rényi models)
- `lab01/main.py`: Main script that generates and visualizes 10 random graphs

## Usage

### Running the Main Script

To generate and visualize 10 random graphs (5 using each Erdős–Rényi model):

```bash
cd lab01
python main.py
```

This will:
1. Generate 10 random graphs
2. Print their representations (adjacency matrix, incidence matrix, adjacency list)
3. Visualize each graph using both circular and force-directed layouts
4. Save all visualizations to the `output` directory

### Using Individual Modules

#### Graph Representation

```python
from lab01.graph_representation import Graph

# Create a graph with 5 vertices
g = Graph(5)

# Add edges
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 3)

# Get different representations
adj_matrix = g.get_adjacency_matrix()
inc_matrix = g.get_incidence_matrix()
adj_list = g.get_adjacency_list()

# Create a graph from an existing representation
adj_matrix = [
    [0, 1, 1, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 0, 1, 0]
]
g2 = Graph(5, 'adjacency_matrix', adj_matrix)
```

#### Graph Visualization

```python
from lab01.graph_representation import Graph
from lab01.graph_visualization import visualize_graph, visualize_circular, visualize_force_directed

# Create a graph
g = Graph(6)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(4, 5)
g.add_edge(5, 0)

# Visualize with both layouts
visualize_graph(g, title_prefix="My Graph")

# Or use individual visualization functions
visualize_circular(g, title="My Graph - Circular")
visualize_force_directed(g, title="My Graph - Force-Directed")

# Save visualizations to files
visualize_graph(g, save_prefix="output/my_graph")
```

#### Random Graph Generation

```python
from lab01.random_graph_generator import generate_gnm_random_graph, generate_gnp_random_graph

# Generate a G(n,m) random graph (Erdős–Rényi model 1)
n = 10  # vertices
m = 15  # edges
g1 = generate_gnm_random_graph(n, m)

# Generate a G(n,p) random graph (Erdős–Rényi model 2)
n = 10  # vertices
p = 0.3  # probability
g2 = generate_gnp_random_graph(n, p)
```

## Tasks Completed

1. Graph representation using adjacency matrix, incidence matrix, and adjacency list
2. Conversion between different graph representations
3. Graph visualization with vertices evenly distributed on a circle
4. Random graph generation using both Erdős–Rényi models:
   - G(n,m): Graph with n vertices and m randomly placed edges
   - G(n,p): Graph with n vertices where each edge exists with probability p 