from topology import Graph


# Gives the shortest path only on unweighted graph
def bfs(graph_data: list[list[int, ...], ...], source: int, destination: int):
    queue = []
    discovered = [False] * len(graph_data)
    distance = [-1] * len(graph_data)  # Mark unreachable nodes as -1
    previous = [-1] * len(graph_data)

    discovered[source] = True
    queue.append(source)
    distance[source] = 0
    idx = 0

    while idx < len(queue) and not discovered[destination]:
        current = queue[idx]
        idx += 1

        for neighbour, dist in enumerate(graph_data[current]):
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


def dijkstra(topology):
    best_route = []
    return best_route


def a_star(topology):
    best_route = []
    return best_route
