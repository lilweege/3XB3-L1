def reconstruct_path(fr, to, edges):
    path = []
    while to != fr:
        edge = edges[to]
        path.append(edge)
        to = edge.fr
    return list(reversed(path))
