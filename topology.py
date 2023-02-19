class Graph:
    def __init__(self, num_nodes, edges):
        self.num_nodes = num_nodes
        self.data = [[0] * num_nodes for _ in range(num_nodes)]
        for n1, n2 in edges:
            self.data[n1][n2] = 1
            self.data[n2][n1] = 1

    def __repr__(self):
        header = '    '
        for i in range(len(self.data)):
            header += f'{i}: '
        header += '\n'
        return header + '\n'.join([f'{n}: {neighbours}' for n, neighbours in enumerate(self.data)])

    def __str__(self):
        return self.__repr__()

    def add_edge(self, edge: tuple[int, int]):
        n1, n2 = edge
        self.data[n1][n2] = 1
        self.data[n2][n1] = 1

    def remove_edge(self, edge: tuple[int, int]):
        n1, n2 = edge
        self.data[n1][n2] = 0
        self.data[n2][n1] = 0


def main():
    num_nodes = 4
    edges = [(0, 1), (0, 3), (1, 3), (1, 2), (2, 3)]
    graph = Graph(num_nodes, edges)
    graph.add_edge((2, 2))
    graph.remove_edge((0, 3))
    print(graph)


if __name__ == '__main__':
    main()
