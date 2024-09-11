import tkinter as tk

# Define the knapsack_backtracking function as before
def knapsack_backtracking(values, weights, capacity, n):
    
    if capacity == 0 or n == 0:
        return 0


    if weights[n - 1] > capacity:
        return knapsack_backtracking(values, weights, capacity, n - 1)

 
    else:
        include_item = values[n - 1] + knapsack_backtracking(values, weights, capacity - weights[n - 1], n - 1)
        exclude_item = knapsack_backtracking(values, weights, capacity, n - 1)
        return max(include_item, exclude_item)


def get_input():
    
    values = list(map(int, values_entry.get().split()))
    weights = list(map(int, weights_entry.get().split()))
    capacity = int(capacity_entry.get())
    n = len(values)

    
    result = knapsack_backtracking(values, weights, capacity, n)
    result_label.config(text=f"The maximum value that can be obtained is: {result}")


#GUI


root = tk.Tk()
root.title("Knapsack Problem")


frame = tk.Frame(root)
frame.pack(padx=10, pady=10)


values_label = tk.Label(frame, text="Enter the values of the items, separated by spaces:")
values_label.grid(row=0, column=0, sticky=tk.W)
values_entry = tk.Entry(frame)
values_entry.grid(row=1, column=0, sticky=tk.W)


weights_label = tk.Label(frame, text="Enter the weights of the items, separated by spaces:")
weights_label.grid(row=2, column=0, sticky=tk.W)
weights_entry = tk.Entry(frame)
weights_entry.grid(row=3, column=0, sticky=tk.W)


capacity_label = tk.Label(frame, text="Enter the capacity of the knapsack:")
capacity_label.grid(row=4, column=0, sticky=tk.W)
capacity_entry = tk.Entry(frame)
capacity_entry.grid(row=5, column=0, sticky=tk.W)


button = tk.Button(frame, text="Calculate", command=get_input)
button.grid(row=6, column=0, sticky=tk.W)


result_label = tk.Label(frame, text="")
result_label.grid(row=7, column=0, sticky=tk.W)


root.mainloop()
