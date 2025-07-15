import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import uuid


class SubscriptionsZoomedWindow(tk.Toplevel):
    def __init__(self, master=None, customer_data=None):
        super().__init__(master)
        self.title("Subscription Information")
        self.geometry("500,500")
        self.configure(padx=20, pady=20)

        self.entries = {}
        self.customer_id = customer_data[0]

        options_frame = ttk.LabelFrame(self, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=(0, 10))

        save_button = ttk.Button(options_frame, text="Save", command=self.on_save)
        close_button = ttk.Button(options_frame, text="Close", command=self.destroy)

        save_button.pack(side="left", padx=5)
        close_button.pack(side="left", padx=5)