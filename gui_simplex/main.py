
import input_gui
from tableau import Tableau


def main():
    inp = input_gui.Input()
    inp.mainloop()
    input_str = inp.input_str

    constraints = input_str.strip().splitlines()
    constraints, n_art_vars = Tableau.preprocess(constraints)
    t = Tableau(constraints, n_art_vars)
    t.create_tableau(constraints)
    t.generate_col_titles()
    t.delete_empty()
    try:
        t.run_simp()
    except Exception:
        # If optimal solution is reached
        out = input_gui.Output(t.output_dict)
        out.mainloop()





if __name__ == "__main__":
    main()
