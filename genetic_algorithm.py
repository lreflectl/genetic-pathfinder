import random
import time

import numpy as np


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
                neighbours.append(neigh)
        random.shuffle(neighbours)  # can be improved
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


def fitness_all(population: list[list[int]], graph_data: list[list[int]]) -> list[float]:
    """ Calculate all path costs of the population. """
    results = []
    for path in population:
        path_cost = 0
        for idx in range(len(path) - 1):
            n1, n2 = path[idx], path[idx + 1]
            edge_cost = graph_data[n1][n2]
            if edge_cost != 0:
                path_cost += graph_data[n1][n2]
            else:
                path_cost = float('inf')
                break
        results.append(path_cost)
    return results


def generate_initial_population(
        source: int, destination: int, population_size: int, sub_graph_nodes: list[int],
        sub_graph_adj_lists: dict[int, list[int]]
) -> list[list[int]]:
    """ Creates random sample of possible paths from source to destination. """

    population = [[] for _ in range(population_size)]
    for idx in range(population_size):
        population[idx] = randomized_dfs(source, destination, sub_graph_nodes, sub_graph_adj_lists)

    return population


def selection(path_lengths: list[float], remain_pct=0.5, reverse_prob=False, preserve_best=False) -> list[int]:
    """ Randomly pick selected percent of paths of the population based on their fitness.
        Return ids of selected paths. """
    remain_num = round(len(path_lengths) * remain_pct)

    if remain_num < 1:
        return []

    min_path = min(path_lengths)
    min_path_idx = path_lengths.index(min_path)
    if not reverse_prob:
        max_path = max(path_lengths)

        def reverse_path_length(path_len):
            return max_path - path_len + min_path
        path_lengths = map(reverse_path_length, path_lengths)

    # create a dict for saving the initial indexes of paths after multiple roulette spins
    path_lengths_dict = {path_idx: path_length for path_idx, path_length in enumerate(path_lengths)}

    if preserve_best:
        path_lengths_dict.pop(min_path_idx)
        remain_num -= 1

    remain_ids = []
    for spin in range(remain_num):
        p_sum = sum(path_lengths_dict.values())
        fixed_point = random.randint(0, p_sum)
        cumulative_length = 0
        for path_idx, length in path_lengths_dict.items():
            cumulative_length += length
            if fixed_point <= cumulative_length:
                remain_ids.append(path_idx)
                path_lengths_dict.pop(path_idx)
                break

    if preserve_best:
        remain_ids.append(min_path_idx)

    return remain_ids


# def selection(path_lengths: list[float], remain_pct=0.5, reverse_prob=False) -> list[int]:
#     """ Randomly pick selected percent of paths of the population based on their fitness.
#         Return ids of selected paths. """
#     population_len = len(path_lengths)
#     remain_num = round(population_len * remain_pct)
#
#     if remain_num < 1:
#         return []
#
#     if not reverse_prob:
#         offset = max(path_lengths) + min(path_lengths)
#         path_lengths = tuple(offset - path_length for path_length in path_lengths)
#
#     path_lengths = np.array(path_lengths)
#     selection_probabilities = path_lengths / path_lengths.sum()
#
#     remain_ids = np.random.choice(
#         np.arange(0, population_len), p=selection_probabilities, size=remain_num, replace=False
#     )
#
#     return list(remain_ids)


def crossover(path1: list[int], path2: list[int]) -> tuple[list[int], list[int]]:
    """ Randomly pick common node for the paths, then cut them and connect pieces in with each other.
        Support only simple paths. Return two new children. """

    common_nodes = [node for node in path1[1:-2] if node in path2]
    if len(common_nodes) < 1:
        return path1, path2

    node = random.choice(common_nodes)
    node_id_in_path1 = path1.index(node)
    node_id_in_path2 = path2.index(node)

    child1 = path1[:node_id_in_path1] + path2[node_id_in_path2:]
    child2 = path2[:node_id_in_path2] + path1[node_id_in_path1:]
    return child1, child2


def crossover_all(parents: list[list[int]]) -> list[list[int]]:
    # if some path has no pair, then leave it as is
    last_path = None
    if len(parents) % 2 == 1:
        last_path = parents[-1]

    children = []
    for idx in range(0, len(parents) - 1, 2):
        child1, child2 = crossover(parents[idx], parents[idx+1])
        children.append(child1)
        children.append(child2)

    if last_path:
        children.append(last_path)

    return children


def mutation(path: list[int], sub_graph_adj_lists: dict[int, list[int]]) -> list[int]:
    """ Randomly pick node and check if possible to replace the node with a random link.
        Replace if possible and return mutated path, if not return original path. """
    if len(path) < 3:
        return path

    node_id = random.choice(range(len(path) - 2))
    current = path[node_id]
    next_node = path[node_id + 1]
    after_next = path[node_id + 2]

    currents_links = sub_graph_adj_lists[current].copy()
    currents_links.remove(next_node)

    analog_links = []
    for link in currents_links:
        if after_next in sub_graph_adj_lists[link]:
            analog_links.append(link)

    if analog_links:
        path[node_id + 1] = random.choice(analog_links)
        return path

    return path


def genetic(graph_data: list[list[int]], source: int, destination: int) -> list[int]:
    population_size = 4
    max_generations_num = 6
    crossover_prob = 0.5
    mutation_prob = 0.1
    survival_pct = 0.6
    max_generations_unimproved = 2

    sub_graph_nodes = reverse_dfs(destination, graph_data)
    sub_graph_adj_lists = create_sub_graph_adj_lists(sub_graph_nodes, graph_data)
    population = generate_initial_population(
        source, destination, population_size, sub_graph_nodes, sub_graph_adj_lists
    )
    path_lengths = fitness_all(population, graph_data)
    generations_unimproved = 0
    last_best_length = float('inf')
    best_path = []

    for generation in range(max_generations_num):
        # crossover selection
        parents_ids = selection(path_lengths, crossover_prob)
        # when some path has no pair, skip it
        if len(parents_ids) % 2 == 1:
            parents_ids.pop()
        # crossover through the population
        for idx in range(0, len(parents_ids), 2):
            parent1, parent2 = population[parents_ids[idx]], population[parents_ids[idx+1]]
            child1, child2 = crossover(parent1, parent2)
            population[parents_ids[idx]], population[parents_ids[idx+1]] = child1, child2
            # update new path fitness
            path_lengths[parents_ids[idx]] = fitness(child1, graph_data)
            path_lengths[parents_ids[idx + 1]] = fitness(child2, graph_data)

        # mutation selection, reverse probabilities to choose the worst paths for mutation first
        mutation_ids = selection(path_lengths, mutation_prob, reverse_prob=True)

        for idx in mutation_ids:
            population[idx] = mutation(population[idx], sub_graph_adj_lists)
            # update path length after mutation
            path_lengths[idx] = fitness(population[idx], graph_data)

        # survivors selection
        survivors_ids = selection(path_lengths, survival_pct, preserve_best=True)
        # if there are no survivors, stop on current generation
        if not survivors_ids:
            break
        # best fitted path remain, others die
        population = [population[idx] for idx in survivors_ids]
        path_lengths = [path_lengths[idx] for idx in survivors_ids]

        current_best_length = min(path_lengths)
        if current_best_length >= last_best_length:
            generations_unimproved += 1
        else:
            generations_unimproved = 0
        last_best_length = current_best_length

        if generations_unimproved >= max_generations_unimproved:
            # print(f"Termination because there has been no improvement for {generations_unimproved} generations.")
            break

    # print('result paths =', population)
    best_path_id = path_lengths.index(min(path_lengths))
    return population[best_path_id]
