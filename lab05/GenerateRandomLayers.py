import random
import string

def generate_random_layers(N):
    # Słownik gdzie s - źródło, v - ujście
    layers = {0: ['s'], N+1: ['v']}

    # Oznaczamy co zostało użyte
    used_letters = set(['s', 'v'])

    # Generuje nazwy wierzchołków pomijając s i v
    letter_gen = (c for c in string.ascii_lowercase if c not in used_letters)

    # Dla każdej warsty losuje ile będzie wierzchołków i tworzy listę wierzchołków dla warstwy
    for i in range(1, N+1):
        count = random.randint(2, N)
        layers[i] = [next(letter_gen) for _ in range(count)]

    # Każdemu wierzchołkowi przypisywana jest warstwa
    node_layer_map = {node: layer for layer, nodes in layers.items() for node in nodes}

    # Zwracany jest słownik klucz - nazwa wierzchołka, wartość - numer warstwy
    return node_layer_map
