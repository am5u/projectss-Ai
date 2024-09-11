import random
import time
import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

def individuals(color_of_nodes,num_nodes):
    for i in range(1, num_nodes + 1):
        color_of_nodes[i] = random.randint(0, len(set_of_colors) - 1)
    return color_of_nodes

def crossover(parent1, parent2):
    rindex = random.randrange(1, len(parent1))
    child1 = parent1[:rindex] + parent2[rindex:]
    child2 = parent1[rindex:] + parent2[:rindex]
    return child1, child2


def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, len(set_of_colors) - 1)


def fitness(individual, num_nodes, edges):
    num_of_error = sum(
        individual[node] == individual[int(nei)] for node in range(1, num_nodes + 1) for nei in edges[str(node)]
    )
    num_of_colors = len(set(individual[1:num_nodes + 1]))
    return num_of_error + num_of_colors


def genetics_algo(frame_dell,population_size, generations, mutation_rate, crossover_prob,retain, num_nodes, edges):
    start_time = time.perf_counter()
    color_of_nodes = [0] * (num_nodes + 2)
    population = [individuals(color_of_nodes,num_nodes) for _ in range(0, population_size)]

    for generation in range(generations):
        population.sort(key=lambda ind: fitness(ind, num_nodes, edges))
        population = population[:(int(retain * population_size))]

        for _ in range(int(population_size - (retain * population_size))):
            parent1, parent2 = random.sample(population, 2)
            if random.random() < crossover_prob:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2

            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            population.append(child1)
            population.append(child2)

        optimal_ans = min(population, key=lambda ind: fitness(ind, num_nodes, edges))
        color_of_nodes = optimal_ans
    end_time = time.perf_counter()
    time_taken = end_time - start_time

    print("Time taken:", time_taken)
    print("Number of colors:", len(set(color_of_nodes[1:num_nodes + 1])))
    draw_graph(frame_dell, num_nodes, color_of_nodes, edges)


def is_valid2(color, src, color_of_nodes, edges):
    error_no = 0
    for child in edges[str(src)]:
        if color_of_nodes[int(child)] == color:
            error_no += 1
    return error_no


def is_valid(color, src, visited, color_of_nodes, edges):
    for child in edges[str(src)]:
        if visited[int(child)] != 0 and color_of_nodes[int(child)] == color:
            return False
    return True


def dfs(src, visited, color_of_nodes, edges):
    visited[src] = 1
    for child in edges[str(src)]:
        if visited[int(child)] == 0:
            for i in range(len(set_of_colors)):
                if is_valid(i, int(child), visited, color_of_nodes, edges):
                    color_of_nodes[int(child)] = i
                    break
            dfs(int(child), visited, color_of_nodes, edges)


def solve(num_nodes, edges,frame_dell):
    visited = [0] * (num_nodes + 2)
    start_time = time.perf_counter()
    color_of_nodes = [0] * (num_nodes + 2)
    for i in range(1, num_nodes + 1):
        if visited[i] == 0:
            color_of_nodes[i] = 0
            dfs(i, visited, color_of_nodes, edges)
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print("Time taken:", time_taken)
    print("Number of colors:", len(set(color_of_nodes[1:num_nodes + 1])))
    draw_graph(frame_dell,num_nodes,color_of_nodes,edges)


def close_program():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()


def draw_graph(frame_del, num_nodes, color_of_nodes, edges):
    frame_del.pack_forget()
    frame5 = tk.Frame(root)
    frame5.pack()
    G = nx.Graph()
    for i in range(1, num_nodes + 1):
        G.add_node(str(i))
    G.add_edges_from(list1)
    fig = plt.figure()
    plot1 = fig.add_subplot(111)
    colors = []
    for i in range(1, num_nodes + 1):
        colors.append(set_of_colors[color_of_nodes[i]])
    nx.draw(G, with_labels=True, ax=plot1, node_color=colors)
    canvas = FigureCanvasTkAgg(fig, master=frame5)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    root.protocol("WM_DELETE_WINDOW",close_program)


def get_data(frame_dell,population_size, generations, mutation_rate, crossover_prob,retain_prob, num_nodes, edges):
    population_size = int(population_size.get())
    generations = int(generations.get())
    mutation_rate = float(mutation_rate.get())
    crossover_prob = float(crossover_prob.get())
    retain_prob = float(retain_prob.get())
    genetics_algo(frame_dell,population_size, generations, mutation_rate, crossover_prob,retain_prob, num_nodes, edges)


def show_next_page5(frame_dell,num_nodes,edges):
    frame_dell.pack_forget()

    frame4 = tk.Frame(root)
    frame4.pack()

    population_ch = tk.Label(frame4, text="Population size:")
    population_ch.pack()
    population_size = tk.Entry(frame4, width=10)
    population_size.pack()

    generation_ch = tk.Label(frame4, text="Number of generations:")
    generation_ch.pack()
    generations = tk.Entry(frame4, width=10)
    generations.pack()

    mutation_ch = tk.Label(frame4, text="Mutation rate:")
    mutation_ch.pack()
    mutation_rate = tk.Entry(frame4, width=10)
    mutation_rate.pack()

    crossover_ch = tk.Label(frame4, text="Crossover probability:")
    crossover_ch.pack()
    crossover_prob = tk.Entry(frame4, width=10)
    crossover_prob.pack()

    retain_ch = tk.Label(frame4, text="Retain probability:")
    retain_ch.pack()
    retain_prob = tk.Entry(frame4, width=10)
    retain_prob.pack()

    submit = tk.Button(frame4, text="OK", command=lambda: get_data(frame4,population_size, generations, mutation_rate, crossover_prob,retain_prob, num_nodes, edges))
    submit.pack()


def show_next_page4(num_nodes, edges):
    for i in range(1, num_nodes + 1):
        if str(i) in edges:
            continue
        edges[str(i)] = []
    frame3 = tk.Frame(root)
    frame3.pack()
    choice = tk.Label(frame3, text="Choose which algorithm to use")
    choice.pack(pady=10)
    ch_back = tk.Button(frame3, text="Backtracking Search Algorithm", command=lambda: solve(num_nodes, edges,frame3))
    ch_back.pack(pady=10)
    ch_gen = tk.Button(frame3, text="Genetics Algorithm", command=lambda: show_next_page5(frame3,num_nodes,edges))
    ch_gen.pack(pady=10)

def takeData(node1,node2,num_nodes,edges,frame_dell,flag):
    str1 = str(node1.get())
    str2 = str(node2.get())
    if str1 != "":
        list1.append((str1, str2))
        if str1 in edges:
            edges[str1].append(str2)
        else:
            edges[str1] = [str2]
        if str2 in edges:
            edges[str2].append(str1)
        else:
            edges[str2] = [str1]
    frame_dell.pack_forget()
    if flag:
        show_next_page4(num_nodes,edges)
    else:
        show_next_page(edges,frame_dell)

def show_next_page(edges,frame_dell):
    num_nodes = int(nodes_entry.get())
    frame_dell.pack_forget()
    frame2 = tk.Frame(root)
    frame2.pack()

    label5 = tk.Label(frame2, text="Node 1:")
    label5.pack(pady=10)

    node1 = tk.Entry(frame2, width=10)
    node1.pack()

    label6 = tk.Label(frame2, text="Node 2:")
    label6.pack(pady=10)

    node2 = tk.Entry(frame2, width=10)
    node2.pack()
    frame_dell=frame2
    button2 = tk.Button(frame2, text="OK", command=lambda: takeData(node1,node2,num_nodes,edges,frame_dell,0))
    button2.pack(pady=10)

    button2 = tk.Button(frame2, text="Finish", command=lambda: takeData(node1,node2,num_nodes, edges,frame2,1))
    button2.pack(pady=30)


def create_gui():
    global nodes_entry
    frame1 = tk.Frame(root)
    frame1.pack()

    label1 = tk.Label(frame1, text="Number of nodes:")
    label1.pack(pady=10)

    nodes_entry = tk.Entry(frame1)
    nodes_entry.pack(pady=20)

    button = tk.Button(frame1, text="OK", command=lambda: show_next_page(edges,frame1))
    button.pack()


if __name__ == "__main__":
    edges = {}
    list1 = []
    set_of_colors = ["red", "yellow", "green", "blue", "purple"]
    root = tk.Tk()

    window_width = 600  # Width of the window
    window_height = 500  # Height of the window

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    create_gui()
    root.mainloop()
