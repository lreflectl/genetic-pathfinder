import time
from genetic_algorithm import *
import python_graph


edges = [(0, 2, 8), (0, 3, 2), (0, 4, 7), (0, 5, 4), (2, 1, 2), (3, 6, 6), (4, 7, 2), (5, 7, 3), (5, 6, 3),
         (6, 8, 5), (6, 9, 2), (7, 8, 1), (8, 10, 4), (8, 12, 3), (9, 10, 3), (11, 6, 3), (12, 7, 5)]
num_nodes = 13
source, destination = 0, 10

graph = python_graph.Graph(num_nodes, edges, is_directed=True)

# --- SETUP ---
sub_nodes = reverse_dfs(destination, graph.data)
sub_adj_lists = create_sub_graph_adj_lists(sub_nodes, graph.data)
population = generate_initial_population(source, destination, 100, sub_nodes, sub_adj_lists)
path_lengths = fitness_all(population, graph.data)
# -------------
start = time.perf_counter()
for _ in range(1000):
    selected_ids = selection(path_lengths)
end = time.perf_counter()
print(f"Result time = {end-start:.2f} sec")
# -------------
# start = time.perf_counter()
# for _ in range(1000):
#     selected = mutation(population[selected_ids[0]], sub_adj_lists)
# end = time.perf_counter()
# print(f"Result time = {end-start:.2f} sec")
# ------------
path_lengths = [2, 3, 4, 5, 6, 7]
frequencies = [0, 0, 0, 0, 0, 0]
for i in range(10000):
    selected_ids = selection(path_lengths)
    for idx in selected_ids:
        frequencies[idx] += 1
print(frequencies)
