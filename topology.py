import baseline_algorithms


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
        if self._is_weighted:
            for n1, n2, weight in edges:
                self.data[n1][n2] = weight
                if not is_directed:
                    self.data[n2][n1] = weight
        else:
            for n1, n2 in edges:
                self.data[n1][n2] = 1
                if not is_directed:
                    self.data[n2][n1] = 1

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
            if not self._is_directed:
                self.data[n2][n1] = weight
        else:
            if len(edge) != 2:
                raise Exception('Wrong edge type for unweighted graph, should be tuple(int, int).')
            n1, n2 = edge
            self.data[n1][n2] = 1
            if not self._is_directed:
                self.data[n2][n1] = 1

    def remove_edge(self, edge: tuple[int, int]):
        n1, n2 = edge
        self.data[n1][n2] = 0
        if not self._is_directed:
            self.data[n2][n1] = 0


def main():
    num_nodes = 4
    edges = [(0, 1, 8), (0, 3, 5), (1, 3, 4), (1, 2, 5), (2, 3, 6)]
    graph = Graph(num_nodes, edges)
    graph.add_edge((2, 2, 4))
    graph.remove_edge((0, 3))
    print(graph)
    print(baseline_algorithms.dfs(graph, 0))


if __name__ == '__main__':
    main()
