"""
Wizualizacja grafów skierowanych (digrafów).
"""

import matplotlib.pyplot as plt
import numpy as np
import math
from lab04.digraph_representation import DiGraph

def visualize_digraph(digraph, title="Graf skierowany", layout="circular", highlight_edges=None, 
                     save_path=None, node_labels=None, edge_labels=True, interactive=False,
                     show_weights=True, edge_colors=None):
    """
    Wizualizuje graf skierowany.
    
    Args:
        digraph: DiGraph do wizualizacji
        title: Tytuł wykresu
        layout: Układ wierzchołków ('circular' lub 'force_directed')
        highlight_edges: Krawędzie do wyróżnienia
        save_path: Ścieżka do zapisania obrazu
        node_labels: Etykiety wierzchołków (domyślnie ich numery)
        edge_labels: Czy wyświetlać etykiety krawędzi (wagi)
        interactive: Czy tryb interaktywny
        show_weights: Czy wyświetlać wagi krawędzi
        edge_colors: Kolory krawędzi (słownik: (u,v) -> kolor)
    """
    if not interactive:
        plt.ioff()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title(title)
    
    # Liczba wierzchołków
    n = digraph.V
    
    # Pozycje wierzchołków
    pos = {}
    
    if layout == 'circular':
        # Rozmieszczenie wierzchołków na okręgu
        radius = 5
        for i in range(n):
            angle = 2 * math.pi * i / n
            pos[i] = (radius * math.cos(angle), radius * math.sin(angle))
    else:
        # Bardziej złożone rozmieszczenie wierzchołków (uproszczone force-directed)
        pos = _force_directed_layout(digraph)
    
    # Domyślne etykiety wierzchołków
    if node_labels is None:
        node_labels = {i: str(i) for i in range(n)}
    
    # Domyślne kolory krawędzi
    if edge_colors is None:
        edge_colors = {}
    
    # Rysuj wierzchołki
    for v in range(n):
        ax.plot(pos[v][0], pos[v][1], 'o', markersize=25, 
                color='lightblue', alpha=0.8, zorder=1)
        ax.text(pos[v][0], pos[v][1], node_labels[v], 
                fontsize=12, ha='center', va='center', zorder=2)
    
    # Rysuj krawędzie z strzałkami
    for u, v in digraph.get_edges():
        # Sprawdź, czy krawędź ma być wyróżniona
        is_highlighted = False
        if highlight_edges and ((u, v) in highlight_edges or [u, v] in highlight_edges):
            is_highlighted = True
        
        # Ustal kolor krawędzi
        if (u, v) in edge_colors:
            edge_color = edge_colors[(u, v)]
        elif is_highlighted:
            edge_color = 'blue'
        else:
            edge_color = 'black'
        
        # Rysuj krawędź z odpowiednim kolorem i grubością
        edge_width = 2 if is_highlighted else 1.5
        
        # Oblicz punkty kontrolne dla łuku
        # Jeśli mamy krawędzie w obie strony, użyj łuków
        if (v, u) in digraph.get_edges():
            # Krawędzie w obie strony - rysujemy łuki
            # Oblicz środkowy punkt między wierzchołkami
            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2
            
            # Oblicz wektor prostopadły do linii łączącej wierzchołki
            dx = pos[v][0] - pos[u][0]
            dy = pos[v][1] - pos[u][1]
            length = math.sqrt(dx*dx + dy*dy)
            
            # Normalizuj i obróć o 90 stopni
            nx = -dy / length
            ny = dx / length
            
            # Punkt kontrolny dla łuku
            ctrl_x = mid_x + nx * length * 0.3
            ctrl_y = mid_y + ny * length * 0.3
            
            # Rysuj łuk za pomocą krzywej Beziera
            t = np.linspace(0, 1, 100)
            x = (1-t)**2 * pos[u][0] + 2*(1-t)*t * ctrl_x + t**2 * pos[v][0]
            y = (1-t)**2 * pos[u][1] + 2*(1-t)*t * ctrl_y + t**2 * pos[v][1]
            
            ax.plot(x, y, color=edge_color, linewidth=edge_width, alpha=0.7, zorder=0)
            
            # Dodaj strzałkę na końcu łuku
            arrow_idx = 80  # Indeks punktu, gdzie umieścić strzałkę
            _draw_arrow(ax, (x[arrow_idx], y[arrow_idx]), (x[arrow_idx+1], y[arrow_idx+1]), 
                       color=edge_color, width=edge_width)
            
            # Dodaj wagę jako etykietę na łuku
            if edge_labels and show_weights:
                weight = digraph.get_weight(u, v)
                if weight is not None:
                    text_idx = 50  # Indeks punktu, gdzie umieścić etykietę
                    ax.text(x[text_idx], y[text_idx], str(weight), 
                           fontsize=10, ha='center', va='center',
                           bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        else:
            # Pojedyncza krawędź - prosta linia ze strzałką
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 
                   color=edge_color, linewidth=edge_width, alpha=0.7, zorder=0)
            
            # Dodaj strzałkę
            arrow_pos = 0.8  # Pozycja strzałki na linii (0.8 = 80% odległości)
            arrow_x = pos[u][0] + arrow_pos * (pos[v][0] - pos[u][0])
            arrow_y = pos[u][1] + arrow_pos * (pos[v][1] - pos[u][1])
            _draw_arrow(ax, (arrow_x, arrow_y), (pos[v][0], pos[v][1]), 
                       color=edge_color, width=edge_width)
            
            # Dodaj wagę jako etykietę na linii
            if edge_labels and show_weights:
                weight = digraph.get_weight(u, v)
                if weight is not None:
                    mid_x = (pos[u][0] + pos[v][0]) / 2
                    mid_y = (pos[u][1] + pos[v][1]) / 2
                    ax.text(mid_x, mid_y, str(weight), 
                           fontsize=10, ha='center', va='center',
                           bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    ax.axis('equal')
    ax.grid(alpha=0.3)
    ax.axis('off')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    elif interactive:
        plt.show()
    else:
        plt.draw()
        plt.pause(0.001)
        input("Naciśnij Enter, aby kontynuować...")
        plt.close()
    
    if not interactive:
        plt.ion()

def _draw_arrow(ax, start, end, color='black', width=1.5, head_width=0.2, head_length=0.3):
    """Rysuje strzałkę od punktu start do end."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx*dx + dy*dy)
    
    # Normalizacja wektora kierunkowego
    if length > 0:
        dx /= length
        dy /= length
    
    # Oblicz punkty trójkąta strzałki
    x1 = end[0] - head_length * dx + head_width * dy
    y1 = end[1] - head_length * dy - head_width * dx
    x2 = end[0] - head_length * dx - head_width * dy
    y2 = end[1] - head_length * dy + head_width * dx
    
    # Rysuj trójkąt strzałki
    ax.fill([end[0], x1, x2], [end[1], y1, y2], color=color, zorder=1)

def _force_directed_layout(digraph, iterations=100, k=1.0):
    """
    Oblicza układ wierzchołków metodą force-directed (uproszczoną).
    
    Args:
        digraph: Graf skierowany
        iterations: Liczba iteracji algorytmu
        k: Stała sprężystości
        
    Returns:
        Słownik pozycji wierzchołków {v: (x, y)}
    """
    n = digraph.V
    
    # Inicjalizacja pozycji losowo w kwadracie 10x10
    pos = {i: (np.random.uniform(-5, 5), np.random.uniform(-5, 5)) for i in range(n)}
    
    # Temperatura (określa maksymalny ruch wierzchołka)
    t = 10.0
    
    # Iteracje algorytmu
    for iter in range(iterations):
        # Dla każdego wierzchołka
        for v in range(n):
            # Siła odpychania od wszystkich innych wierzchołków
            force_x, force_y = 0, 0
            
            for u in range(n):
                if u != v:
                    # Oblicz różnicę pozycji
                    dx = pos[v][0] - pos[u][0]
                    dy = pos[v][1] - pos[u][1]
                    
                    # Odległość między wierzchołkami
                    dist = max(0.1, math.sqrt(dx*dx + dy*dy))
                    
                    # Siła odpychania (odwrotnie proporcjonalna do odległości)
                    force = k / dist
                    force_x += (dx / dist) * force
                    force_y += (dy / dist) * force
            
            # Siła przyciągania od połączonych wierzchołków
            for u in digraph.get_out_neighbors(v):
                # Oblicz różnicę pozycji
                dx = pos[v][0] - pos[u][0]
                dy = pos[v][1] - pos[u][1]
                
                # Odległość między wierzchołkami
                dist = max(0.1, math.sqrt(dx*dx + dy*dy))
                
                # Siła przyciągania (proporcjonalna do odległości)
                force = dist / k
                force_x -= (dx / dist) * force
                force_y -= (dy / dist) * force
            
            # Ogranicz siłę do maksymalnej temperatury
            force_mag = math.sqrt(force_x*force_x + force_y*force_y)
            if force_mag > 0:
                force_x = force_x / force_mag * min(force_mag, t)
                force_y = force_y / force_mag * min(force_mag, t)
            
            # Aktualizuj pozycję
            pos[v] = (pos[v][0] + force_x, pos[v][1] + force_y)
        
        # Zmniejszaj temperaturę wraz z postępem algorytmu
        t = max(0.1, t * 0.95)
    
    return pos

def visualize_digraph_with_components(digraph, components, title="Silnie spójne składowe",
                                    layout="circular", save_path=None, interactive=False):
    """
    Wizualizuje graf skierowany z wyróżnionymi silnie spójnymi składowymi.
    
    Args:
        digraph: DiGraph do wizualizacji
        components: Lista list wierzchołków tworzących silnie spójne składowe
        title: Tytuł wykresu
        layout: Układ wierzchołków
        save_path: Ścieżka do zapisania obrazu
        interactive: Czy tryb interaktywny
    """
    if not interactive:
        plt.ioff()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title(title)
    
    # Liczba wierzchołków
    n = digraph.V
    
    # Pozycje wierzchołków
    pos = {}
    
    if layout == 'circular':
        # Rozmieszczenie wierzchołków na okręgu
        radius = 5
        for i in range(n):
            angle = 2 * math.pi * i / n
            pos[i] = (radius * math.cos(angle), radius * math.sin(angle))
    else:
        # Bardziej złożone rozmieszczenie wierzchołków
        pos = _force_directed_layout(digraph)
    
    # Kolory dla poszczególnych składowych
    colors = plt.cm.tab10.colors
    node_colors = ['lightgray'] * n
    
    # Przypisz kolory wierzchołkom w składowych
    for i, component in enumerate(components):
        color_idx = i % len(colors)
        for v in component:
            node_colors[v] = colors[color_idx]
    
    # Rysuj wierzchołki z odpowiednimi kolorami
    for v in range(n):
        ax.plot(pos[v][0], pos[v][1], 'o', markersize=25, 
                color=node_colors[v], alpha=0.8, zorder=1)
        ax.text(pos[v][0], pos[v][1], str(v), 
                fontsize=12, ha='center', va='center', zorder=2)
    
    # Rysuj krawędzie z strzałkami
    for u, v in digraph.get_edges():
        # Sprawdź, czy krawędź łączy wierzchołki z tej samej składowej
        same_component = False
        for component in components:
            if u in component and v in component:
                same_component = True
                break
        
        # Ustal kolor krawędzi
        edge_color = 'blue' if same_component else 'gray'
        edge_width = 2 if same_component else 1
        
        # Rysuj krawędź
        if (v, u) in digraph.get_edges():
            # Krawędzie w obie strony - rysujemy łuki
            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2
            
            dx = pos[v][0] - pos[u][0]
            dy = pos[v][1] - pos[u][1]
            length = math.sqrt(dx*dx + dy*dy)
            
            nx = -dy / length
            ny = dx / length
            
            ctrl_x = mid_x + nx * length * 0.3
            ctrl_y = mid_y + ny * length * 0.3
            
            t = np.linspace(0, 1, 100)
            x = (1-t)**2 * pos[u][0] + 2*(1-t)*t * ctrl_x + t**2 * pos[v][0]
            y = (1-t)**2 * pos[u][1] + 2*(1-t)*t * ctrl_y + t**2 * pos[v][1]
            
            ax.plot(x, y, color=edge_color, linewidth=edge_width, alpha=0.7, zorder=0)
            
            arrow_idx = 80
            _draw_arrow(ax, (x[arrow_idx], y[arrow_idx]), (x[arrow_idx+1], y[arrow_idx+1]), 
                       color=edge_color, width=edge_width)
        else:
            # Pojedyncza krawędź - prosta linia ze strzałką
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 
                   color=edge_color, linewidth=edge_width, alpha=0.7, zorder=0)
            
            arrow_pos = 0.8
            arrow_x = pos[u][0] + arrow_pos * (pos[v][0] - pos[u][0])
            arrow_y = pos[u][1] + arrow_pos * (pos[v][1] - pos[u][1])
            _draw_arrow(ax, (arrow_x, arrow_y), (pos[v][0], pos[v][1]), 
                       color=edge_color, width=edge_width)
    
    # Dodaj legendę dla składowych
    legend_handles = []
    for i, component in enumerate(components):
        color_idx = i % len(colors)
        label = f"Składowa {i+1}: {component}"
        handle = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[color_idx],
                          markersize=10, label=label)
        legend_handles.append(handle)
    
    if legend_handles:
        ax.legend(handles=legend_handles, loc='best', fontsize=10)
    
    ax.axis('equal')
    ax.grid(alpha=0.3)
    ax.axis('off')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    elif interactive:
        plt.show()
    else:
        plt.draw()
        plt.pause(0.001)
        input("Naciśnij Enter, aby kontynuować...")
        plt.close()
    
    if not interactive:
        plt.ion() 