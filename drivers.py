import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
class Driver:
    def __init__(self):
        self.name = None
        self.vehicle_number = None
        self.contact_number = None
        self.assigned_trips = []

    def register(self, name, vehicle_number, contact_number):
        if not name or not vehicle_number or not contact_number:
            return "All fields are required for registration!"
        self.name = name
        self.vehicle_number = vehicle_number
        self.contact_number = contact_number
        with open("drivers.txt", "a") as file:
            file.write(f"{self.name},{self.vehicle_number},{self.contact_number}\n")
        return f"Driver {name} registered successfully!"

    def view_assigned_trips_by_contact(self, contact_number):
        try:
            if not contact_number:
                return "Please provide a contact number!"
            with open("bookings.txt", "r") as file:
                self.assigned_trips = [
                    line.strip() for line in file.readlines()
                    if line.strip().split(",")[-1].strip().lower() == contact_number.strip().lower()
                ]
            return self.assigned_trips or "No assigned trips found!"
        except FileNotFoundError:
            return "No bookings found!"

def open_driver_page():
    driver = Driver()
    def register_driver():
        name = name_entry.get()
        vehicle_number = vehicle_entry.get()
        contact_number = contact_entry.get()
        result = driver.register(name, vehicle_number, contact_number)
        messagebox.showinfo("Registration", result)
        reset_registration_fields()

    def view_assigned_trips():
        contact_number = search_entry.get()
        if not contact_number:
            messagebox.showwarning("Search trips", "Please enter contact number!")
            return
        trips = driver.view_assigned_trips_by_contact(contact_number)
        trips_table.delete(*trips_table.get_children())  # Clear the table
        if isinstance(trips, str):  # If trips is an error message
            messagebox.showinfo("Assigned trips", trips)
        else:
            for idx, trip in enumerate(trips, start=1):
                trips_table.insert("", "end", values=(idx, trip))
    def reset_registration_fields():
        name_entry.delete(0, tk.END)
        vehicle_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Driver Dashboard")
    root.geometry("800x600")
    root.configure(bg="#f0f8ff")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", padding=8, font=("Helvetica", 12), background="#4CAF50", foreground="white")
    style.configure("TLabel", font=("Helvetica", 11))
    style.configure("TFrame", background="#f0f8ff")
    style.configure("Treeview", font=("Helvetica", 10), padding=5, rowheight=30)
    style.configure("Treeview.Heading", background="#4CAF50", foreground="white", font=("Helvetica", 12))

    title_label = tk.Label(root, text="Taxi Driver Dashboard", font=("Helvetica", 24, "bold"), bg="#f0f8ff", fg="#333")
    title_label.pack(pady=20)

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True, fill="both")

    registration_frame = ttk.Frame(notebook)
    registration_frame.configure(style="TFrame")
    notebook.add(registration_frame, text="Driver Registration")
    ttk.Label(registration_frame, text="Driver Name:", style="TLabel").grid(row=0, column=0, padx=20, pady=10,
                                                                            sticky="w")
    name_entry = ttk.Entry(registration_frame, width=40)
    name_entry.grid(row=0, column=1, padx=20, pady=10)
    ttk.Label(registration_frame, text="Vehicle Number:", style="TLabel").grid(row=1, column=0, padx=20, pady=10,
                                                                               sticky="w")
    vehicle_entry = ttk.Entry(registration_frame, width=40)
    vehicle_entry.grid(row=1, column=1, padx=20, pady=10)
    ttk.Label(registration_frame, text="Contact Number:", style="TLabel").grid(row=2, column=0, padx=20, pady=10,
                                                                               sticky="w")
    contact_entry = ttk.Entry(registration_frame, width=40)
    contact_entry.grid(row=2, column=1, padx=20, pady=10)

    register_button = ttk.Button(registration_frame, text="Register", command=register_driver)
    register_button.grid(row=3, column=1, padx=20, pady=20, sticky="e")

    trips_frame = ttk.Frame(notebook)
    trips_frame.configure(style="TFrame")
    notebook.add(trips_frame, text="Assigned Trips")

    ttk.Label(trips_frame, text="Search by Contact:", style="TLabel").grid(row=0, column=0, padx=20, pady=10,
                                                                           sticky="w")
    search_entry = ttk.Entry(trips_frame, width=40)
    search_entry.grid(row=0, column=1, padx=20, pady=10)

    search_button = ttk.Button(trips_frame, text="Search Trips", command=view_assigned_trips)
    search_button.grid(row=0, column=2, padx=20, pady=10)

    trips_table = ttk.Treeview(trips_frame, columns=("No", "Trip Details"), show="headings", height=12)
    trips_table.heading("No", text="No.")
    trips_table.column("No", width=50, anchor="center")
    trips_table.heading("Trip Details", text="Trip Details")
    trips_table.column("Trip Details", stretch=True)
    trips_table.grid(row=1, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")
    root.mainloop()
if __name__ == "__main__":
    open_driver_page()