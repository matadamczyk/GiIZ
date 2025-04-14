from collections import deque

from lab05 import FlowNetwork


def bfs(residual, s, t):
    parent = {s: None}
    queue = deque([s])

    while queue:
        u = queue.popleft()
        for v in residual.get(u, {}):
            if residual[u][v] > 0 and v not in parent:
                parent[v] = u
                if v == t:
                    path = []
                    while v != s:
                        path.append((parent[v], v))
                        v = parent[v]
                    path.reverse()
                    return path
                queue.append(v)
    return None

def edmonds_karp(network: FlowNetwork, s='s', t='v'):
    flow = {}
    capacity = {}
    for u, v, c in network.edges:
        flow[(u, v)] = 0
        capacity[(u, v)] = c

    def build_residual():
        residual = {}
        for (u, v), f in flow.items():
            cap = capacity[(u, v)]
            residual.setdefault(u, {})[v] = cap - f
            residual.setdefault(v, {})[u] = f
        return residual

    max_flow = 0

    while True:
        residual = build_residual()
        path = bfs(residual, s, t)
        if not path:
            break
        cf_p = min(residual[u][v] for u, v in path)
        for u, v in path:
            if (u, v) in flow:
                flow[(u, v)] += cf_p
            else:
                flow[(v, u)] -= cf_p
        max_flow += cf_p

    return max_flow, flow, capacity
