import tkinter as tk
from tkinter import ttk

class SubscriptionsZoomedWindow(tk.Toplevel):
    def __init__(self, master=None, subscription_data=None):
        super().__init__(master)
        self.title("Subscription Information")
        self.geometry("500x500")
        self.configure(padx=20, pady=20)

        options_frame = ttk.LabelFrame(self, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=(0, 10))

        save_button = ttk.Button(options_frame, text="Save", command=self.on_save)
        close_button = ttk.Button(options_frame, text="Close", command=self.destroy)
        save_button.pack(side="left", padx=5)
        close_button.pack(side="left", padx=5)

        form_frame = ttk.LabelFrame(self, text="Subscription Details", padding=10)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fields = ["Product Name", "Family", "Purchase Date", "Expiration Date", "Quantity"]
        self.entries = {}

        for i, field in enumerate(fields):
            label = ttk.Label(form_frame, text=field + ":")
            entry = ttk.Entry(form_frame, width=40)
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            self.entries[field] = entry

        if subscription_data:
            for key, value in zip(fields, subscription_data):
                self.entries[key].insert(0, str(value))

    def on_save(self):
        values = {field: entry.get() for field, entry in self.entries.items()}
        print("Saved values:", values)
        self.destroy()

# Run test
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    SubscriptionsZoomedWindow(root)
    root.mainloop()
