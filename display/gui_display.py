import tkinter as tk

class VerseDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bible Verse Display")
        self.label = tk.Label(self.root, text="", font=("Arial", 36), wraplength=1200)
        self.label.pack(expand=True, fill="both")

    def update_verse(self, text):
        self.label.config(text=text)
        self.root.update_idletasks()

    def start(self):
        self.root.mainloop()
