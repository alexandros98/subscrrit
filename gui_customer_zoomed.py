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
        self.customer_id = customer_data[0]

        options_frame = ttk.LabelFrame(self, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=(0, 10))

        save_button = ttk.Button(options_frame, text="Save", command=self.on_save)
        close_button = ttk.Button(options_frame, text="Close", command=self.destroy)

        save_button.pack(side="left", padx=5)
        close_button.pack(side="left", padx=5)

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

        # --- Country Dropdown ---
        label_country = ttk.Label(general_info_frame, text="Country:")
        label_country.grid(row=len(general_fields), column=0, sticky="e", padx=5, pady=2)

        self.country_var = tk.StringVar()
        self.country_dropdown = ttk.Combobox(general_info_frame, textvariable=self.country_var, width=57, state="readonly")
        self.country_dropdown.grid(row=len(general_fields), column=1, sticky="w", padx=5, pady=2)
        self.country_map = {}  # name -> code

        # ---- Type Dropdown ---
        label_type = ttk.Label(general_info_frame, text="Customer Type:")
        label_type.grid(row=len(general_fields)+1, column=0, sticky="e", padx=5, pady=2)

        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(general_info_frame, textvariable=self.type_var, width=57, state="readonly")
        self.type_dropdown.grid(row=len(general_fields)+1, column=1, sticky="w", padx=5, pady=2)
        self.type_map = {}  # name -> code

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


        # --- subscriptions related stuff start here ---
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
        
        #my attempt to connect to the database and fill the rows
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            query = ("""
                select software_products.name, software_family.name, purchase_date, expiration_date, customer_subscriptions.quantity
                from customer_subscriptions
                inner join software_products on software_products.id = customer_subscriptions.product
                inner join software_family on software_family.code = software_products.id
                where customer_subscriptions.customer = ?
            """)
            cursor.execute(query, self.customer_id)
            customer_subscriptions = cursor.fetchall()
            cursor.close()
            conn.close()
            print("****************Data fetched succesfully********************")
            print(self.customer_id)
            print(customer_subscriptions)
        except:
            print("data could not be fetched")
        print("---------------------------------------------------------------------------------")
        print(customer_subscriptions)

        for row in customer_subscriptions:
            # Convert all items in the row to string (especially date objects)
            formatted_row = [str(item) for item in row]
            print("Inserting formatted row:", formatted_row)
            self.tree.insert("", "end", values=formatted_row)

        self.load_countries()
        self.load_customer_types()

        if customer_data:
            self.prefill_customer_info(customer_data)

    def connect_db(self):
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=COMPUTOR\\ALEXTESTS22;'
            'DATABASE=okay;UID=sa;PWD=1'
        )

    def load_countries(self):

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT code, name FROM countries ORDER BY name")
            countries = cursor.fetchall()
            cursor.close()
            conn.close()

            # Map country name to code
            self.country_map = {name: code for code, name in countries}
            self.country_dropdown['values'] = list(self.country_map.keys())
        except Exception as e:
            messagebox.showerror("Error", f"Could not load countries:\n{e}")

    def load_customer_types(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT code, name FROM customer_type ORDER BY name")
            types = cursor.fetchall()
            cursor.close()
            conn.close()

            self.type_map = {name: code for code, name in types}
            self.type_dropdown['values'] = list(self.type_map.keys())
        except Exception as e:
            messagebox.showerror("Error", f"Could not load customer types:\n{e}")

    def on_save(self):
        try:
            values = {field: self.entries[field].get() for field in self.entries}
            country_code = self.country_map.get(self.country_var.get())
            type_code = self.type_map.get(self.type_var.get())

            conn = self.connect_db()
            cursor = conn.cursor()

            if self.customer_id:
                query = """
                    UPDATE customers SET
                        name = ?, vatNr = ?, profession = ?, address = ?, city = ?, postalCode = ?,
                        phone1Type = ?, phone1 = ?,
                        phone2Type = ?, phone2 = ?,
                        phone3Type = ?, phone3 = ?,
                        email1Type = ?, email1 = ?,
                        email2Type = ?, email2 = ?,
                        email3Type = ?, email3 = ?,
                        country = ?,
                        type = ?
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
                    country_code,
                    type_code,
                    self.customer_id
                )
                cursor.execute(query, params)
            else:
                new_id = str(uuid.uuid4())
                query = """
                    INSERT INTO customers
                        (id, name, vatNr, profession, address, city, postalCode,
                         phone1Type, phone1,
                         phone2Type, phone2,
                         phone3Type, phone3,
                         email1Type, email1,
                         email2Type, email2,
                         email3Type, email3,
                         country)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    new_id, values["Name"], values["VAT Nr"], values["Profession"], values["Address"],
                    values["City"], values["Postal Code"],
                    values["Phone Type 1"], values["Phone 1"],
                    values["Phone Type 2"], values["Phone 2"],
                    values["Phone Type 3"], values["Phone 3"],
                    values["Email Type 1"], values["Email 1"],
                    values["Email Type 2"], values["Email 2"],
                    values["Email Type 3"], values["Email 3"],
                    country_code
                )
                cursor.execute(query, params)

            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Customer data saved successfully!")
            self.destroy()
            if self.master:
                self.master.load_customers()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save customer data:\n{e}")

    def prefill_customer_info(self, data):
        # Data tuple:
        # (id, name, vatNr, profession, address, city, postalCode, country_code,
        #  phone1Type, phone1, phone2Type, phone2, phone3Type, phone3,
        #  email1Type, email1, email2Type, email2, email3Type, email3)

        if not data:
            return

        (
            self.customer_id, name, vat_nr, profession, address, city, postal_code, country_code, customer_type_code,
            phone1Type, phone1, phone2Type, phone2, phone3Type, phone3,
            email1Type, email1, email2Type, email2, email3Type, email3
        ) = data

        #print("Opening edit window with:", data[0])
        self.temp = data[0]

        self.entries["Name"].insert(0, name or "")
        self.entries["VAT Nr"].insert(0, vat_nr or "")
        self.entries["Profession"].insert(0, profession or "")
        self.entries["Address"].insert(0, address or "")
        self.entries["City"].insert(0, city or "")
        self.entries["Postal Code"].insert(0, postal_code or "")

        # Set country dropdown by matching country code
        if country_code:
            for cname, ccode in self.country_map.items():
                if ccode == country_code:
                    self.country_var.set(cname)
                    break

        # Set customer type dropdown by matching code
        if customer_type_code:
            for tname, tcode in self.type_map.items():
                if tcode == customer_type_code:
                    self.type_var.set(tname)
                    break

        self.entries["Phone Type 1"].insert(0, phone1Type or "")
        self.entries["Phone 1"].insert(0, phone1 or "")
        self.entries["Phone Type 2"].insert(0, phone2Type or "")
        self.entries["Phone 2"].insert(0, phone2 or "")
        self.entries["Phone Type 3"].insert(0, phone3Type or "")
        self.entries["Phone 3"].insert(0, phone3 or "")

        self.entries["Email Type 1"].insert(0, email1Type or "")
        self.entries["Email 1"].insert(0, email1 or "")
        self.entries["Email Type 2"].insert(0, email2Type or "")
        self.entries["Email 2"].insert(0, email2 or "")
        self.entries["Email Type 3"].insert(0, email3Type or "")
        self.entries["Email 3"].insert(0, email3 or "")
