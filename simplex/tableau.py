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
        row_type = find_type(row_string)
        split_string = row_string.split()
        if row_type in "min-max":
            new_constraints.append(row_string)
            continue
        if row_type == "==":
            n_art_vars += 1
            split_string[-2] = "<="
            new_constraints.append(" ".join(split_string))
            split_string[-2] = ">="
            new_constraints.append(" ".join(split_string))
        if row_type == ">=":
            n_art_vars += 1
            new_constraints.append(row_string)
        elif row_type != "==":
            new_constraints.append(row_string)
    return new_constraints, n_art_vars


class Tab:
    """Generate and operate on simplex tableaus"""

    def __init__(
        self, constraints=None, n_art_vars=None, tableau=None, col_titles=None
    ):
        self.col_titles = col_titles
        self.tableau = tableau
        if constraints is not None:
            self.n_stages = (n_art_vars > 0) + 1
            self.n_vars = len(constraints[0].split()) - 1
            self.n_rows = len(constraints) + (n_art_vars > 0)
            self.n_slack = len(constraints) - 1
            self.n_art_vars = n_art_vars  # Number of artificial variables
            self.n_cols = self.n_vars + self.n_rows + self.n_art_vars + 1

            self.tableau = np.zeros((self.n_rows - 1, self.n_cols))

        # Previous states
        self.previous_states = []

        # Objectives for each state
        self.objectives = []

        # Indices of rows that have greater than or equal to constraints
        self.geq_ids = []

        # Index of pivot row and column
        self.row_idx = None
        self.col_idx = None

        # Does objective row only contain (non)-negative values?
        self.stop_iter = False

    def add_row(self, row_string, row_num, art_vars_left=0):
        """Add objective, slack, and artificial variables to one row of the
        simplex tableau
        """
        row_type = find_type(row_string)
        row = np.zeros(self.n_cols)
        row_string = row_string.split()

        # Multiplicand of variable entries = Value of slack entry =  1
        coeff = slack_val = 1

        # Not including inequality sign or RHS
        s = slice(0, -2)

        if row_type in "max-min":
            s = slice(1, self.n_cols)
            slack_val = 0
            self.objectives.append(row_type)
        else:  # If it is a constraint row add RHS
            row[-1] = row_string[-1]
        if row_type == "max":
            coeff = -1
        elif row_type == ">=":
            self.geq_ids.append(row_num)
            slack_val = -1
            row[-art_vars_left - 1] = 1

            # Move position of next artificial variable one column to the right
            art_vars_left -= 1

        # Add variable entries
        row[: self.n_vars] = np.array([coeff * int(x) for x in row_string[s]])

        # Add slack entry
        row[self.n_vars + row_num] = slack_val

        # Add row to tableau
        self.tableau[row_num] = row
        return art_vars_left

    def create_art_row(self):
        """
        Sum the rows with >= inequalities to produce the new objective row
        (excluding artificial variables)
        """
        # Column index of left-most artificial column
        art_idx = self.n_cols - self.n_art_vars - 1

        # Create index array to exclude artificial variable columns in sum
        idx_arr = np.ones(self.n_cols, dtype=bool)
        idx_arr[art_idx:-1] = False

        # Sum rows whose indices belong to geq_ids
        art_row = np.sum(self.tableau[:, idx_arr][self.geq_ids], axis=0)

        # Insert 0s to fill the gap between non-artificial variables and RHS
        art_row = np.insert(art_row, art_idx, np.zeros(self.n_art_vars))

        self.tableau = np.vstack((art_row, self.tableau))
        self.objectives.append("min")

    def create_tableau(self, constraints):
        art_vars_left = self.n_art_vars
        for row_idx, row_string in enumerate(constraints):
            art_vars_left = self.add_row(row_string, row_idx, art_vars_left)

        # If there are any >= constraints, an additional objective is needed
        if self.geq_ids:
            self.create_art_row()

    def delete_empty(self):
        # Delete empty columns
        del_ids = ~np.any(self.tableau, axis=0)
        self.tableau = np.delete(self.tableau, del_ids, axis=1)

    def generate_col_titles(self):
        string_starts = ["x_", "s_", "a_"]
        constants = self.n_vars, self.n_slack, self.n_art_vars
        col_titles = []
        for i in range(3):
            for j in range(constants[i]):
                col_titles.append(string_starts[i] + str(j + 1))
        col_titles.append("RHS")
        self.col_titles = col_titles

    def find_pivot(self):
        tableau = self.tableau
        objective = self.objectives[-1]

        # Find entries of highest magnitude in objective rows
        sign = (objective == "min") - (objective == "max")
        self.col_idx = np.argmax(sign * tableau[0, :-1])

        # Check if choice is valid, or if iteration must be stopped
        if sign * self.tableau[0, self.col_idx] <= 0:
            self.stop_iter = True
            return

        # Pivot row is chosen as having the lowest quotient when elements of
        # the pivot column divide the right-hand side
        s = slice(self.n_stages, self.n_rows)
        quotients = tableau[s, -1] / tableau[s, self.col_idx]
        quotients[quotients <= 0] = float("inf")
        self.row_idx = np.argmin(quotients) + self.n_stages
        pass

    def pivot(self):
        piv_row = self.tableau[self.row_idx].copy()
        piv_val = piv_row[self.col_idx]
        piv_row *= 1 / piv_val

        # Variable in pivot column becomes basic, ie the only non-zero entry
        for idx, coeff in enumerate(self.tableau[:, self.col_idx]):
            self.tableau[idx] += -coeff * piv_row
        self.tableau[self.row_idx] = piv_row

    def change_stage(self):
        # Objective of original objective row remains
        self.objectives.pop()

        if not self.objectives:
            return

        s = slice(-self.n_art_vars - 1, -1)

        # Delete the artificial variable columns
        self.tableau = np.delete(self.tableau, s, axis=1)

        # Delete the objective row of the first stage
        self.tableau = np.delete(self.tableau, 0, axis=0)

        self.n_stages = 1
        self.n_rows -= 1
        self.n_art_vars = 0

    def run_simp(self):
        # Record current state
        self.generate_col_titles()
        self.previous_states.append(
            Tab(tableau=self.tableau.copy(), col_titles=self.col_titles.copy())
        )

        # If optimal solution reached
        if not self.objectives:
            return

        self.find_pivot()
        if self.stop_iter:
            self.change_stage()
            self.run_simp()
        self.pivot()
        self.run_simp()
