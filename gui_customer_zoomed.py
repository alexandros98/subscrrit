import tkinter as tk
from tkinter import ttk

class CustomerZoomedWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Customer Information")
        self.geometry("1000x800")
        self.configure(padx=20, pady=20)

        # === Container: Options ===
        options_frame = ttk.LabelFrame(self, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=(0, 10))

        def on_save():
            print("Save button clicked!")
            # Add save logic here

        save_button = ttk.Button(options_frame, text="Save", command=on_save)
        save_button.pack(side="left", padx=5)

        close_button = ttk.Button(options_frame, text="Close", command=self.destroy)
        close_button.pack(side="left", padx=5)

        # === Container: Basic Info ===
        basic_info_frame = ttk.LabelFrame(self, text="Basic Info", padding=10)
        basic_info_frame.pack(fill="x", padx=10, pady=10)

        # --- Sub-container: General Info ---
        general_info_frame = ttk.Frame(basic_info_frame)
        general_info_frame.pack(fill="x", pady=(0, 10))

        general_fields = [
            "Name", "VAT Nr", "Profession", "Address",
            "City", "Postal Code", "Country"
        ]
        self.entries = {}

        for i, field in enumerate(general_fields):
            label = ttk.Label(general_info_frame, text=field + ":")
            label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = ttk.Entry(general_info_frame, width=60)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=2)
            self.entries[field] = entry

        # --- Sub-containers frame for Phones and Emails side-by-side ---
        contact_frame = ttk.Frame(basic_info_frame)
        contact_frame.pack(fill="x", pady=10)

        # --- Phones frame ---
        phones_frame = ttk.LabelFrame(contact_frame, text="Phones", padding=10)
        phones_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        for i in range(3):
            label_type = ttk.Label(phones_frame, text=f"Phone Type {i+1}:")
            entry_type = ttk.Entry(phones_frame, width=25)
            label_phone = ttk.Label(phones_frame, text=f"Phone {i+1}:")
            entry_phone = ttk.Entry(phones_frame, width=30)

            label_type.grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry_type.grid(row=i, column=1, sticky="w", padx=5, pady=2)
            label_phone.grid(row=i, column=2, sticky="e", padx=5, pady=2)
            entry_phone.grid(row=i, column=3, sticky="w", padx=5, pady=2)

            self.entries[f"Phone Type {i+1}"] = entry_type
            self.entries[f"Phone {i+1}"] = entry_phone

        # --- Emails frame ---
        emails_frame = ttk.LabelFrame(contact_frame, text="Emails", padding=10)
        emails_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))

        for i in range(3):
            label_type = ttk.Label(emails_frame, text=f"Email Type {i+1}:")
            entry_type = ttk.Entry(emails_frame, width=25)
            label_email = ttk.Label(emails_frame, text=f"Email {i+1}:")
            entry_email = ttk.Entry(emails_frame, width=30)

            label_type.grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry_type.grid(row=i, column=1, sticky="w", padx=5, pady=2)
            label_email.grid(row=i, column=2, sticky="e", padx=5, pady=2)
            entry_email.grid(row=i, column=3, sticky="w", padx=5, pady=2)

            self.entries[f"Email Type {i+1}"] = entry_type
            self.entries[f"Email {i+1}"] = entry_email

        # === Container: Subscriptions ===
        subscriptions_frame = ttk.LabelFrame(self, text="Subscriptions", padding=10)
        subscriptions_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Name", "Family", "Purchase Date", "Expiration Date", "Quantity")

        # Create a Treeview and attach a scrollbar
        tree_scrollbar = ttk.Scrollbar(subscriptions_frame, orient="vertical")
        self.tree = ttk.Treeview(
            subscriptions_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scrollbar.set
        )
        tree_scrollbar.config(command=self.tree.yview)
        tree_scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, side="left")

        # Configure Treeview columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        # Insert 10 example subscriptions
        example_subs = [
            ("Newsletter", "Marketing", "2023-01-01", "2024-01-01", 1),
            ("Premium Access", "Digital", "2023-06-15", "2024-06-15", 3),
            ("Video Library", "Entertainment", "2023-02-10", "2024-02-10", 2),
            ("Fitness Plan", "Health", "2023-03-01", "2024-03-01", 1),
            ("eBooks", "Education", "2023-05-20", "2024-05-20", 5),
            ("Music Pass", "Entertainment", "2023-08-01", "2024-08-01", 2),
            ("Language Course", "Education", "2023-07-15", "2024-07-15", 1),
            ("Cloud Storage", "Utilities", "2023-09-01", "2024-09-01", 1),
            ("VPN Service", "Security", "2023-10-01", "2024-10-01", 1),
            ("Analytics Suite", "Business", "2023-11-10", "2024-11-10", 10),
        ]

        for sub in example_subs:
            self.tree.insert("", tk.END, values=sub)


# For standalone test (optional)
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window
    CustomerZoomedWindow(root).mainloop()
