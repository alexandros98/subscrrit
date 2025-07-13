import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import uuid


class CustomerZoomedWindow(tk.Toplevel):
    def __init__(self, master=None, customer_data=None):
        super().__init__(master)
        self.title("Customer Information")
        self.geometry("1000x800")
        self.configure(padx=20, pady=20)

        self.entries = {}
        self.customer_id = None  # <-- Track existing customer ID

        # Options
        options_frame = ttk.LabelFrame(self, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=(0, 10))

        save_button = ttk.Button(options_frame, text="Save", command=self.on_save)
        close_button = ttk.Button(options_frame, text="Close", command=self.destroy)

        save_button.pack(side="left", padx=5)
        close_button.pack(side="left", padx=5)

        # Basic Info
        basic_info_frame = ttk.LabelFrame(self, text="Basic Info", padding=10)
        basic_info_frame.pack(fill="x", padx=10, pady=10)

        general_info_frame = ttk.Frame(basic_info_frame)
        general_info_frame.pack(fill="x", pady=(0, 10))

        general_fields = [
            "Name", "VAT Nr", "Profession", "Address",
            "City", "Postal Code"
        ]

        for i, field in enumerate(general_fields):
            label = ttk.Label(general_info_frame, text=field + ":")
            entry = ttk.Entry(general_info_frame, width=60)
            label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=2)
            self.entries[field] = entry

        contact_frame = ttk.Frame(basic_info_frame)
        contact_frame.pack(fill="x", pady=10)

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

        subscriptions_frame = ttk.LabelFrame(self, text="Subscriptions", padding=10)
        subscriptions_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Name", "Family", "Purchase Date", "Expiration Date", "Quantity")
        tree_scrollbar = ttk.Scrollbar(subscriptions_frame, orient="vertical")
        self.tree = ttk.Treeview(
            subscriptions_frame, columns=columns, show="headings", yscrollcommand=tree_scrollbar.set
        )
        tree_scrollbar.config(command=self.tree.yview)
        tree_scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, side="left")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        if customer_data:
            self.prefill_customer_info(customer_data)

    def connect_db(self):
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=COMPUTOR\\ALEXTESTS22;'
            'DATABASE=okay;UID=sa;PWD=1'
        )

    def on_save(self):
        try:
            values = {field: self.entries[field].get() for field in self.entries}

            print("\n--- DEBUG: Customer Save ---")
            for k, v in values.items():
                print(f"{k}: {v}")

            conn = self.connect_db()
            cursor = conn.cursor()

            if self.customer_id:
                # Update existing customer
                print(f"Updating existing customer ID: {self.customer_id}")
                query = """
                    UPDATE customers SET
                        name = ?, vatNr = ?, profession = ?, address = ?, city = ?, postalCode = ?,
                        phone1Type = ?, phone1 = ?,
                        phone2Type = ?, phone2 = ?,
                        phone3Type = ?, phone3 = ?,
                        email1Type = ?, email1 = ?,
                        email2Type = ?, email2 = ?,
                        email3Type = ?, email3 = ?
                    WHERE id = ?
                """
                params = (
                    values["Name"], values["VAT Nr"], values["Profession"], values["Address"],
                    values["City"], values["Postal Code"],
                    values["Phone Type 1"], values["Phone 1"],
                    values["Phone Type 2"], values["Phone 2"],
                    values["Phone Type 3"], values["Phone 3"],
                    values["Email Type 1"], values["Email 1"],
                    values["Email Type 2"], values["Email 2"],
                    values["Email Type 3"], values["Email 3"],
                    self.customer_id
                )
                print("Customer updated successfully.")
                messagebox.showinfo("Success", "Customer updated successfully.")
            else:
                # Insert new customer
                self.customer_id = str(uuid.uuid4())
                print(f"Inserting new customer ID: {self.customer_id}")
                query = """
                    INSERT INTO customers(
                        id, name, vatNr, profession, address, city, postalCode,
                        phone1Type, phone1,
                        phone2Type, phone2,
                        phone3Type, phone3,
                        email1Type, email1,
                        email2Type, email2,
                        email3Type, email3
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    self.customer_id, values["Name"], values["VAT Nr"], values["Profession"], values["Address"],
                    values["City"], values["Postal Code"],
                    values["Phone Type 1"], values["Phone 1"],
                    values["Phone Type 2"], values["Phone 2"],
                    values["Phone Type 3"], values["Phone 3"],
                    values["Email Type 1"], values["Email 1"],
                    values["Email Type 2"], values["Email 2"],
                    values["Email Type 3"], values["Email 3"]
                )
                print("Customer saved successfully.")
                messagebox.showinfo("Success", "Customer saved successfully.")

            cursor.execute(query, params)
            conn.commit()
            cursor.close()
            conn.close()

            self.destroy()
            self.master.load_customers()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer:\n{e}")
            print("ERROR:", e)

    def prefill_customer_info(self, data):
        (
            id_value,
            name, vat, profession, address,
            city, postal_code, country,
            phone1_type, phone1,
            phone2_type, phone2,
            phone3_type, phone3,
            email1_type, email1,
            email2_type, email2,
            email3_type, email3
        ) = data

        self.customer_id = id_value  # <-- Save ID for update

        field_map = {
            "Name": name,
            "VAT Nr": vat,
            "Profession": profession,
            "Address": address,
            "City": city,
            "Postal Code": postal_code,
            "Phone Type 1": phone1_type,
            "Phone 1": phone1,
            "Phone Type 2": phone2_type,
            "Phone 2": phone2,
            "Phone Type 3": phone3_type,
            "Phone 3": phone3,
            "Email Type 1": email1_type,
            "Email 1": email1,
            "Email Type 2": email2_type,
            "Email 2": email2,
            "Email Type 3": email3_type,
            "Email 3": email3,
        }

        for field, value in field_map.items():
            if field in self.entries and value is not None:
                self.entries[field].insert(0, str(value))


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    CustomerZoomedWindow(root).mainloop()
