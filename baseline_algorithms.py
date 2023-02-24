import heapq


class Node:
    def __init__(self, idx, weight):
        self.idx = idx
        self.weight = weight

    def __gt__(self, other):
        return self.weight > other

    def __lt__(self, other):
        return self.weight < other

    def __repr__(self):
        return f"{self.idx}"


def dfs_connected(graph_data: list[list[int]]):
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
    heap = []
    discovered = [False] * len(graph_data)
    distance = [float('inf')] * len(graph_data)
    previous = [-1] * len(graph_data)

    discovered[source] = True
    distance[source] = 0
    heapq.heappush(heap, Node(source, 0))

    while heap:
        current = heapq.heappop(heap).idx
        discovered[current] = True

        for neighbour, dist in enumerate(graph_data[current]):
            if dist > 0:
                new_dist = distance[current] + dist
                if distance[neighbour] > new_dist:
                    distance[neighbour] = new_dist
                    previous[neighbour] = current

        neighbours_with_dist = (
            (node, distance[node]) for node, weight in enumerate((dist for dist in graph_data[current])) if weight > 0
        )
        for node in neighbours_with_dist:
            if not discovered[node[0]]:
                heapq.heappush(heap, Node(node[0], node[1]))

    best_route = []
    current = destination

    while current != source and current != -1:
        best_route.append(current)
        current = previous[current]
    best_route.append(source)
    best_route.reverse()
    return best_route, distance[destination]


def a_star(graph_data: list[list[int]], source: int, destination: int):
    heap = []
    discovered = [False] * len(graph_data)
    distance = [float('inf')] * len(graph_data)
    previous = [-1] * len(graph_data)

    # Heuristic which represent distance to destination
    _, _, hops_from_source = bfs(graph_data, source, destination)
    hops_to_destination = [hops_from_source[destination] - hops if hops != -1 else -1 for hops in hops_from_source]

    discovered[source] = True
    distance[source] = 0
    heapq.heappush(heap, Node(source, 0))

    while heap:
        current = heapq.heappop(heap).idx
        discovered[current] = True

        for neighbour, dist in enumerate(graph_data[current]):
            if dist > 0:
                new_dist = distance[current] + dist
                if distance[neighbour] > new_dist:
                    distance[neighbour] = new_dist
                    previous[neighbour] = current

        neighbours_with_dist = (
            (node, distance[node]) for node, weight in enumerate((dist for dist in graph_data[current])) if weight > 0
        )
        for node in neighbours_with_dist:
            if not discovered[node[0]]:
                heapq.heappush(heap, Node(node[0], node[1] + hops_to_destination[node[0]]))

    best_route = []
    current = destination

    while current != source and current != -1:
        best_route.append(current)
        current = previous[current]
    best_route.append(source)
    best_route.reverse()
    return best_route, distance[destination]
