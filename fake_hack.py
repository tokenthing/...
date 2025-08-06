import os
import time
import platform
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Create full screen green-on-black fake terminal UI
root = tk.Tk()
root.title("Terminal")
root.configure(bg='black')
root.attributes('-fullscreen', True)

text_area = ScrolledText(root, bg='black', fg='green', insertbackground='green', font=('Courier', 12))
text_area.pack(expand=True, fill='both')

def fake_print(text, delay=):
    for char in text:
        text_area.insert(tk.END, char)
        text_area.see(tk.END)
        root.update()
        time.sleep(delay)
    text_area.insert(tk.END, '\n')
    root.update()

# Begin fake hacking
fake_print("Scanning system files...")
time.sleep()

# Collect filenames (just simulate reading)
home_dir = os.path.expanduser("~")
for dirpath, dirnames, filenames in os.walk(home_dir):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        fake_print(f"[+] Found: {filepath}")
        time.sleep()

fake_print("\nUploading to tokendarkwet...")
time.sleep()

# Simulate upload animation
for i in range(1, 101):
    fake_print(f"Upload progress: {i}%", delay=0.005)
    time.sleep()

fake_print("\nSuccess. Data breach complete.")
fake_print("Press ESC to exit.")

# Exit on ESC
def exit_program(event):
    root.destroy()

root.bind("<Escape>", exit_program)
root.mainloop()
