import math
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


def create_sub_graph_adj_lists(sub_graph_nodes: list[int], graph_data: list[list[int]]) -> dict[int, list[int]]:
    """ Create sub graph adjacency list with edges only among nodes in the nodes list. Return sub graph adj list. """
    sub_graph_adj_lists = dict((sub_node, []) for sub_node in sub_graph_nodes)
    for sub_node in sub_graph_nodes:
        for edge in sub_graph_nodes:
            edge_weight = graph_data[sub_node][edge]
            if edge_weight > 0:
                sub_graph_adj_lists[sub_node].append(edge)
    return sub_graph_adj_lists


def randomized_dfs(
        source: int, destination: int, sub_nodes: list[int], sub_graph_adj_lists: dict[int, list[int]]) -> list[int]:
    """ Returns random path from source to destination on the sub graph. """
    stack = [source]
    visited = dict((node, False) for node in sub_nodes)
    previous = dict((node, -1) for node in sub_nodes)
    visited[source] = True

    while not visited[destination] or not stack:
        current = stack.pop()

        neighbours = []
        for neigh in sub_graph_adj_lists[current]:
            if not visited[neigh]:
                visited[neigh] = True
                previous[neigh] = current
                # faster than random.shuffle() to randomly distribute neighbours in stack
                if random.getrandbits(1):  # return 0 or 1
                    neighbours.append(neigh)
                else:
                    stack.append(neigh)
        stack.extend(neighbours)

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
        source: int, destination: int, population_size: int, graph_data: list[list[int]]) -> list[list[int]]:
    """ Creates random sample of possible paths from source to destination. """
    sub_graph_nodes = reverse_dfs(destination, graph_data)

    sub_graph_adj_lists = create_sub_graph_adj_lists(sub_graph_nodes, graph_data)

    population = []
    for _ in range(population_size):
        population.append(randomized_dfs(source, destination, sub_graph_nodes, sub_graph_adj_lists))

    return population


def tournament(population: list[list[int]], graph_data: list[list[int]], remain_pct=0.5) -> list[list[int]]:
    population.sort(key=lambda path: fitness(path, graph_data))
    population = population[:math.ceil(len(population)*remain_pct)]
    return population


def genetic(graph_data: list[list[int]], source: int, destination: int):
    best_route = []
    return best_route
