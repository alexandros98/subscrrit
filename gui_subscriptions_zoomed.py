import tkinter as tk
from tkinter import ttk, messagebox

class SubscriptionsZoomedWindow(tk.Toplevel):
    def __init__(self, master=None, subscription_data=None):
        super().__init__(master)
        self.title("Edit Subscription")
        self.geometry("600x400")
        self.configure(padx=20, pady=20)

        self.subscription_data = subscription_data

        # Example fields based on columns: ("Name", "Family", "Purchase Date", "Expiration Date", "Quantity")
        labels = ["Name", "Family", "Purchase Date", "Expiration Date", "Quantity"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ttk.Label(self, text=label_text + ":")
            entry = ttk.Entry(self, width=40)
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            self.entries[label_text] = entry

        # Prefill fields if data is passed
        if subscription_data:
            for i, value in enumerate(subscription_data):
                label = labels[i]
                self.entries[label].insert(0, str(value))

        btn_save = ttk.Button(self, text="Save", command=self.on_save)
        btn_save.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def on_save(self):
        # Here you can implement saving logic to the DB
        # For now, just show info and close
        messagebox.showinfo("Save", "Subscription saved (not implemented)")
        self.destroy()
