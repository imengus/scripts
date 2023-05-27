import tableau
from tabulate import tabulate
import tkinter as tk
from input_gui import Input


def main():
    master = tk.Tk()
    inp = Input(master)
    master.mainloop()
    constraints = inp.input_str.strip().splitlines()
    constraints, n_art_vars = tableau.preprocess(constraints)
    t = tableau.Tab(constraints, n_art_vars)
    t.create_tableau(constraints)
    t.generate_col_titles()
    t.delete_empty()
    t.run_simp()
    for num, state in enumerate(t.previous_states[:-1]):
        tab, col_titles = state.tableau, state.col_titles
        print(num, ":")
        print(tabulate(tab, headers=col_titles, tablefmt="grid"))


if __name__ == "__main__":
    main()
