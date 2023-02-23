from topology import Graph


# Gives the shortest path only on unweighted graph
def bfs(graph_data: list[list[int]], source: int, destination: int):
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
                # distance[neighbour] = distance[current] + dist
                distance[neighbour] = distance[current] + 1  # Imitate unweighted graph to count hops
                previous[neighbour] = current

                # Skip discovering other current`s neighbours
                if discovered[destination]:
                    break

    best_route = []
    current = destination
    while current != source and current != -1:
        best_route.append(current)
        current = previous[current]
    best_route.append(source)
    best_route.reverse()
    return best_route, distance[destination], distance


def dijkstra(graph_data: list[list[int]], source: int, destination: int):
    queue = []
    discovered = [False] * len(graph_data)
    distance = [float('inf')] * len(graph_data)
    previous = [-1] * len(graph_data)

    discovered[source] = True
    distance[source] = 0
    queue.append(source)
    idx = 0

    while idx < len(queue):
        current = queue[idx]
        idx += 1

        if current == destination:
            break

        for neighbour, dist in enumerate(graph_data[current]):
            if dist > 0 and not discovered[neighbour]:
                discovered[neighbour] = True
                new_dist = distance[current] + dist
                if distance[neighbour] > new_dist:
                    distance[neighbour] = new_dist
                    previous[neighbour] = current

        neighbours_with_dist = tuple(
            (node, distance[node]) for node, weight in enumerate((dist for dist in graph_data[current])) if weight > 0
        )
        if len(neighbours_with_dist) > 0:
            queue.append(
                min(neighbours_with_dist, key=lambda x: x[1])[0]
            )

    best_route = []
    current = destination

    while current != source and current != -1:
        best_route.append(current)
        current = previous[current]
    best_route.append(source)
    best_route.reverse()
    return best_route, distance[destination]


def a_star(graph_data: list[list[int]], source: int, destination: int):
    queue = []
    discovered = [False] * len(graph_data)
    distance = [float('inf')] * len(graph_data)
    previous = [-1] * len(graph_data)

    # Heuristic which represent distance to destination
    _, _, hops_from_source = bfs(graph_data, source, destination)
    hops_to_destination = [hops_from_source[destination] - hops if hops != -1 else -1 for hops in hops_from_source]

    discovered[source] = True
    distance[source] = 0
    queue.append(source)
    idx = 0

    while idx < len(queue):
        current = queue[idx]
        idx += 1

        if current == destination:
            break

        for neighbour, dist in enumerate(graph_data[current]):
            if dist > 0:
                discovered[neighbour] = True
                new_dist = distance[current] + dist
                if distance[neighbour] > new_dist:
                    distance[neighbour] = new_dist
                    previous[neighbour] = current

        neighbours_with_dist = tuple(
            (node, distance[node] + hops_to_destination[node]) for node, weight in enumerate((dist for dist in graph_data[current])) if weight > 0
        )
        if len(neighbours_with_dist) > 0:
            queue.append(
                min(neighbours_with_dist, key=lambda x: x[1])[0]
            )

    best_route = []
    current = destination

    while current != source and current != -1:
        best_route.append(current)
        current = previous[current]
    best_route.append(source)
    best_route.reverse()
    return best_route, distance[destination]
