import baseline_algorithms
from matplotlib import pyplot as plt
import networkx as nx
import time
import random
import genetic_algorithm


class Graph:
    def __init__(self, num_nodes, edges, is_directed=False):
        if len(edges) < 1:
            raise Exception('Graph should contain at least one node.')
        if len(edges[0]) == 2:
            self._is_weighted = False
        elif len(edges[0]) == 3:
            self._is_weighted = True
        else:
            raise Exception('Unsupported edge type.')

        self._is_directed = is_directed
        self.num_nodes = num_nodes
        self.data = [[0] * num_nodes for _ in range(num_nodes)]
        self.adjacency_lists = [[] * num_nodes for _ in range(num_nodes)]
        if self._is_weighted:
            for n1, n2, weight in edges:
                self.data[n1][n2] = weight
                self.adjacency_lists[n1].append(n2)
                if not is_directed:
                    self.data[n2][n1] = weight
                    self.adjacency_lists[n2].append(n1)
        else:
            for n1, n2 in edges:
                self.data[n1][n2] = 1
                self.adjacency_lists[n1].append(n2)
                if not is_directed:
                    self.data[n2][n1] = 1
                    self.adjacency_lists[n2].append(n1)

    def __repr__(self):
        header = '    '
        for i in range(len(self.data)):
            header += f'{i}: '
        header += '\n'
        return header + '\n'.join([f'{n}: {neighbours}' for n, neighbours in enumerate(self.data)])

    def __str__(self):
        return self.__repr__()

    def add_edge(self, edge: tuple[int, ...]):
        if self._is_weighted:
            if len(edge) != 3:
                raise Exception('Wrong edge type for weighted graph, should be tuple(int, int, int).')
            n1, n2, weight = edge
            self.data[n1][n2] = weight
            self.adjacency_lists[n1].append(n2)
            if not self._is_directed:
                self.data[n2][n1] = weight
                self.adjacency_lists[n2].append(n1)
        else:
            if len(edge) != 2:
                raise Exception('Wrong edge type for unweighted graph, should be tuple(int, int).')
            n1, n2 = edge
            self.data[n1][n2] = 1
            self.adjacency_lists[n1].append(n2)
            if not self._is_directed:
                self.data[n2][n1] = 1
                self.adjacency_lists[n2].append(n1)

    def remove_edge(self, edge: tuple[int, int]):
        n1, n2 = edge
        self.data[n1][n2] = 0
        self.adjacency_lists[n1].remove(n2)
        if not self._is_directed:
            self.data[n2][n1] = 0
            self.adjacency_lists[n2].remove(n1)


def draw_directed_weighted_graph(edges, path=None):
    edges = ((n1, n2, {"weight": weight}) for n1, n2, weight in edges)
    graph = nx.DiGraph(edges)
    position = nx.arf_layout(graph)
    if path:
        node_colors = ["#72f536" if node in path else "#4287f5" for node in graph.nodes()]
    else:
        node_colors = "#4287f5"
    nx.draw(graph, pos=position, with_labels=True, font_weight='bold', node_color=node_colors)
    edge_weight = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos=position, edge_labels=edge_weight)
    plt.show()


def generate_random_edges(num_nodes):
    edges = []
    random.seed(1)
    unique_edges = set()
    for edge in range(num_nodes * 2):
        unique_rands = random.sample(range(num_nodes), k=2)
        unique_edges.add((unique_rands[0], unique_rands[1]))
    for edge in unique_edges:
        edges.append((*edge, random.randint(1, 10)))
    return edges


def main():
    num_nodes = 30
    edges = [(0, 2, 8), (0, 3, 2), (0, 4, 7), (0, 5, 4), (2, 1, 2), (3, 6, 6), (4, 7, 2), (5, 7, 3), (6, 8, 5),
             (6, 9, 2), (7, 8, 1), (8, 10, 4), (8, 12, 3), (9, 10, 3), (11, 6, 3), (12, 7, 5)]
    # edges = generate_random_edges(num_nodes)

    graph = Graph(num_nodes, edges, is_directed=True)
    print(graph)
    print(graph.adjacency_lists)
    # draw_directed_weighted_graph(edges)

    # ------ Algorithms time comparison ------

    # source, destination = 18, 29
    #
    # dijkstra_start = time.perf_counter()
    # for i in range(100000):
    #     result = baseline_algorithms.dijkstra(graph.data, source, destination)
    # print(f"Dijkstra time = {time.perf_counter() - dijkstra_start:.2f} sec")
    #
    # a_star_start = time.perf_counter()
    # for i in range(100000):
    #     result = baseline_algorithms.a_star(graph.data, source, destination)
    # print(f"A-Star time = {time.perf_counter() - a_star_start:.2f} sec")

    # --------------------------------------

    # a_star_start = time.perf_counter()
    # result = baseline_algorithms.a_star(graph.data, 18, 29)
    # print(f"A-Star time = {time.perf_counter() - a_star_start:.2f} sec")
    # print(result)
    # draw_directed_weighted_graph(edges, path=result[0])

    # ------------------------------

    sub_graph_nodes = genetic_algorithm.reverse_dfs(10, graph.data)
    sub_graph_adj_lists = dict(
        ( node, list(filter(lambda n: n in sub_graph_nodes, graph.adjacency_lists[node])) )
        for node in sub_graph_nodes
    )
    print(sub_graph_adj_lists)
    result = genetic_algorithm.randomized_dfs(0, 10, sub_graph_adj_lists)
    print(result)
    print(genetic_algorithm.fitness(result, graph.data))


if __name__ == '__main__':
    main()
