import tkinter as tk
from tableau import Tableau

LABEL = """Overwrite the example to input your linear program

Note: '+2 +1 == 10' for '2*x + y = 10'
"""
EXAMPLE = r"""Max: +2 +3 +1
+1 +1 +1 <= 40
+2 +1 -1 >= 10
+0 -1 +1 >= 10
"""

class Simplex(tk.Tk):
    def __init__(self):
        super().__init__()
        self.output = None

        self.in_label = tk.Label(self, text=LABEL, font=("Courier", 18))
        self.in_label.pack(padx=20, pady=20, fill="both")

        self.text = tk.Text(self, font=("Courier", 18), height=6)
        self.text.pack()
        self.text.insert("1.0", EXAMPLE)

        self.input_str = None

        self.button_commit = tk.Button(
            self,
            height=1,
            width=10,
            text="Commit",
            command=lambda: self.simplex()
        )
        self.button_commit.pack()

        self.bind("<Return>", self.simplex)

    def simplex(self):
        self.input_str = self.text.get("1.0", "end-1c")
        constraints = self.input_str.strip().splitlines()
        constraints, n_art_vars = Tableau.preprocess(constraints)
        t = Tableau(constraints, n_art_vars)
        t.create_tableau(constraints)
        t.generate_col_titles()
        t.delete_empty()
        try:
            t.run_simp()
        except Exception:
            self.out_text = self.make_str(t.output_dict)
            self.out_label = tk.Label(self, text=self.out_text, font=("Courier", 18))
            self.out_label.pack(padx=20, pady=20, fill="both")

    @staticmethod
    def make_str(d):
        string = "Output:"
        for i, j in d.items():
            string +=  f"\n {i} = " + str(j)
        return string


if __name__ == "__main__":
    simp = Simplex()
    simp.mainloop()