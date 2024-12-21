import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
class Admin:
    def get_customers(self):
        try:
            with open("customers.txt", "r") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []
    def get_drivers(self):
        try:
            with open("drivers.txt", "r") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []
    def get_bookings(self):
        try:
            with open("bookings.txt", "r") as file:
                bookings = []
                for line in file.readlines():
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        # Ensure there are exactly 8 parts (phone, name, from, to, date, time, driver, status)
                        if len(parts) == 8:
                            bookings.append({
                                "phone": parts[0],
                                "name": parts[1],
                                "from": parts[2],
                                "to": parts[3],
                                "date": parts[4],
                                "time": parts[5],
                                "driver": parts[6],
                                "status": parts[7]
                            })
                        else:
                            print(f"Skipping malformed booking: {line}")  # Debugging message
                return bookings
        except FileNotFoundError:
            return []
    def update_bookings(self, bookings):
        with open("bookings.txt", "w") as file:
            for booking in bookings:
                file.write(
                    f"{booking['phone']},{booking['name']},{booking['from']},{booking['to']},{booking['date']},{booking['time']},{booking['driver']},{booking['status']}\n")

def open_admin_page():
    admin = Admin()
    def refresh_data():
        for item in customer_list.get_children():
            customer_list.delete(item)
        customers = admin.get_customers()
        for i, customer in enumerate(customers):
            fields = customer.split(",")
            if len(fields) >= 4:
                contact, name, address, email = fields
                customer_list.insert("", "end", values=(i + 1, contact, name, address, email))
            else:
                customer_list.insert("", "end", values=(i + 1, "Missing Info", "N/A", "N/A", "N/A"))
        for item in driver_list.get_children():
            driver_list.delete(item)
        drivers = admin.get_drivers()
        for i, driver in enumerate(drivers):
            fields = driver.split(",")
            if len(fields) >= 3:
                driver_name, car_number, contact_info = fields
                driver_list.insert("", "end", values=(i + 1, driver_name, car_number, contact_info))
            else:
                driver_list.insert("", "end", values=(i + 1, "Missing Info", "N/A", "N/A"))
        for item in booking_list.get_children():
            booking_list.delete(item)
        bookings = admin.get_bookings()
        if bookings:
            for i, booking in enumerate(bookings):
                phone = booking.get("phone", "N/A")
                name = booking.get("name", "N/A")
                departure = booking.get("from", "N/A")
                destination = booking.get("to", "N/A")
                date = booking.get("date", "N/A")
                time = booking.get("time", "N/A")
                driver = booking.get("driver", "N/A")
                status = booking.get("status", "N/A")
                booking_list.insert("", "end",
                                    values=(i + 1, phone, name, departure, destination, date, time, driver, status))
        else:
            booking_list.insert("", "end", values=("No bookings found", "", "", "", "", "", "", "", ""))

        analytics_label.config(
            text=f"Total customers : {len(customers)} -|- Total drivers : {len(drivers)} -|- Total bookings : {len(bookings)}"
        )
    def assign_driver():
        assign_window = tk.Toplevel(root)
        assign_window.title("Assign Driver")
        assign_window.geometry("400x250")
        bookings = admin.get_bookings()
        drivers = admin.get_drivers()

        booking_options = [f"{booking['phone']} - {booking['name']}" for booking in bookings]
        driver_options = [driver.split(",")[0] for driver in drivers]  # Assuming the first part is the driver name

        booking_label = ttk.Label(assign_window, text="Select Booking:")
        booking_label.pack(pady=10)
        booking_dropdown = ttk.Combobox(assign_window, values=booking_options, width=30)
        booking_dropdown.pack(pady=10)

        driver_label = ttk.Label(assign_window, text="Select Driver:")
        driver_label.pack(pady=10)
        driver_dropdown = ttk.Combobox(assign_window, values=driver_options, width=30)
        driver_dropdown.pack(pady=10)

        def confirm_assignment():
            selected_booking = booking_dropdown.get()
            selected_driver = driver_dropdown.get()

            if selected_booking and selected_driver:
                phone_number = selected_booking.split(" - ")[0]
                for booking in bookings:
                    if booking["phone"] == phone_number:
                        booking["driver"] = selected_driver
                        booking["status"] = "Assigned"
                        break
                admin.update_bookings(bookings)
                refresh_data()
                messagebox.showinfo("Success", f"Driver {selected_driver} has been assigned to the booking.")
                assign_window.destroy()
            else:
                messagebox.showwarning("Selection error", "Please select both a booking and a driver.")

        assign_button = ttk.Button(assign_window, text="Assign Driver", command=confirm_assignment)
        assign_button.pack(pady=20)

    root = tk.Tk()
    root.title("Admin Panel")
    root.geometry("900x700")
    root.configure(bg="#f2f4f7")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 12), background="#4CAF50", foreground="white", padding=5)
    style.configure("Treeview", font=("Helvetica", 10), rowheight=30)
    style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#4CAF50", foreground="white")
    style.configure("TLabel", font=("Helvetica", 12), background="#f2f4f7", foreground="#333")
    style.configure("TFrame", background="#f2f4f7")

    title_label = ttk.Label(root, text="Admin Dashboard", font=("Helvetica", 24, "bold"), background="#f2f4f7")
    title_label.pack(pady=20)

    notebook = ttk.Notebook(root, style="TNotebook")
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    customer_frame = ttk.Frame(notebook)
    notebook.add(customer_frame, text="Customers")

    customer_list = ttk.Treeview(
        customer_frame, columns=("ID", "Contact", "Name", "Address", "Email"),
        show="headings", height=15
    )
    customer_list.heading("ID", text="ID")
    customer_list.column("ID", width=40, anchor="center")
    customer_list.heading("Contact", text="Contact")
    customer_list.column("Contact", width=150, anchor="center")
    customer_list.heading("Name", text="Name")
    customer_list.column("Name", width=120, anchor="center")
    customer_list.heading("Address", text="Address")
    customer_list.column("Address", width=200, anchor="center")
    customer_list.heading("Email", text="Email")
    customer_list.column("Email", width=200, anchor="center")
    customer_list.pack(fill="both", expand=True, padx=20, pady=20)

    driver_frame = ttk.Frame(notebook)
    notebook.add(driver_frame, text="Drivers")

    driver_list = ttk.Treeview(
        driver_frame, columns=("ID", "Driver Name", "Car Number", "Contact Info"),
        show="headings", height=15
    )
    driver_list.heading("ID", text="ID")
    driver_list.column("ID", width=40, anchor="center")
    driver_list.heading("Driver Name", text="Driver Name")
    driver_list.column("Driver Name", width=150, anchor="center")
    driver_list.heading("Car Number", text="Car Number")
    driver_list.column("Car Number", width=150, anchor="center")
    driver_list.heading("Contact Info", text="Contact Info")
    driver_list.column("Contact Info", width=150, anchor="center")
    driver_list.pack(fill="both", expand=True, padx=20, pady=20)
    booking_frame = ttk.Frame(notebook)
    notebook.add(booking_frame, text="Bookings")
    booking_list = ttk.Treeview(
        booking_frame,
        columns=("ID", "Phone", "Name", "From", "To", "Date", "Time", "Driver", "Status"),
        show="headings", height=15
    )
    booking_list.heading("ID", text="ID")
    booking_list.column("ID", width=40, anchor="center")
    booking_list.heading("Phone", text="Phone")
    booking_list.column("Phone", width=100, anchor="center")
    booking_list.heading("Name", text="Name")
    booking_list.column("Name", width=150, anchor="center")
    booking_list.heading("From", text="From")
    booking_list.column("From", width=200, anchor="center")
    booking_list.heading("To", text="To")
    booking_list.column("To", width=200, anchor="center")
    booking_list.heading("Date", text="Date")
    booking_list.column("Date", width=100, anchor="center")
    booking_list.heading("Time", text="Time")
    booking_list.column("Time", width=100, anchor="center")
    booking_list.heading("Driver", text="Driver")
    booking_list.column("Driver", width=150, anchor="center")
    booking_list.heading("Status", text="Status")
    booking_list.column("Status", width=100, anchor="center")
    booking_list.pack(fill="both", expand=True, padx=20, pady=20)

    analytics_label = ttk.Label(root, text="Loading data...", style="TLabel")
    analytics_label.pack(pady=10)

    refresh_button = ttk.Button(root, text="Refresh Data", command=refresh_data)
    refresh_button.pack(pady=20)

    assign_driver_frame = ttk.Frame(notebook)
    notebook.add(assign_driver_frame, text="Assign Driver")

    assign_button = ttk.Button(assign_driver_frame, text="Assign Driver", command=assign_driver)
    assign_button.pack(pady=20)

    refresh_data()
    root.mainloop()
if __name__ == "__main__":
    open_admin_page()