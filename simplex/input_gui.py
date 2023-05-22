import tkinter as tk

LABEL = """Overwrite the example to input your maximisation problem

Note: '+2 +1 == 10' for '2*x + y = 10'
"""
EXAMPLE = r"""Max: +2 +3 +1
+1 +1 +1 <= 40
+2 +1 -1 >= 10
+0 -1 +1 >= 10
"""

root = tk.Tk()
root.geometry("1000x500")
root.title("Simplex GUI")


def retrieve_input():
    global initial
    initial = text.get("1.0", "end-1c")


label = tk.Label(root, text=LABEL, font=("Courier", 18), anchor="n")
label.pack(padx=20, pady=20, fill="both")


text = tk.Text(root, font=("Courier", 18), height=4)
text.pack()
text.insert("1.0", EXAMPLE)

buttonCommit = tk.Button(
    root,
    height=1,
    width=10,
    text="Commit",
    command=lambda: [retrieve_input(), root.quit()],
)
buttonCommit.pack()


root.mainloop()
