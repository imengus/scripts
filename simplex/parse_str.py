import re
import numpy as np

class RowObject:
    def __init__(self, string=None):
        if string is not None:
            self.type = string[:3]
            self.s = string.split()
        self.rhs = None
        self.row = None

    def get_attr(self):
        signs = '<=->=-=='
        match = re.search(self.s[-2], signs)
        self.type = match.group(0)
        self.rhs = self.s[-1]

    def add_row(self, n_cols, n_obj_cols, n_vars, slack_idx):
        row = np.zeros(n_cols)
        row[n_obj_cols:n_vars+n_obj_cols] = np.array([int(x) for x in self.s[:-2]])
        row[n_obj_cols + n_vars + slack_idx] = 1
        row[-1] = self.rhs
        self.row = row
        pass
        
    def add_art(self, n_obj_cols, n_vars, art_idx, n_art_vars):
        self.row[n_obj_cols + n_vars + art_idx] = -1
        self.row[-n_art_vars - 1] = 1

    def create_art_row(self, row_dict, n_art_vars, n_cols):
        idx = -n_art_vars-1
        art_row = np.zeros(n_cols)
        for obj in row_dict.values():
            if obj.type == ">=":
                art_row[:idx] += obj.row[:idx]
                art_row[-1] += -obj.row[-1]
        art_row[0] = 1
        self.row = art_row

    def create_obj_row(self, n_cols, n_obj_cols, n_vars):
        row = np.zeros(n_cols)
        row[n_obj_cols:n_vars+n_obj_cols] = np.array([-int(x) for x in self.s[1:]])
        row[n_obj_cols -1] = 1
        self.row = row

def preprocess(constraints):
    new_constraints = [constraints[0]]
    n_art_vars = 0
    for i in range(1, len(constraints)):
        obj = RowObject(constraints[i])
        obj.get_attr()
        if obj.type == "==":
            n_art_vars += 1
            obj.s[-2] = "<="
            new_constraints.append(" ".join(obj.s))
            obj.s[-2] = ">="
            new_constraints.append(" ".join(obj.s))
        if obj.type == ">=":
            n_art_vars += 1
            new_constraints.append(constraints[i])
        elif obj.type != "==":
            new_constraints.append(constraints[i])
    return new_constraints, n_art_vars


def calculate_constants(constraints, n_art_vars):
    n_rows = len(constraints) - 1
    n_vars = len(constraints[1].split()) - 2
    n_obj_cols = (n_art_vars > 0) + 1
    n_cols = n_vars + n_rows + n_obj_cols + n_art_vars + 1
    return [n_cols, n_obj_cols, n_vars, n_rows, n_art_vars]


def create_row_objects(constraints, constants):
    n_cols, n_obj_cols, n_vars, n_rows, n_art_vars = constants
    art_idx = n_art_vars
    row_dict = {}
    for i in range(n_rows + 1):
        obj = RowObject(constraints[i])
        if obj.type in ("Max", "Min"):
            obj.create_obj_row(n_cols, n_obj_cols, n_vars)
        else:
            obj.get_attr()
            obj.add_row(n_cols, n_obj_cols, n_vars, i-1)
        if obj.type == ">=":
            obj.add_art(n_obj_cols, n_vars, i-1, art_idx)
            art_idx -= 1
        row_dict[obj.type + str(i)] = obj
    if n_obj_cols > 1:
        obj = RowObject()
        obj.create_art_row(row_dict, n_art_vars, n_cols)
        rows = list(row_dict.items())
        rows.insert(0, ("art_row", obj))
        row_dict = dict(rows)
    return row_dict

def create_tableau(row_dict, n_cols):
    tableau = np.zeros(n_cols)
    for obj in row_dict.values():
        tableau = np.vstack((tableau, obj.row))
    tableau = np.delete(tableau, 0, axis=0)
    vertical_sum = np.sum(tableau, axis=1)
    tableau = np.delete(tableau, np.where(vertical_sum == 0), axis=1)
    return tableau

def generate_col_titles(constants):
    strings = ["o_", "x_", "s_", "a_"]
    col_titles = []
    for i in range(4):
        for j in range(constants[i + 1]):
            col_titles.append(strings[i] + str(j + 1))
    col_titles.append("RHS")
    return col_titles
    
def input_to_tableau(INITIAL):
    constraints, n_art_vars = preprocess(INITIAL.strip().splitlines())
    constants = calculate_constants(constraints, n_art_vars)
    row_dict = create_row_objects(constraints, constants)
    tableau = create_tableau(row_dict, constants[0])
    col_titles = generate_col_titles(constants)
    return tableau, col_titles, n_art_vars