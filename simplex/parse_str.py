import re
import numpy as np


def find_type(row_string):
    """Find whether the constraint is a minimise or maximise objective function
    or a constraint with an (in)equality.
    """
    row_string = row_string.lower()
    match = re.search("(min|max|<=|>=|==)", row_string)
    return match.group(0)


def preprocess(constraints):
    """Replace equalities with >=, <= and count the number of artificial
    variables necessary.
    """
    new_constraints = []
    n_art_vars = 0
    for row_string in constraints:
        type = find_type(row_string)
        split_string = row_string.split()
        if type in "min-max":
            new_constraints.append(row_string)
            continue
        if type == "==":
            n_art_vars += 1
            split_string[-2] = "<="
            new_constraints.append(" ".join(split_string))
            split_string[-2] = ">="
            new_constraints.append(" ".join(split_string))
        if type == ">=":
            n_art_vars += 1
            new_constraints.append(row_string)
        elif type != "==":
            new_constraints.append(row_string)
    return new_constraints, n_art_vars


class Tab:
    """Generate and operate on simplex tableaus"""

    def __init__(self, constraints: str, n_art_vars: int):

        self.n_obj_cols = (n_art_vars > 0) + 1
        self.n_vars = len(constraints[0].split()) - 1
        self.n_rows = len(constraints)
        self.n_art_vars = n_art_vars
        self.n_cols = self.n_vars + self.n_rows + self.n_art_vars

        self.tableau = np.zeros((self.n_rows, self.n_cols))
        self.col_titles = None

        # Indices of rows that have greater than or equal to constraints
        self.geq_idxs = []

        # Slice excluding objective columns and right-hand side
        self.s = slice(0, self.n_vars)

    def add_row(self, row_string, row_idx, art_vars_left=0):
        """Add objective, slack, and artifical variables to one row of the
        simplex tableau
        """
        idx_minus = row_idx - 1
        row_type = find_type(row_string)
        row = np.zeros(self.n_cols)
        row_string = row_string.split()

        # Multiplicand of variable entries = Value of slack entry =  1
        var_sign = slack_val = 1

        # Not including inequality sign or RHS
        s = slice(0, -2)

        if row_type in "max-min":
            s = slice(1, self.n_cols)
            slack_val = 0
        else:  # If it is a constraint row add RHS
            row[-1] = row_string[-1]
        if row_type == "max":
            var_sign = -1
        elif row_type == ">=":
            self.geq_idxs.append(row_idx)
            slack_val = -1
            row[-art_vars_left - 1] = 1

            # Move position of next artificial variable one column to the right
            art_vars_left -= 1

        # Add variable entries
        row[self.s] = np.array([var_sign * int(x) for x in row_string[s]])

        # Add slack entry
        row[self.n_vars + idx_minus] = slack_val

        # Add row to tableau
        self.tableau[row_idx] = row
        return art_vars_left

    def create_art_row(self):
        """
        Sum the rows with >= inequalities to produce the new objective row
        (excluding artifical variables)
        """
        # Column index of left-most artifical column
        art_idx = self.n_cols - self.n_art_vars - 1

        # Create index array to exclude artifical variable columns in sum
        idx_arr = np.ones(self.n_cols, dtype=bool)
        idx_arr[art_idx:-1] = False

        # Sum rows whose indices belong to geq_idxs
        art_row = np.sum(self.tableau[:, idx_arr][self.geq_idxs], axis=0)

        # Insert 0s to fill the gap between non-artifical variables and RHS
        art_row = np.insert(art_row, art_idx, np.zeros(self.n_art_vars))

        self.tableau = np.vstack((art_row, self.tableau))

    def create_tableau(self, constraints):
        art_vars_left = self.n_art_vars
        for row_idx, row_string in enumerate(constraints):
            art_vars_left = self.add_row(row_string, row_idx, art_vars_left)
        if self.geq_idxs:
            self.create_art_row()

    def generate_col_titles(self):
        strings = ["x_", "s_", "a_"]
        col_titles = []
        for i in range(3):
            for j in range(self.n_cols):
                col_titles.append(strings[i] + str(j + 1))
        col_titles.append("RHS")
        self.col_titles = col_titles


def tabulate(input_str):
    constraints = input_str.strip().splitlines()
    constraints, n_art_vars = preprocess(constraints)
    t = Tab(constraints, n_art_vars)
    t.create_tableau(constraints)
    t.generate_col_titles()
    return t
