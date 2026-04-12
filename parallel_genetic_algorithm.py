import multiprocessing
from genetic_algorithm import create_sub_graph_adj_lists, crossover, fitness, fitness_all, generate_initial_population, mutation, reverse_dfs, selection


class ParallelGenetic():

    def __init__(self, graph_data: list[list[int]], population_size: int, cpus=2):
        self.graph_data = graph_data
        self.population_size = population_size
        self.pool = multiprocessing.Pool(cpus)

        self.max_generations_num = 6
        self.crossover_prob = 0.6
        self.mutation_prob = 0.1
        self.survival_pct = 0.5
        self.max_generations_unimproved = 2


    def genetic(self, source: int, destination: int) -> list[int]:
        sub_graph_nodes = reverse_dfs(destination, self.graph_data)
        sub_graph_adj_lists = create_sub_graph_adj_lists(sub_graph_nodes, self.graph_data)
        population = generate_initial_population(source, destination, self.population_size, sub_graph_nodes, sub_graph_adj_lists)
        path_lengths = fitness_all(population, self.graph_data)
        generations_unimproved = 0
        last_best_length = float('inf')

        for generation in range(self.max_generations_num):
            # crossover selection
            parents_ids = selection(path_lengths, self.crossover_prob)
            # when some path has no pair, skip it
            if len(parents_ids) % 2 == 1:
                parents_ids.pop()

            # crossover through the population
            pairs_ids = range(0, len(parents_ids), 2)
            self.pool.starmap(crossover_pair, ((idx, population, parents_ids, path_lengths, self.graph_data) for idx in pairs_ids))
                
            # mutation selection, reverse probabilities to choose the worst paths for mutation first
            mutation_ids = selection(path_lengths, self.mutation_prob, reverse_prob=True)
            self.pool.starmap(mutate, ((idx, population, sub_graph_adj_lists, path_lengths, self.graph_data) for idx in mutation_ids))

            # survivors selection
            survivors_ids = selection(path_lengths, self.survival_pct, preserve_best=True)
            # if there are no survivors (one preserved), stop on current generation
            if len(survivors_ids) <= 1:
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

            if generations_unimproved >= self.max_generations_unimproved:
                # print(f"Termination because there has been no improvement for {generations_unimproved} generations.")
                break

        # print('result paths =', population)
        best_path_id = path_lengths.index(min(path_lengths))
        return population[best_path_id]


def crossover_pair(idx, population, parents_ids, path_lengths, graph_data) -> None:
    parent1, parent2 = population[parents_ids[idx]], population[parents_ids[idx+1]]
    child1, child2 = crossover(parent1, parent2)
    population[parents_ids[idx]], population[parents_ids[idx+1]] = child1, child2
    # update new path fitness
    path_lengths[parents_ids[idx]] = fitness(child1, graph_data)
    path_lengths[parents_ids[idx + 1]] = fitness(child2, graph_data)


def mutate(idx, population, sub_graph_adj_lists, path_lengths, graph_data) -> None:
    population[idx] = mutation(population[idx], sub_graph_adj_lists)
    # update path length after mutation
    path_lengths[idx] = fitness(population[idx], graph_data)
