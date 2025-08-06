import tkinter as tk
from tkinter import simpledialog
import threading
import time
from pynput import keyboard
import pyautogui

class ClickTarget:
    def __init__(self, canvas, x, y, click_rate=5):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.click_rate = click_rate  # clicks per second
        self.circle = canvas.create_oval(x-30, y-30, x+30, y+30, fill="#aaf", outline="#33f", width=2)
        self.dot = canvas.create_oval(x-5, y-5, x+5, y+5, fill="#33f")
        self.text = canvas.create_text(x, y+40, text=f"{click_rate} cps", fill="#333")
        self.drag_data = {"x": 0, "y": 0}
        self.bind_events()

    def bind_events(self):
        self.canvas.tag_bind(self.circle, "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(self.circle, "<B1-Motion>", self.drag)
        self.canvas.tag_bind(self.circle, "<ButtonRelease-1>", self.end_drag)
        self.canvas.tag_bind(self.circle, "<Double-Button-1>", self.set_rate)
        self.canvas.tag_bind(self.dot, "<Button-1>", self.set_rate)
        self.canvas.tag_bind(self.text, "<Button-1>", self.set_rate)

    def start_drag(self, event):
        self.drag_data["x"] = event.x - self.x
        self.drag_data["y"] = event.y - self.y

    def drag(self, event):
        self.x = event.x - self.drag_data["x"]
        self.y = event.y - self.drag_data["y"]
        self.update()

    def end_drag(self, event):
        pass

    def update(self):
        self.canvas.coords(self.circle, self.x-30, self.y-30, self.x+30, self.y+30)
        self.canvas.coords(self.dot, self.x-5, self.y-5, self.x+5, self.y+5)
        self.canvas.coords(self.text, self.x, self.y+40)
        self.canvas.itemconfig(self.text, text=f"{self.click_rate} cps")

    def set_rate(self, event=None):
        new_rate = simpledialog.askinteger("Set Click Rate", "Clicks per second:", initialvalue=self.click_rate, minvalue=1, maxvalue=50)
        if new_rate:
            self.click_rate = new_rate
            self.update()

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Auto Clicker")
        self.targets = []
        self.clicking = False
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        self.canvas = tk.Canvas(root, width=600, height=400, bg="#f7f7ff")
        self.canvas.pack(fill="both", expand=True)
        self.add_button = tk.Button(root, text="+", font=("Arial", 16, "bold"), command=self.add_target)
        self.add_button.pack(pady=10)
        self.status_label = tk.Label(root, text="Status: OFF (press = to toggle)", fg="red")
        self.status_label.pack()
        self.thread = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_target(self):
        x, y = 300, 200
        target = ClickTarget(self.canvas, x, y)
        self.targets.append(target)

    def on_key_press(self, key):
        try:
            if key.char == "=":
                self.toggle_clicking()
        except AttributeError:
            pass

    def toggle_clicking(self):
        self.clicking = not self.clicking
        self.status_label.config(text=f"Status: {'ON' if self.clicking else 'OFF'} (press = to toggle)",
                                 fg="green" if self.clicking else "red")
        if self.clicking:
            self.thread = threading.Thread(target=self.click_loop, daemon=True)
            self.thread.start()

    def click_loop(self):
        last_click_times = [0] * len(self.targets)
        while self.clicking:
            now = time.time()
            for idx, target in enumerate(self.targets):
                if idx >= len(last_click_times):
                    last_click_times.append(0)
                interval = 1.0 / target.click_rate if target.click_rate > 0 else 1.0
                if now - last_click_times[idx] >= interval:
                    screen_x = self.root.winfo_rootx() + self.canvas.winfo_x() + target.x
                    screen_y = self.root.winfo_rooty() + self.canvas.winfo_y() + target.y
                    pyautogui.click(x=screen_x, y=screen_y)
                    last_click_times[idx] = now
            time.sleep(0.01)

    def on_close(self):
        self.clicking = False
        self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    import sys
    import os
    try:
        import pyautogui
    except ImportError:
        print("pyautogui not installed. Please run: pip install pyautogui pynput")
        sys.exit(1)
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()autoclicker_gui.py
