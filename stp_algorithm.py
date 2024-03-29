def build_link_tree(links: list[tuple[int, int, dict]]):
    """ Create hash map of the links and their metrics """
    link_tree = {}
    for link in links:
        link_tree.setdefault(link[0], {})
        link_tree[link[0]].setdefault(link[1], [])
        link_tree[link[0]][link[1]].append(link[2])
    return link_tree


def remove_cycles(link_tree: dict[int, dict[int, list]]):
    """ Remove links with the same node in the tree """
    for key in link_tree.keys():
        while key in link_tree[key]:
            link_tree[key].pop(key)


def remove_identical_links(link_tree: dict[int, dict[int, list]], metric='weight'):
    """ Remove multiple links between two nodes and leave the shortest one.
        Unpack list wrapped values. """
    for node, adjacent_nodes in link_tree.items():
        for adj_node, link_values in adjacent_nodes.items():
            # if adjacent node is connected by multiple links then pick the best one
            if len(link_values) > 1:
                min_link_value = min(link_values, key=lambda value: value[metric])
                link_tree[node][adj_node] = min_link_value
            elif len(link_values) == 1:
                link_tree[node][adj_node] = link_values[0]


def build_spanning_tree(link_tree: dict[int, dict[int, dict]], nodes: list[int], root_node: int, metric='weight') \
        -> dict[int, dict[int, dict]] or None:
    """ Build minimal spanning tree of the given tree of links. It is assumed that the input tree
        do not have redundant links and same node cycles. Return None if graph is not connected.
        Tip: it is better to pick center node as root. """
    if not link_tree:
        return None

    spanning_tree = {}
    visited = {node: False for node in nodes}
    stack = []
    current_node = root_node

    # Iterate until all nodes marked as visited
    while True:
        # If current node already has been visited, then its neighbours already have been put in the stack,
        # so skip adding them again
        if not visited[current_node]:
            # Check if current node has outbound links
            if current_node in link_tree:
                links = [(current_node, dst_node, metrics) for dst_node, metrics in link_tree[current_node].items()]
                # Descending sort of the adjacent links to extend the stack
                links = sorted(links, key=lambda link: link[2][metric], reverse=True)
                stack.extend(links)
            visited[current_node] = True

        if all(visited.values()):
            break

        # If stack is empty while not visited all nodes, then the graph is not connected
        if not stack:
            return None

        src_node, dst_node, metrics = stack.pop()
        # Add only links to new nodes
        if not visited[dst_node]:
            spanning_tree.setdefault(src_node, {})
            spanning_tree[src_node][dst_node] = metrics
            current_node = dst_node

    return spanning_tree


def set_reverse_links(spanning_tree: dict[int, dict[int, dict]], link_tree: dict[int, dict[int, dict]]):
    """ For every link in the spanning tree set reverse one if it exists in the link tree """
    reverse_links_tree = {}
    for src_node in spanning_tree.keys():
        for dst_node, metrics in spanning_tree[src_node].items():
            try:
                new_metrics = link_tree[dst_node][src_node]
                reverse_links_tree.setdefault(dst_node, {})
                reverse_links_tree[dst_node][src_node] = new_metrics
            except KeyError:
                print(f'No reverse link from {dst_node} to {src_node}!')
    for src_node, dst_nodes in reverse_links_tree.items():
        spanning_tree.setdefault(src_node, {})
        spanning_tree[src_node].update(dst_nodes)


def main():
    # nodes = [1, 2, 3, 4, 5]
    # links = [(1, 2, {'length': 6}), (2, 3, {'length': 8}), (3, 4, {'length': 7}),
    #          (4, 5, {'length': 9}), (4, 5, {'length': 9}), (3, 3, {'length': 7}),
    #          (1, 5, {'length': 7}), (5, 2, {'length': 8}), (4, 2, {'length': 8})]

    nodes = [1, 2, 3, 4]
    links = [(1, 2, {'port': 2, 'weight': 1}), (2, 1, {'port': 3, 'weight': 1}),
             (2, 3, {'port': 2, 'weight': 1}), (3, 2, {'port': 3, 'weight': 1}),
             (3, 4, {'port': 2, 'weight': 1}), (4, 3, {'port': 2, 'weight': 1})]

    link_tree = build_link_tree(links)
    print(link_tree)
    remove_cycles(link_tree)
    remove_identical_links(link_tree)
    spanning_tree = build_spanning_tree(link_tree, nodes, root_node=1)
    print("Original st:", spanning_tree)
    set_reverse_links(spanning_tree, link_tree)
    print("With rv. st:", spanning_tree)


if __name__ == '__main__':
    main()
