import tkinter as tk

class MinimalAutoClickerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Small AutoClicker UI")
        self.root.geometry("180x60")
        self.root.resizable(False, False)

        # Default CPS value
        self.cps_var = tk.IntVar(value=10)

        # CPS Entry
        self.cps_entry = tk.Entry(root, textvariable=self.cps_var, width=5, font=("Arial", 14), justify="center")
        self.cps_entry.grid(row=0, column=0, padx=10, pady=10)

        # + Button
        self.plus_button = tk.Button(root, text="+", width=2, font=("Arial", 14), command=self.increment_cps)
        self.plus_button.grid(row=0, column=1, padx=0, pady=10)

    def increment_cps(self):
        try:
            current = int(self.cps_var.get())
        except ValueError:
            current = 0
        self.cps_var.set(current + 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MinimalAutoClickerUI(root)
    root.mainloop()
