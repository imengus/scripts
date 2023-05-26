import numpy as np
import parse_str
# import input_gui

# input_str = input_gui.initial
input_str = r"""Max: +2 +3 +1
+1 +1 +1 <= 40
+2 +1 -1 >= 10
+0 -1 +1 >= 10
"""

tableau, col_titles, n_art_cols, min_max = parse_str.tableau(input_str)
n_stages = 1 + n_art_cols > 0

class Tab:
    def __init__(self, tableau, col_titles, n_art_cols, min_max, n_stages):
        self.tableau = tableau
        self.min_max = min_max
        self.stages_left = n_stages
        self.n_art_cols = n_art_cols
        self.col_titles = col_titles
        self.row_idx = None
        self.col_idx = None
        self.order = 0
        self.previous = []

    def pivot(self):
        piv_row = tableau[self.row_idx].copy()
        pivot_coeff = piv_row[col_idx]
        piv_row *= (1 / pivot_coeff)
        for idx, coeff in enumerate(tableau[:, col_idx]):
            tableau[idx] += -coeff * piv_row
        tableau[row_idx] = piv_row
        self.tableau = tableau


    def find_pivot(self):
        if sum(min_max * tableau[n_stages:-1]) < 0:
            return 0, 0, 0
        if min_max == -1:
            col_idx = np.argmin(tableau[n_stages:-1]) + n_stages
        elif min_max == 1:
            col_idx = np.argmax(tableau[n_stages:-1]) + n_stages
        quotients = tableau[:, -1] / tableau[:, col_idx]
        quotients[quotients < 0] = float("inf")
        row_idx = np.argmin(quotients)
        return row_idx, col_idx, n_stages


def change_stage(tableau, n_art_cols):
    tableau = np.delete(tableau, (0, slice(-n_art_cols, -1)), axis=0)
    tableau = np.delete(tableau, 0, axis=1)
    return tableau
    

def run_simp(tableau, tab_list, n_stages, n_art_cols, min_max):
    if n_stages <= 0:
        return tab_list
    row_idx, col_idx, obj_row = find_pivot(tableau, n_stages, min_max)
    if not obj_row:
        n_stages -= 1
        tableau = change_stage(tableau, n_art_cols)
        run_simp(tableau, tab_list, n_stages, n_art_cols, min_max)
    tableau = pivot(tableau, row_idx, col_idx)
    tab_list.append(tableau)
    run_simp(tableau, tab_list, n_stages, n_art_cols, min_max)

    
if __name__ == "__main__":
    pivot(tableau, 3, 2)
