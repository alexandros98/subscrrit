import tkinter as tk
from tkinter import ttk
import pyodbc

# Import the zoomed window class
from gui_customer_zoomed import CustomerZoomedWindow

class CustomerListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Customers List")
        self.geometry("900x600")
        self.configure(padx=20, pady=20)

        # --- Options container ---
        options_frame = ttk.LabelFrame(self, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=(0, 10))

        edit_button = ttk.Button(options_frame, text="Edit", command=self.on_edit)
        delete_button = ttk.Button(options_frame, text="Delete", command=self.on_delete)
        new_button = ttk.Button(options_frame, text="New", command=self.on_new)

        new_button.pack(side="left", padx=5)
        edit_button.pack(side="left", padx=5)
        delete_button.pack(side="left", padx=5)

        # --- List container ---
        list_frame = ttk.LabelFrame(self, text="Customers", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Columns based on your SQL query
        columns = ("Type", "Name", "VAT Nr", "Address", "City", "Postal Code")

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")

        self.customers_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.customers_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.customers_tree.pack(fill="both", expand=True, side="left")

        # Setup columns headings and width
        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, anchor="center", width=140)

        # Connect to DB and load customers
        self.load_customers()

    def load_customers(self):
        # Database connection settings
        server = "COMPUTOR\\ALEXTESTS22"
        database = "okay"
        username = "sa"
        password = "1"

        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        cursor = conn.cursor()

        query = """
            select customer_type.name, customers.name, customers.vatNr, customers.address, customers.city, customers.postalCode
            from customers
            inner join customer_type on customer_type.code = customers.type
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Debug: print raw rows fetched
        for row in rows:
            print(row)  # Should print something like ('Επιχείρηση - ΤΣΟΚΟΣ ΑΝΩΝΥΜH ΕΤΑΙΡΕΙΑ', '800932757', 'ΝΕΑ ΔΗΜΟΤΙΚΗ ΑΓΟΡΑ', 'ΧΑΛΚΙΔΑ', '34100')

        # Clear any existing data
        for row_id in self.customers_tree.get_children():
            self.customers_tree.delete(row_id)

        # Insert fetched data into the tree with explicit tuple conversion
        for row in rows:
            # Convert each field to str in case of None or other types
            values = tuple(str(field) if field is not None else "" for field in row)
            self.customers_tree.insert("", tk.END, values=values)

        conn.close()


    def on_edit(self):
        selected = self.customers_tree.selection()
        if not selected:
            print("No customer selected for edit")
            return
        # For demo, open the zoomed window (you can add prefill logic here)
        CustomerZoomedWindow(self)

    def on_delete(self):
        selected = self.customers_tree.selection()
        if not selected:
            print("No customer selected for delete")
            return
        for sel in selected:
            print(f"Deleting customer: {self.customers_tree.item(sel)['values']}")
            self.customers_tree.delete(sel)

    def on_new(self):
        # Open new customer window
        CustomerZoomedWindow(self)


if __name__ == "__main__":
    app = CustomerListApp()
    app.mainloop()
