#!/usr/bin/python3

import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import pulp
 
class ProjjApp:
    
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        toplevel1.resizable(False, False)
        frame1 = ttk.Frame(toplevel1)
        frame1.configure(height=200, padding=20, width=200)
        label1 = ttk.Label(frame1)
        label1.configure(
            font="{@Microsoft JhengHei UI} 16 {}",
            padding=10,
            state="normal",
            text='Nurse Scheduling')
        label1.pack(side="top")
        frame2 = ttk.Frame(frame1)
        frame2.configure(height=200, padding=20, width=200)
        label2 = ttk.Label(frame2)
        label2.configure(
            font="{Microsoft} 10 {}",
            padding=10,
            text='The minimum number of nurses required each day')
        label2.pack(side="top")
        self.min_ = ttk.Entry(frame2)
        self.min_n = tk.IntVar()
        self.min_.configure(textvariable=self.min_n)
        self.min_.pack(side="top")
        label3 = ttk.Label(frame2)
        label3.configure(
            font="{Microsoft} 10 {}",
            padding=10,
            text='The maximum number of nurses required each day')
        label3.pack(side="top")
        self.max_ = ttk.Entry(frame2)
        self.max_n = tk.IntVar()
        self.max_.configure(textvariable=self.max_n)
        self.max_.pack(side="top")
        label4 = ttk.Label(frame2)
        label4.configure(
            font="{Microsoft} 10 {}",
            padding=10,
            text='Enter the population size')
        label4.pack(side="top")
        self.pop = ttk.Entry(frame2)
        self.popSize = tk.IntVar()
        self.pop.configure(textvariable=self.popSize)
        self.pop.pack(side="top")
        label5 = ttk.Label(frame2)
        label5.configure(
            font="{Microsoft} 10 {}",
            padding=10,
            text='Enter number of iterations')
        label5.pack(side="top")
        self.itrs = ttk.Entry(frame2)
        self.its = tk.IntVar()
        self.itrs.configure(textvariable=self.its)
        self.itrs.pack(side="top")
        frame3 = ttk.Frame(frame2)
        frame3.configure(height=200, padding=20, width=200)
        button1 = ttk.Button(frame3)
        button1.configure(text='print nurses schedule')
        button1.pack(padx=10, pady=10, side="left")
        button1.configure(command=self.printSchedule)
        button2 = ttk.Button(frame3)
        button2.configure(text='Calculate number of nurses')
        button2.pack(padx=10, pady=10, side="right")
        button2.configure(command=self.calculate)
        frame3.pack(side="top")
        frame2.pack(side="top")
        frame1.pack(side="top")

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()
    
    def printSchedule(self):
            fobj = lambda x: sum(x)
            bounds=[(self.min_n.get(),self.max_n.get())]*7
            mut=0.8
            crossp=0.7
            popsize=self.popSize.get()
            its=self.its.get()
            self.nurses_num_day=[]
            week=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'] 
            def de():
                n=[]
                dimensions = len(bounds)
                pop = np.random.rand(popsize, dimensions)
                min_b, max_b = np.asarray(bounds).T
                diff = np.fabs(min_b - max_b)
                pop_denorm = min_b + pop * diff
                fitness = np.asarray([fobj(ind) for ind in pop_denorm])
                best_idx = np.argmin(fitness)
                best = pop_denorm[best_idx]
                for i in range(its):
                    for j in range(popsize):
                        idxs = [idx for idx in range(popsize) if idx != j]
                        a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
                        mutant = np.clip(a + mut * (b - c), 0, 1)
                        cross_points = np.random.rand(dimensions) < crossp
                        if not np.any(cross_points):
                            cross_points[np.random.randint(0, dimensions)] = True
                        trial = np.where(cross_points, mutant, pop[j])
                        trial_denorm = min_b + trial * diff
                        f = fobj(trial_denorm)
                        if f < fitness[j]:
                            fitness[j] = f
                            pop[j] = trial
                            if f < fitness[best_idx]:
                                best_idx = j
                                best = trial_denorm
                    n=[int(i) for i in best]    
                    return n 
            self.nurses_num_day=de()
            print("--------------------------------")
            print("DAYS        	    NUM_OF_NURSES")
            print("--------------------------------")
            for i in range(7):
                print(f"{week[i]}   \t \t    {self.nurses_num_day[i]}")
                
            print("--------------------------------")
    
    def calculate(self):
        prob = pulp.LpProblem("Nurse Schedule", pulp.LpMinimize)
        # Variables to represent the number of nurses working each shift
        x1=pulp.LpVariable("x1",0,None,pulp.LpInteger)
        x2=pulp.LpVariable("x2",0,None,pulp.LpInteger)
        x3=pulp.LpVariable("x3",0,None,pulp.LpInteger)
        x4=pulp.LpVariable("x4",0,None,pulp.LpInteger)
        x5=pulp.LpVariable("x5",0,None,pulp.LpInteger)
        x6=pulp.LpVariable("x6",0,None,pulp.LpInteger)
        x7=pulp.LpVariable("x7",0,None,pulp.LpInteger)
        
        # The objective function is added to 'prob' first
        prob += x1 + x2 + x3 + x4 + x5 + x6 + x7

        # The 7 constraints to ensure that nurses can work 3 consecutive days and 4 days off
        prob += x1 + x6 + x7 >=self.nurses_num_day[0]
        prob += x1 + x2 + x7 >=self.nurses_num_day[1]
        prob += x1 + x2 + x3 >=self.nurses_num_day[2]
        prob += x2 + x3 + x4 >=self.nurses_num_day[3]
        prob += x3 + x4 + x5 >=self.nurses_num_day[4]
        prob += x4 + x5 + x6 >=self.nurses_num_day[5]
        prob += x5 + x6 + x7 >=self.nurses_num_day[6]

        prob.solve()

     
        print("Total number of nurses = ", pulp.value(prob.objective))

if __name__ == "__main__":
    app = ProjjApp()
    app.run()
