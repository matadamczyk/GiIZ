import random
import string

def generate_random_layers(N):
    assert 2 <= N <= 4
    layers = {0: ['s'], N+1: ['v']}
    used_letters = set(['s', 'v'])
    letter_gen = (c for c in string.ascii_lowercase if c not in used_letters)

    for i in range(1, N+1):
        count = random.randint(2, N)
        layers[i] = [next(letter_gen) for _ in range(count)]

    node_layer_map = {node: layer for layer, nodes in layers.items() for node in nodes}
    return node_layer_map
