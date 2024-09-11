import tkinter as tk

class UnboundedKnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unbounded Knapsack Solver")

        self.label1 = tk.Label(root, text="Capacity:")
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        self.capacity_entry = tk.Entry(root)
        self.capacity_entry.grid(row=0, column=1, padx=10, pady=10)

        self.label2 = tk.Label(root, text="Weights (comma-separated):")
        self.label2.grid(row=1, column=0, padx=10, pady=10)

        self.weights_entry = tk.Entry(root)
        self.weights_entry.grid(row=1, column=1, padx=10, pady=10)

        self.label3 = tk.Label(root, text="Values (comma-separated):")
        self.label3.grid(row=2, column=0, padx=10, pady=10)

        self.values_entry = tk.Entry(root)
        self.values_entry.grid(row=2, column=1, padx=10, pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.solve_button = tk.Button(root, text="Solve", command=self.solve_knapsack)
        self.solve_button.grid(row=4, column=0, columnspan=2, pady=10)

    def solve_knapsack(self):
        try:
            capacity = int(self.capacity_entry.get())
            weights = [int(w) for w in self.weights_entry.get().split(',')]
            values = [int(v) for v in self.values_entry.get().split(',')]

            n = len(weights)
            result = self.knap_sack(capacity, weights, values, n)

            self.result_label.config(text=f"Maximum value: {result}")
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter valid integers.")

    def knap_sack(self, C, weight, value, n):
        if n == 0 or C == 0:
            return 0

        if weight[n - 1] > C:
            return self.knap_sack(C, weight, value, n - 1)
        else:
            return max(value[n - 1] + self.knap_sack(C - weight[n - 1], weight, value, n),
                       self.knap_sack(C, weight, value, n-1))


if __name__ == "__main__":
    root = tk.Tk()
    app = UnboundedKnapsackGUI(root)
    root.mainloop()
