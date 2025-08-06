import tkinter as tk
import itertools
import threading
import time
import random

root = tk.Tk()
root.title("Fake Hack Terminal")
root.attributes("-fullscreen", True)  # Make fullscreen
root.configure(bg="black")

canvas = tk.Canvas(root, width=100, height=100, bg="black", highlightthickness=0)
canvas.pack(side=tk.TOP, pady=20)

angles = itertools.cycle(range(0, 360, 10))

def rotate():
    canvas.delete("all")
    canvas.create_rectangle(30, 30, 70, 70, fill='lime')
    root.after(100, rotate)

rotate()

text = tk.Text(root, bg="black", fg="lime", insertbackground="lime", font=("Courier", 14))
text.pack(fill=tk.BOTH, expand=True)

# Fake list of filenames to simulate scanning
fake_files = [
    "secret_plans.docx",
    "passwords.txt",
    "bank_info.csv",
    "private_keys.pem",
    "project_alpha.zip",
    "notes.md",
    "todo.txt",
    "confidential.pdf"
]

fake_data = [
    "Initializing system scan...",
    "Reading file structure...",
]

# Add fake files to output
for f in fake_files:
    fake_data.append(f"Found file: {f}")

fake_data += [
    "Uploading files to Tokendarkweb...",
    "Upload complete.",
    "Process finished successfully."
]

def fake_typing():
    for line in fake_data:
        for char in line:
            text.insert(tk.END, char)
            text.see(tk.END)
            root.update()
            time.sleep(0.03 + random.random() * 0.03)
        text.insert(tk.END, "\n")
        text.see(tk.END)
        time.sleep(0.5)

threading.Thread(target=fake_typing, daemon=True).start()

root.mainloop()
