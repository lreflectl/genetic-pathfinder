import time
import random
import fnss
import genetic_algorithm
import baseline_algorithms
import python_graph
import networkx as nx
from matplotlib import pyplot as plt


def draw_fnss_topology(topology):
    nx.draw(topology)
    plt.show()


def main():
    # fat_tree_topology = fnss.fat_tree_topology(4)
    # draw_fnss_topology(fat_tree_topology.graph)

    num_nodes = 13
    edges = [(0, 2, 8), (0, 3, 2), (0, 4, 7), (0, 5, 4), (2, 1, 2), (3, 6, 6), (4, 7, 2), (5, 7, 3), (5, 6, 3),
             (6, 8, 5), (6, 9, 2), (7, 8, 1), (8, 10, 4), (8, 12, 3), (9, 10, 3), (11, 6, 3), (12, 7, 5)]

    # num_nodes = 100
    # edges = [(0, n, n) for n in range(1, 99)]
    # edges.extend([(n, 99, n) for n in range(1, 99)])
    python_graph.draw_directed_weighted_graph(edges)

    graph = python_graph.Graph(num_nodes, edges, is_directed=True)

    # ------ Algorithms time comparison ------
    # random.seed(123)
    source, destination = 0, 10

    dijkstra_start = time.perf_counter()
    cumulative_path_length = 0
    experiments = 10000
    for i in range(experiments):
        best_path = baseline_algorithms.dijkstra(graph.data, source, destination)
        cumulative_path_length += best_path[1]
    print(f"Dijkstra time = {time.perf_counter() - dijkstra_start:.2f} sec, path = {best_path}")
    print(f"Average path length = {cumulative_path_length/experiments}")

    genetic_start = time.perf_counter()
    cumulative_path_length = 0
    for i in range(experiments):
        best_path = genetic_algorithm.genetic(graph.data, source, destination)
        cumulative_path_length += genetic_algorithm.fitness(best_path, graph.data)
    print(f"Genetic time = {time.perf_counter() - genetic_start:.2f} sec,"
          f" path = {(best_path, genetic_algorithm.fitness(best_path, graph.data))}")
    print(f"Average path length = {cumulative_path_length / experiments}")

    # --------------------------------------

    # a_star_start = time.perf_counter()
    # result = baseline_algorithms.a_star(graph.data, 18, 29)
    # print(f"A-Star time = {time.perf_counter() - a_star_start:.2f} sec")
    # print(result)
    # draw_directed_weighted_graph(edges, path=result[0])

    # ------------------------------

    # random.seed(123)
    # genetic_start = time.perf_counter()
    # for i in range(100):
    #     best_path = genetic_algorithm.genetic(graph.data, source=0, destination=99)
    # print(f"Genetic time = {time.perf_counter() - genetic_start:.2f} sec")
    # print(f'Best path: {best_path}, with length = {genetic_algorithm.fitness(best_path, graph.data)}')
    #
    # genetic_start = time.perf_counter()
    # for i in range(100):
    #     best_path = baseline_algorithms.dijkstra(graph.data, source=0, destination=99)
    # print(f"Dijkstra time = {time.perf_counter() - genetic_start:.2f} sec")
    # print(f'Best path: {best_path[0]}, with length = {best_path[1]}')

    # print(genetic_algorithm.mutation([0, 5, 9], graph.adjacency_lists))
    # print(genetic_algorithm.crossover([0, 5, 9], [0, 1, 9]))
    # print(genetic_algorithm.fitness([0, 1, 9], graph.data))

    # sub_graph_nodes = genetic_algorithm.reverse_dfs(99, graph.data)
    # sub_graph_adj_lists = genetic_algorithm.create_sub_graph_adj_lists(sub_graph_nodes, graph.data)
    # population = genetic_algorithm.generate_initial_population(
    #     0, 99, 10, sub_graph_nodes, sub_graph_adj_lists
    # )
    # print(population)


if __name__ == '__main__':
    main()
