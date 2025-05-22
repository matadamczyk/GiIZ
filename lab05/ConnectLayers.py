import random


def connect_layers(node_layer_map, N):
    from collections import defaultdict

    # Słownik gdzie klucz to numer warstwy, wartość to lista wierzchołków należących do warstwy
    layers = defaultdict(list)

    for node, layer in node_layer_map.items():
        layers[layer].append(node)

    edges = set()

    for i in range(N + 1):
        src_nodes = layers[i]
        dst_nodes = layers[i + 1]

        has_out = {node: False for node in src_nodes} # Czy wierzchołek ma krawędź wychodzącą
        has_in = {node: False for node in dst_nodes} # wchodzącą

        # Pętla upewniająca się że każdy wierzchołek ma min 1 wychodzącą
        for src in src_nodes:
            dst = random.choice(dst_nodes)
            edges.add((src, dst))
            has_out[src] = True
            has_in[dst] = True

        # Pętla upewniająca się że każdy wierzchołek ma min 1 wchodzącą
        for dst in dst_nodes:
            if not has_in[dst]:
                src = random.choice(src_nodes)
                edges.add((src, dst))
                has_out[src] = True
                has_in[dst] = True

    # Lista krawędzi łączących warstwy
    return list(edges)
