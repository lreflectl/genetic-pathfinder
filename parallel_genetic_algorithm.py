import multiprocessing
from genetic_algorithm import create_sub_graph_adj_lists, crossover, fitness, fitness_all, generate_initial_population, mutation, reverse_dfs, selection


class ParallelGenetic():

    def __init__(self, graph_data: list[list[int]], population_size: int, cpus=2):
        self.pool = multiprocessing.Pool(cpus)
        self.graph_data = graph_data
        self.population_size = population_size

        self.max_generations_num = 6
        self.crossover_prob = 0.6
        self.mutation_prob = 0.1
        self.survival_pct = 0.5
        self.max_generations_unimproved = 2

        self.sub_graph_nodes = None
        self.sub_graph_adj_lists = None
        self.population = None
        self.path_lengths = None
        self.generations_unimproved = None
        self.last_best_length = None
        self.parents_ids = None


    def genetic(self, source: int, destination: int) -> list[int]:
        self.sub_graph_nodes = reverse_dfs(destination, self.graph_data)
        self.sub_graph_adj_lists = create_sub_graph_adj_lists(self.sub_graph_nodes, self.graph_data)
        self.population = generate_initial_population(
            source, destination, self.population_size, self.sub_graph_nodes, self.sub_graph_adj_lists
        )
        self.path_lengths = fitness_all(self.population, self.graph_data)
        self.generations_unimproved = 0
        self.last_best_length = float('inf')

        for generation in range(self.max_generations_num):
            # crossover selection
            self.parents_ids = selection(self.path_lengths, self.crossover_prob)
            # when some path has no pair, skip it
            if len(self.parents_ids) % 2 == 1:
                self.parents_ids.pop()

            # crossover through the population
            pairs_ids = range(0, len(self.parents_ids), 2)
            self.pool.map(self.crossover_pair, pairs_ids)
                
            # mutation selection, reverse probabilities to choose the worst paths for mutation first
            mutation_ids = selection(self.path_lengths, self.mutation_prob, reverse_prob=True)
            self.pool.map(self.mutate, mutation_ids)

            # survivors selection
            survivors_ids = selection(self.path_lengths, self.survival_pct, preserve_best=True)
            # if there are no survivors (one preserved), stop on current generation
            if len(survivors_ids) <= 1:
                break
            # best fitted path remain, others die
            self.population = [self.population[idx] for idx in survivors_ids]
            self.path_lengths = [self.path_lengths[idx] for idx in survivors_ids]

            current_best_length = min(self.path_lengths)
            if current_best_length >= self.last_best_length:
                self.generations_unimproved += 1
            else:
                self.generations_unimproved = 0
            self.last_best_length = current_best_length

            if self.generations_unimproved >= self.max_generations_unimproved:
                # print(f"Termination because there has been no improvement for {generations_unimproved} generations.")
                break

        # print('result paths =', population)
        best_path_id = self.path_lengths.index(min(self.path_lengths))
        return self.population[best_path_id]


    def crossover_pair(self, idx: int) -> None:
        parent1, parent2 = self.population[self.parents_ids[idx]], self.population[self.parents_ids[idx+1]]
        child1, child2 = crossover(parent1, parent2)
        self.population[self.parents_ids[idx]], self.population[self.parents_ids[idx+1]] = child1, child2
        # update new path fitness
        self.path_lengths[self.parents_ids[idx]] = fitness(child1, self.graph_data)
        self.path_lengths[self.parents_ids[idx + 1]] = fitness(child2, self.graph_data)

    
    def mutate(self, idx) -> None:
        self.population[idx] = mutation(self.population[idx], self.sub_graph_adj_lists)
        # update path length after mutation
        self.path_lengths[idx] = fitness(self.population[idx], self.graph_data)
