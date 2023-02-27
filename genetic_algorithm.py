import random


def reverse_dfs(destination: int, graph_data: list[list[int]]) -> list[int]:
    """ Returns list of nodes from which destination is reachable. """
    num_nodes = len(graph_data)
    stack = [destination]
    visited = [False] * num_nodes

    while stack:
        current = stack.pop()
        for neighbour in range(num_nodes):
            if graph_data[neighbour][current] > 0 and not visited[neighbour]:
                stack.append(neighbour)
        visited[current] = True

    nodes = [node for node, reached in enumerate(visited) if reached]
    return nodes


def create_sub_graph(nodes: list[int], graph_data: list[list[int]]) -> list[list[int]]:
    """ Create copy of a graph data with edges only among nodes in the list. Returns new graph data matrix. """
    sub_graph_data = [[0] * len(graph_data) for _ in range(len(graph_data))]
    for node in nodes:
        for edge in nodes:
            sub_graph_data[node][edge] = graph_data[node][edge]
    return sub_graph_data


def randomized_dfs(source: int, destination: int, sub_nodes_num: int, sub_graph_data: list[list[int]]) -> list[int]:
    """ Returns random path from source to destination on the sub graph. """
    stack = [source]
    visited = [False] * len(sub_graph_data)

    previous = [-1] * len(sub_graph_data)

    for _ in range(sub_nodes_num):
        current = stack.pop()
        if current == destination:
            break

        neighbours = []
        for neighbour, weight in enumerate(sub_graph_data[current]):
            if weight > 0 and not visited[neighbour]:
                neighbours.append(neighbour)
                previous[neighbour] = current
        random.shuffle(neighbours)
        stack.extend(neighbours)
        visited[current] = True

    path = []
    current = destination
    while current != -1:
        path.append(current)
        current = previous[current]
    path.reverse()

    return path


def fitness(path: list[int], graph_data: list[list[int]]) -> float:
    """ Calculate path cost. Returns inf if the nodes are not connected. """
    path_cost = 0
    for idx in range(len(path) - 1):
        n1, n2 = path[idx], path[idx + 1]
        edge_cost = graph_data[n1][n2]
        if edge_cost != 0:
            path_cost += graph_data[n1][n2]
        else:
            path_cost = float('inf')
            break
    return path_cost


def generate_initial_population(
        source: int, destination: int, population_size: int, graph_data: list[list[int]]
) -> list[list[int]]:
    """ Creates random sample of possible paths from source to destination. """
    sub_graph_nodes = reverse_dfs(destination, graph_data)

    sub_graph_data = create_sub_graph(sub_graph_nodes, graph_data)

    population = []
    for i in range(population_size):
        population.append(randomized_dfs(source, destination, len(sub_graph_nodes), sub_graph_data))
    return population


def tournament(population: list[list[int]], graph_data: list[list[int]], remain_pct=0.5) -> list[list[int]]:
    population.sort(key=lambda path: fitness(path, graph_data))
    population = population[:round(len(population)*remain_pct)]
    return population


def genetic(graph_data: list[list[int]], source: int, destination: int):
    best_route = []
    return best_route
