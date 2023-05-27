import tkinter as tk

LABEL = """Overwrite the example to input your linear program

Note: '+2 +1 == 10' for '2*x + y = 10'
"""
EXAMPLE = r"""Max: +2 +3 +1
+1 +1 +1 <= 40
+2 +1 -1 >= 10
+0 -1 +1 >= 10
"""


class SetUp:
    def __init__(self, root):
        self.root = root
        root.title("Simplex GUI")


class Input(SetUp):
    def __init__(self, root):
        super().__init__(root)
        self.label = tk.Label(root, text=LABEL, font=("Courier", 18))
        self.label.pack(padx=20, pady=20, fill="both")

        self.text = tk.Text(root, font=("Courier", 18), height=4)
        self.text.pack()
        self.text.insert("1.0", EXAMPLE)

        self.input_str = None

        self.button_commit = tk.Button(
            root,
            height=1,
            width=10,
            text="Commit",
            command=lambda: [self.retrieve_input(), root.quit()])
        self.button_commit.pack()

    def retrieve_input(self):
        self.input_str = self.text.get("1.0", "end-1c")
