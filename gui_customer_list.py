import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

from gui_customer_zoomed import CustomerZoomedWindow


class CustomerListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Customers List")
        self.geometry("1100x600")
        self.configure(padx=20, pady=20)

        options_frame = ttk.LabelFrame(self, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=(0, 10))

        new_button = ttk.Button(options_frame, text="New", command=self.on_new)
        edit_button = ttk.Button(options_frame, text="Edit", command=self.on_edit)
        delete_button = ttk.Button(options_frame, text="Delete", command=self.on_delete)

        new_button.pack(side="left", padx=5)
        edit_button.pack(side="left", padx=5)
        delete_button.pack(side="left", padx=5)

        list_frame = ttk.LabelFrame(self, text="Customers", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Type", "Name", "VAT Nr", "Address", "City", "Postal Code")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        self.customers_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.customers_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.customers_tree.pack(fill="both", expand=True, side="left")

        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, anchor="center", width=140)

        self.load_customers()

    def load_customers(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        query = """
            SELECT customer_type.name, customers.name, customers.vatNr, 
            customers.address, customers.city, customers.postalCode
            FROM customers
            LEFT JOIN customer_type ON customer_type.code = customers.type
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        for row_id in self.customers_tree.get_children():
            self.customers_tree.delete(row_id)

        for row in rows:
            values = tuple(str(field) if field is not None else "" for field in row)
            self.customers_tree.insert("", tk.END, values=values)

        conn.close()

    def on_edit(self):
        selected = self.customers_tree.selection()
        if not selected:
            print("No customer selected for edit")
            return

        item = self.customers_tree.item(selected[0])
        vat_nr = item["values"][2]
        full_data = self.get_full_customer_data(vat_nr)

        if full_data:
            CustomerZoomedWindow(self, customer_data=full_data)
        else:
            print(f"No customer found with VAT Nr: {vat_nr}")

    def on_new(self):
        CustomerZoomedWindow(self)

    def on_delete(self):
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a customer to delete.")
            return

        customer_values = self.customers_tree.item(selected[0])["values"]
        customer_name = customer_values[1]
        vat_number = customer_values[2]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{customer_name}'?")
        if not confirm:
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE vatNr = ?", vat_number)
            conn.commit()
            conn.close()
            self.load_customers()
            messagebox.showinfo("Deleted", f"Customer '{customer_name}' has been deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete customer:\n{e}")

    def connect_db(self):
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=COMPUTOR\\ALEXTESTS22;'
            'DATABASE=okay;UID=sa;PWD=1'
        )

    def get_full_customer_data(self, vat_nr):
        conn = self.connect_db()
        cursor = conn.cursor()
        query = """
            SELECT customers.id, customers.name, customers.vatNr, customers.profession, customers.address,
                customers.city, customers.postalCode, countries.name,
                customers.phone1Type, customers.phone1,
                customers.phone2Type, customers.phone2,
                customers.phone3Type, customers.phone3,
                customers.email1Type, customers.email1,
                customers.email2Type, customers.email2,
                customers.email3Type, customers.email3
            FROM customers
            left JOIN countries ON countries.code = customers.country
            WHERE customers.vatNr = ?
        """
        cursor.execute(query, vat_nr)
        result = cursor.fetchone()
        conn.close()
        return result


if __name__ == "__main__":
    app = CustomerListApp()
    app.mainloop()
