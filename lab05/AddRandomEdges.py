import random


def add_random_edges(existing_edges, node_layer_map, N):
    all_nodes = list(node_layer_map.keys())
    edge_set = set(existing_edges)
    new_edges = set()

    while len(new_edges) < 2 * N:
        u, v = random.sample(all_nodes, 2)

        if v == 's' or u == 'v':
            continue
        if (u, v) in edge_set or (u, v) in new_edges:
            continue

        new_edges.add((u, v))

    return existing_edges + list(new_edges)
