from topology import Graph


# Gives the shortest path only on unweighted graph
def bfs(graph: Graph, source: int, destination: int):
    queue = []
    discovered = [False] * len(graph.data)
    distance = [-1] * len(graph.data)  # Mark unreachable nodes as -1
    previous = [-1] * len(graph.data)

    discovered[source] = True
    queue.append(source)
    distance[source] = 0
    idx = 0

    while idx < len(queue) and not discovered[destination]:
        current = queue[idx]
        idx += 1

        for neighbour, dist in enumerate(graph.data[current]):
            if dist > 0 and not discovered[neighbour]:
                queue.append(neighbour)
                discovered[neighbour] = True
                distance[neighbour] = distance[current] + dist
                previous[neighbour] = current

                # Skip discovering other current`s neighbours
                if discovered[destination]:
                    break

    best_route = []
    current = destination
    while current != source:
        best_route.append(current)
        current = previous[current]
    best_route.append(source)
    best_route.reverse()
    return best_route, distance[destination]


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
