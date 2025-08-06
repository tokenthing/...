import tkinter as tk
import threading
import pyautogui
import time

class MinimalAutoClickerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker UI with Circles")
        self.root.geometry("320x260")
        self.root.resizable(False, False)

        # Canvas for circles
        self.canvas = tk.Canvas(root, width=280, height=150, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.circles = []
        self.click_pos = None  # (x, y) in screen coordinates

        # CPS Entry
        self.cps_var = tk.IntVar(value=10)
        self.cps_entry = tk.Entry(root, textvariable=self.cps_var, width=5, font=("Arial", 14), justify="center")
        self.cps_entry.grid(row=1, column=0, padx=10, pady=5)

        # + Button to add circles
        self.plus_button = tk.Button(root, text="+", width=3, font=("Arial", 14), command=self.add_circle)
        self.plus_button.grid(row=1, column=1, padx=10, pady=5)

        # Start button
        self.start_button = tk.Button(root, text="Start", width=6, font=("Arial", 14), command=self.start_clicking)
        self.start_button.grid(row=1, column=2, padx=10, pady=5)

        self.stop_flag = threading.Event()

    def add_circle(self):
        # Place new circle offset by number of circles
        idx = len(self.circles)
        x = 40 + 60 * (idx % 4)
        y = 40 + 60 * (idx // 4)
        radius = 20
        circle = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="skyblue", outline="black", width=2)
        # Bind click to record center of this circle
        self.canvas.tag_bind(circle, "<Button-1>", lambda event, cx=x, cy=y: self.on_circle_click(cx, cy))

    def on_circle_click(self, cx, cy):
        # Get canvas position in screen coordinates
        canvas_x = self.canvas.winfo_rootx()
        canvas_y = self.canvas.winfo_rooty()
        click_x = canvas_x + cx
        click_y = canvas_y + cy
        self.click_pos = (click_x, click_y)
        # Highlight the selected circle by drawing a red outline
        self.canvas.delete("highlight")
        self.canvas.create_oval(cx-22, cy-22, cx+22, cy+22, outline="red", width=3, tags="highlight")

    def start_clicking(self):
        if self.click_pos is None:
            print("No circle selected to click.")
            return

        self.stop_flag.clear()
        cps = self.cps_var.get()
        threading.Thread(target=self.autoclick, args=(self.click_pos, cps), daemon=True).start()

    def autoclick(self, pos, cps):
        delay = 1.0 / max(1, cps)
        while not self.stop_flag.is_set():
            pyautogui.click(pos[0], pos[1])
            time.sleep(delay)

    def stop_clicking(self):
        self.stop_flag.set()

if __name__ == "__main__":
    root = tk.Tk()
    app = MinimalAutoClickerUI(root)

    # Stop autoclicking when closing the window
    def on_close():
        app.stop_clicking()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()
