import matplotlib.pyplot as plt
import numpy as np

class FlowNetwork:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, name, layer):
        self.nodes[name] = layer

    def add_edge(self, u, v, capacity):
        self.edges.append((u, v, capacity))

    def draw(self):
        layers = {}
        for node, layer in self.nodes.items():
            layers.setdefault(layer, []).append(node)

        max_width = max(len(nodes) for nodes in layers.values())
        positions = {}

        for layer_idx, (layer, nodes) in enumerate(sorted(layers.items())):
            y_positions = np.linspace(0, 1, len(nodes)+2)[1:-1]
            for i, node in enumerate(nodes):
                positions[node] = (layer_idx, 1 - y_positions[i])

        fig, ax = plt.subplots()
        ax.axis('off')

        for u, v, cap in self.edges:
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            ax.annotate("",
                        xy=(x2, y2), xycoords='data',
                        xytext=(x1, y1), textcoords='data',
                        arrowprops=dict(arrowstyle="->", lw=1))
            ax.text((x1 + x2)/2, (y1 + y2)/2, str(cap), color='red', fontsize=8)

        for node, (x, y) in positions.items():
            ax.plot(x, y, 'o', markersize=16, color='skyblue', markeredgecolor='black', markeredgewidth=1.5)
            ax.text(x, y, f"{node}", ha='center', va='center', fontsize=12, weight='bold')

        plt.show()


    def draw_with_flow(self, flow, capacity):
        layers = {}
        for node, layer in self.nodes.items():
            layers.setdefault(layer, []).append(node)

        max_width = max(len(nodes) for nodes in layers.values())
        positions = {}

        for layer_idx, (layer, nodes) in enumerate(sorted(layers.items())):
            y_positions = np.linspace(0, 1, len(nodes)+2)[1:-1]
            for i, node in enumerate(nodes):
                positions[node] = (layer_idx, 1 - y_positions[i])

        fig, ax = plt.subplots()
        ax.axis('off')

        for u, v, _ in self.edges:
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            ax.annotate("", xy=(x2, y2), xycoords='data',
                        xytext=(x1, y1), textcoords='data',
                        arrowprops=dict(arrowstyle="->", lw=1))
            f = flow.get((u, v), 0)
            c = capacity.get((u, v), 0)
            ax.text((x1 + x2)/2, (y1 + y2)/2, f"{f}/{c}", color='red', fontsize=9)

        for node, (x, y) in positions.items():
            ax.plot(x, y, 'o', markersize=16, color='skyblue', markeredgecolor='black')
            ax.text(x, y, f"{node}", ha='center', va='center', fontsize=12, weight='bold')

        plt.show()

