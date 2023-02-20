from topology import Graph


def bfs(graph: Graph, root: int):
    queue = []
    discovered = [False] * len(graph.data)
    distance = [-1] * len(graph.data)  # Mark unreachable nodes as -1
    previous = [-1] * len(graph.data)

    discovered[root] = True
    queue.append(root)
    distance[root] = 0
    idx = 0

    while idx < len(queue):
        current = queue[idx]
        idx += 1

        for neighbour, dist in enumerate(graph.data[current]):
            if dist > 0 and not discovered[neighbour]:
                queue.append(neighbour)
                discovered[neighbour] = True
                distance[neighbour] = distance[current] + dist
                previous[neighbour] = current

    return queue, previous, distance


# Useless for getting shortest path
def dfs(graph: Graph, root: int):
    stack = [root]
    discovered = [False] * len(graph.data)
    previous = [-1] * len(graph.data)
    distance = [-1] * len(graph.data)

    discovered[root] = True
    distance[root] = 0

    history = []
    while stack:
        current = stack.pop()
        history.append(current)

        for neighbour, dist in enumerate(graph.data[current]):
            if dist > 0 and not discovered[neighbour]:
                stack.append(neighbour)
                discovered[neighbour] = True
                previous[neighbour] = current
                distance[neighbour] = distance[current] + dist

    return history, previous, distance


def dijkstra(topology):
    best_route = []
    return best_route


def a_star(topology):
    best_route = []
    return best_route
