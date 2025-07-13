import tkinter as tk
from tkinter import ttk

class CustomerZoomedWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Test Window")
        self.geometry("400x300")
        ttk.Label(self, text="Hello World").pack(pady=20)
        ttk.Entry(self).pack(pady=10)
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # hide main window
    win = CustomerZoomedWindow()
    root.mainloop()