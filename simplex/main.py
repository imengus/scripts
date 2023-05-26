import tableau
import input_gui


def main():
    input_str = input_gui.initial
    constraints = input_str.strip().splitlines()
    constraints, n_art_vars = tableau.preprocess(constraints)
    t = tableau.Tab(constraints, n_art_vars)
    t.create_tableau(constraints)
    t.generate_col_titles()
    t.delete_empty()
    t.run_simp()
    for num, stage in enumerate(t.previous):
        print(num, ":")
        print(stage)
        print("----")


if __name__ == "__main__":
    main()
