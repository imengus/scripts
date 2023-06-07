import tkinter as tk

LABEL = """Overwrite the example to input your linear program

Note: '+2 +1 == 10' for '2*x + y = 10'
"""
EXAMPLE = r"""Max: +2 +3 +1
+1 +1 +1 <= 40
+2 +1 -1 >= 10
+0 -1 +1 == 10
"""

class Input(tk.Tk):
    def __init__(self):
        super().__init__()
        self.label = tk.Label(self, text=LABEL, font=("Courier", 18))
        self.label.pack(padx=20, pady=20, fill="both")

        self.text = tk.Text(self, font=("Courier", 18), height=4)
        self.text.pack()
        self.text.insert("1.0", EXAMPLE)

        self.input_str = None

        self.button_commit = tk.Button(
            self,
            height=1,
            width=10,
            text="Commit",
            command=lambda: [self.retrieve_input(), self.destroy()],
        )
        self.button_commit.pack()

    def retrieve_input(self):
        self.input_str = self.text.get("1.0", "end-1c")


class Output(tk.Tk):
    def __init__(self, d):
        super().__init__()
        self.label_text = self.make_str(d)
        self.label = tk.Label(self, text=self.label_text, font=("Courier", 18))
        self.label.pack(padx=20, pady=20, fill="both")

    @staticmethod
    def make_str(d):
        string = "Output:"
        for i, j in d.items():
            string +=  f"\n {i} = " + str(j)
        return string
