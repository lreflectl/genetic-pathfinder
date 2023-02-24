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


def randomized_dfs(source: int, destination: int, graph_data: list[list[int]]) -> list[int]:
    """ Returns random path from source to destination on limited by reverse_dfs() graph. """
    pass


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


def get_common_nodes(source: int, destination: int, graph_data: list[list[int]]):
    """ Creates list of nodes reachable both from destination and source """
    source_reachable = set()
    destination_reachable = set()


def generate_initial_population(source: int, destination: int, graph_adj_lists: list[list[int]]) -> list[list[int]]:
    """ Creates random sample of possible paths from source to destination. """
    population_size = 100
    for path_num in range(population_size):
        current = graph_adj_lists[source]
        visited = [False] * len(graph_adj_lists)

        while current != destination:
            pass




def genetic(graph_data: list[list[int]], source: int, destination: int):



    best_route = []
    return best_route
