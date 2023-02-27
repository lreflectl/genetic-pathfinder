import time
from genetic_algorithm import *


def generate_initial_population_profiling(
        source: int, destination: int, population_size: int, graph_data: list[list[int]]
) -> list[list[int]]:
    """ Creates random sample of possible paths from source to destination. """
    reverse_dfs_start = time.perf_counter()
    for _ in range(10000):
        sub_graph_nodes = reverse_dfs(destination, graph_data)
    print(f"reverse_dfs time = {time.perf_counter() - reverse_dfs_start}")

    create_sub_graph_start = time.perf_counter()
    for _ in range(10000):
        sub_graph_data = create_sub_graph(sub_graph_nodes, graph_data)
    print(f"create_sub_graph time = {time.perf_counter() - create_sub_graph_start}")

    population_multiple_start = time.perf_counter()
    for _ in range(10000):
        population = []
        for i in range(population_size):
            population.append(randomized_dfs(source, destination, len(sub_graph_nodes), sub_graph_data))
    print(f"population_multiple time = {time.perf_counter() - population_multiple_start}")

    population_single_start = time.perf_counter()
    for _ in range(10000):
        randomized_dfs(source, destination, len(sub_graph_nodes), sub_graph_data)
    print(f"population_single time = {time.perf_counter() - population_single_start}")

    return population


def randomized_dfs_profiling(source: int, destination: int, sub_nodes_num: int, sub_graph_data: list[list[int]]) -> list[int]:
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
