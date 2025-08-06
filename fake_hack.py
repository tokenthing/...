import tkinter as tk
import itertools
import threading
import time

root = tk.Tk()
root.title("Fake Hack Terminal")
root.geometry("600x400")
root.configure(bg="black")

canvas = tk.Canvas(root, width=100, height=100, bg="black", highlightthickness=0)
canvas.pack(side=tk.TOP, pady=10)

square = canvas.create_rectangle(30,30,70,70,fill='lime')

angles = itertools.cycle(range(0,360,10))

def rotate():
    a = next(angles)
    canvas.delete("all")
    canvas.create_rectangle(30,30,70,70,fill='lime')
    canvas.after(100, rotate)

rotate()

text = tk.Text(root, bg="black", fg="lime", insertbackground="lime", font=("Courier", 12))
text.pack(fill=tk.BOTH, expand=True)

fake_data = [
    "Scanning system...",
    "Reading C:\\Users\\User\\Documents...",
    "Accessing secret files...",
    "Bypassing firewall...",
    "Extracting passwords...",
    "Uploading to darknet...",
    "Process completed successfully.",
]

def fake_typing():
    for line in fake_data:
        for char in line:
            text.insert(tk.END, char)
            text.see(tk.END)
            root.update()
            time.sleep(0.05)
        text.insert(tk.END, "\n")
        text.see(tk.END)
        time.sleep(0.5)

threading.Thread(target=fake_typing, daemon=True).start()
root.mainloop()
