import random
from typing import List
import tkinter as tk
from tkinter import ttk, messagebox
random.seed(1)

def fitness_function(chromosome: List[int], weights: List[int], values: List[int], max_weight: int) -> int:
    total_weight = sum(x * y for x, y in zip(chromosome, weights))
    total_value = sum(x * y for x, y in zip(chromosome, values))
    if total_weight <= max_weight:
        return total_value
    else:
        return 0


def selection_function(population: List[List[int]], fitness_values: List[int]) -> List[List[int]]:
    total_fitness = sum(fitness_values)
    relative_fitness = [f / total_fitness for f in fitness_values]
    cumulative_prob = [sum(relative_fitness[:i + 1]) for i in range(len(relative_fitness))]
    parents = []
    for _ in range(len(population)):
        r = random.random()
        for i, c in enumerate(cumulative_prob):
            if r < c:
                parents.append(population[i])
                break
    return parents


def crossover_function(parents: List[List[int]], crossover_rate: float) -> List[List[int]]:
    random.shuffle(parents)
    offspring = []
    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        r = random.random()
        if r < crossover_rate:
            point = random.randint(1, len(parent1) - 2)
            offspring1 = parent1[:point] + parent2[point:]
            offspring2 = parent2[:point] + parent1[point:]
            offspring.append(offspring1)
            offspring.append(offspring2)
        else:
            offspring.append(parent1)
            offspring.append(parent2)
    return offspring


def mutation_function(offspring: List[List[int]], mutation_rate: float) -> List[List[int]]:
    for i in range(len(offspring)):
        for j in range(len(offspring[i])):
            r = random.random()
            if r < mutation_rate:
                offspring[i][j] = 1 - offspring[i][j]
    return offspring


def genetic_algorithm(weights: List[int], values: List[int], max_weight: int, population_size: int, parent_count: int, probability_of_ones: float, crossover_rate: float, mutation_rate: float, max_generations: int) -> List[int]:
    population = []
    for _ in range(population_size):
        chromosome = [random.choices([0, 1], weights=[1 - probability_of_ones, probability_of_ones])[0] for _ in range(len(weights))]
        population.append(chromosome)

    best_chromosome = None
    best_fitness = 0

    for generation in range(max_generations):
        fitness_values = [fitness_function(c, weights, values, max_weight) for c in population]
        current_best_chromosome = population[fitness_values.index(max(fitness_values))]
        current_best_fitness = max(fitness_values)

        if current_best_fitness > best_fitness:
            best_chromosome = current_best_chromosome
            best_fitness = current_best_fitness

        print(f"Generation {generation}: Best Fitness = {best_fitness}, Best Chromosome = {best_chromosome}")

        if best_fitness == sum(values):
            break

        parents = selection_function(population, fitness_values)
        offspring = crossover_function(parents, crossover_rate)
        offspring = mutation_function(offspring, mutation_rate)
        population = offspring

    return best_chromosome


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Knapsack Problem")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(padx=10, pady=10)

        self.capacity_label = ttk.Label(self.input_frame, text="Capacity:")
        self.capacity_label.grid(row=0, column=0, sticky=tk.W)
        self.capacity_entry = ttk.Entry(self.input_frame)
        self.capacity_entry.grid(row=0, column=1, sticky=tk.E)

        self.values_label = ttk.Label(self.input_frame, text="Values:")
        self.values_label.grid(row=1, column=0, sticky=tk.W)
        self.values_entry = ttk.Entry(self.input_frame)
        self.values_entry.grid(row=1, column=1, sticky=tk.E)

        self.weights_label = ttk.Label(self.input_frame, text="Weights:")
        self.weights_label.grid(row=2, column=0, sticky=tk.W)
        self.weights_entry = ttk.Entry(self.input_frame)
        self.weights_entry.grid(row=2, column=1, sticky=tk.E)

        self.items_label = ttk.Label(self.input_frame, text="Number of items:")
        self.items_label.grid(row=3, column=0, sticky=tk.W)
        self.items_entry = ttk.Entry(self.input_frame)
        self.items_entry.grid(row=3, column=1, sticky=tk.E)

        self.solve_button = ttk.Button(self, text="Solve", command=self.solve)
        self.solve_button.pack(padx=10, pady=10)

        self.output_frame = ttk.Frame(self)
        self.output_frame.pack(padx=10, pady=10)

        self.solution_label = ttk.Label(self.output_frame, text="Solution:")
        self.solution_label.grid(row=0, column=0, sticky=tk.W)
        self.solution_text = tk.Text(self.output_frame, width=40, height=10)
        self.solution_text.grid(row=0, column=1, sticky=tk.E)

    def solve(self):
        capacity = int(self.capacity_entry.get())
        values = list(map(int, self.values_entry.get().split()))
        weights = list(map(int, self.weights_entry.get().split()))
        items = int(self.items_entry.get())

        if capacity <= 0 or items <= 0 or len(values) != items or len(weights) != items or any(v <= 0 for v in values) or any(w <= 0 for w in weights):
            messagebox.showerror("Error", "Invalid input values. Please check the input.")
            return

        best_chromosome = genetic_algorithm(weights, values, capacity, population_size=50, parent_count=30, probability_of_ones=0.5, crossover_rate=0.8, mutation_rate=0.01, max_generations=100)

        self.solution_text.delete(1.0, tk.END)
        self.solution_text.insert(tk.END, f"Selected items: {best_chromosome}\n")
        self.solution_text.insert(tk.END, f"Total value: {fitness_function(best_chromosome, weights, values, capacity)}")

if __name__ == "__main__":
    app = GUI()
    app.mainloop()