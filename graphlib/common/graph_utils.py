def reconstruct_path(fr, to, edge):
    path = [to]
    while to != fr:
        to = edge[to]
        path.append(to)
    return list(reversed(path))
