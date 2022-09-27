def reconstruct_path(fr, to, edges):
    '''
    Reconstruct the path by retracing edges from the end node to the
    start node. Each entry in the <edges> dictionary stores the "parent"
    edge of the indexed node.
    '''
    path = []
    while to != fr:
        edge = edges[to]
        path.append(edge)
        to = edge.fr
    return list(reversed(path))
