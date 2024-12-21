import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
class Customer:
    def __init__(self):
        self.customers_file = "customers.txt"
        self.bookings_file = "bookings.txt"
        self.registered_customers = self.load_customers()
        self.bookings = self.load_bookings()
    def load_customers(self):
        customers = {}
        if os.path.exists(self.customers_file):
            with open(self.customers_file, "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == 4:
                        phone, name, address, email = data
                        customers[phone] = {"Name": name, "Address": address, "Email": email}
        return customers
    def save_customers(self):
        with open(self.customers_file, "w") as file:
            for phone, info in self.registered_customers.items():
                line = f"{phone},{info['Name']},{info['Address']},{info['Email']}\n"
                file.write(line)
    def load_bookings(self):
        bookings = {}
        if os.path.exists(self.bookings_file):
            with open(self.bookings_file, "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == 7:
                        phone, name, pickup, dropoff, date, time, driver = data
                        if phone not in bookings:
                            bookings[phone] = []
                        bookings[phone].append({
                            "Name": name,
                            "Pickup": pickup,
                            "Dropoff": dropoff,
                            "Date": date,
                            "Time": time,
                            "Driver": driver
                        })
        return bookings
    def save_bookings(self):
        with open(self.bookings_file, "w") as file:
            for phone, booking_list in self.bookings.items():
                for booking in booking_list:
                    line = (
                        f"{phone},{booking['Name']},{booking['Pickup']},"
                        f"{booking['Dropoff']},{booking['Date']},{booking['Time']},{booking['Driver']}\n"
                    )
                    file.write(line)
    def register(self, name, address, phone, email):
        if not name or not address or not phone or not email :
            return "All fields are required!"
        if phone in self.registered_customers:
            return f"Phone number {phone} is already registered!"
        self.registered_customers[phone] = {"Name": name, "Address": address, "Email": email}
        self.bookings[phone] = []
        self.save_customers()
        return f"Customer {name} registered successfully!"
    def book_taxi(self, phone, pickup, dropoff, date, time):
        if not pickup or not dropoff or not date or not time:
            return "Plz enter all fields to  book a taxi"
        if phone not in self.bookings:
            return f"Customer not found! {phone}!"
        customer_name = self.registered_customers[phone]["Name"]

        booking = {
            "Name": customer_name,
            "Pickup": pickup,
            "Dropoff": dropoff,
            "Date": date,
            "Time": time,
            "Driver": ""
        }
        self.bookings[phone].append(booking)
        self.save_bookings()
        return "Taxi booked successfully!"

    def view_bookings(self, phone):
        if phone not in self.bookings or not self.bookings[phone]:
            return f"Booking not found {phone}!"
        return self.bookings[phone]

def open_customer_registration():
    customer = Customer()
    def register_customer():
        name = name_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        result = customer.register(name, address, phone, email)
        messagebox.showinfo("Registration", result)
        reset_registration_fields()

    def book_taxi():
        phone = phone_entry.get()
        pickup = pickup_entry.get()
        dropoff = dropoff_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        result = customer.book_taxi(phone, pickup, dropoff, date, time)
        messagebox.showinfo("Booking", result)
        reset_booking_fields()

    def view_bookings():
        phone = search_entry.get()
        bookings = customer.view_bookings(phone)
        bookings_table.delete(*bookings_table.get_children())  # Clear the table
        if isinstance(bookings, str):
            messagebox.showinfo("Bookings", bookings)
        else:
            for idx, booking in enumerate(bookings, start=1):
                bookings_table.insert("", "end", values=(
                    idx,
                    booking["Pickup"],
                    booking["Dropoff"],
                    booking["Date"],
                    booking["Time"],
                    booking["Driver"] if booking["Driver"] else "Not Assigned"
                ))
    def reset_registration_fields():
        name_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
    def reset_booking_fields():
        pickup_entry.delete(0, tk.END)
        dropoff_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Customer dashboard")
    root.geometry("900x700")
    root.configure(bg="#f2f4f7")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", padding=8, font=("Helvetica", 12), background="#4CAF50", foreground="white")
    style.configure("TLabel", font=("Helvetica", 11))
    style.configure("TFrame", background="#f2f4f7")
    style.configure("Treeview", font=("Helvetica", 10), padding=5, rowheight=30)
    style.configure("Treeview.Heading", background="#4CAF50", foreground="white", font=("Helvetica", 12))

    title_label = tk.Label(root, text="Customer dashboard", font=("Helvetica", 24, "bold"), bg="#f2f4f7", fg="#333")
    title_label.pack(pady=20)

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True, fill="both")

    registration_frame = ttk.Frame(notebook)
    registration_frame.configure(style="TFrame")
    notebook.add(registration_frame, text="Customer registration")

    ttk.Label(registration_frame, text="Name:", style="TLabel").grid(row=0, column=0, padx=20, pady=10, sticky="w")
    name_entry = ttk.Entry(registration_frame, width=40)
    name_entry.grid(row=0, column=1, padx=20, pady=10)

    ttk.Label(registration_frame, text="Address:", style="TLabel").grid(row=1, column=0, padx=20, pady=10, sticky="w")
    address_entry = ttk.Entry(registration_frame, width=40)
    address_entry.grid(row=1, column=1, padx=20, pady=10)

    ttk.Label(registration_frame, text="Phone:", style="TLabel").grid(row=2, column=0, padx=20, pady=10, sticky="w")
    phone_entry = ttk.Entry(registration_frame, width=40)
    phone_entry.grid(row=2, column=1, padx=20, pady=10)

    ttk.Label(registration_frame, text="Email:", style="TLabel").grid(row=3, column=0, padx=20, pady=10, sticky="w")
    email_entry = ttk.Entry(registration_frame, width=40)
    email_entry.grid(row=3, column=1, padx=20, pady=10)

    register_button = ttk.Button(registration_frame, text="Register", command=register_customer)
    register_button.grid(row=4, column=1, padx=20, pady=20, sticky="e")

    booking_frame = ttk.Frame(notebook)
    booking_frame.configure(style="TFrame")
    notebook.add(booking_frame, text="Book Taxi")

    ttk.Label(booking_frame, text="Pickup Location:", style="TLabel").grid(row=0, column=0, padx=20, pady=10,
                                                                           sticky="w")
    pickup_entry = ttk.Entry(booking_frame, width=40)
    pickup_entry.grid(row=0, column=1, padx=20, pady=10)

    ttk.Label(booking_frame, text="Dropoff Location:", style="TLabel").grid(row=1, column=0, padx=20, pady=10,
                                                                            sticky="w")
    dropoff_entry = ttk.Entry(booking_frame, width=40)
    dropoff_entry.grid(row=1, column=1, padx=20, pady=10)

    ttk.Label(booking_frame, text="Date (YYYY-MM-DD):", style="TLabel").grid(row=2, column=0, padx=20, pady=10,
                                                                             sticky="w")
    date_entry = ttk.Entry(booking_frame, width=40)
    date_entry.grid(row=2, column=1, padx=20, pady=10)

    ttk.Label(booking_frame, text="Time (HH:MM):", style="TLabel").grid(row=3, column=0, padx=20, pady=10, sticky="w")
    time_entry = ttk.Entry(booking_frame, width=40)
    time_entry.grid(row=3, column=1, padx=20, pady=10)

    book_button = ttk.Button(booking_frame, text="Book Now", command=book_taxi)
    book_button.grid(row=4, column=1, padx=20, pady=20, sticky="e")

    bookings_frame = ttk.Frame(notebook)
    bookings_frame.configure(style="TFrame")
    notebook.add(bookings_frame, text="View Bookings")

    ttk.Label(bookings_frame, text="Search by Phone:", style="TLabel").grid(row=0, column=0, padx=20, pady=10,
                                                                            sticky="w")
    search_entry = ttk.Entry(bookings_frame, width=40)
    search_entry.grid(row=0, column=1, padx=20, pady=10)

    search_button = ttk.Button(bookings_frame, text="Search Bookings", command=view_bookings)
    search_button.grid(row=0, column=2, padx=20, pady=10)

    columns = ("No.", "Pickup", "Dropoff", "Date", "Time", "Driver")
    bookings_table = ttk.Treeview(bookings_frame, columns=columns, show="headings", height=12)
    for col in columns:
        bookings_table.heading(col, text=col)
        bookings_table.column(col, stretch=True, anchor="center")
    bookings_table.grid(row=1, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")
    root.mainloop()
if __name__ == "__main__":
    open_customer_registration()