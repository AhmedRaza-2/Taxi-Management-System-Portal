import tkinter as tk
from tkinter import messagebox, simpledialog
from Customer import open_customer_registration
from drivers import open_driver_page
from admin import open_admin_page

class taxiBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Taxi Booking System")
        self.root.geometry("600x400")
        self.root.config(bg="#f0f0f0")
        self.createWidgets()

    def createWidgets(self):
        self.label_title = tk.Label(
            self.root,
            text="Taxi Booking System",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.label_title.pack(pady=20)

        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)
        button_style = {
            "font": ("Arial", 14),
            "bg": "#4CAF50",
            "fg": "white",
            "activebackground": "#45a049",
            "relief": "flat",
            "width": 20,
            "height": 2
        }

        self.customer_button = tk.Button(
            self.button_frame, text="Customer Page", command=self.customerPage, **button_style
        )
        self.customer_button.grid(row=0, column=0, pady=5)

        self.driver_button = tk.Button(
            self.button_frame, text="Driver Page", command=self.driverPage, **button_style
        )
        self.driver_button.grid(row=1, column=0, pady=5)

        self.admin_button = tk.Button(
            self.button_frame, text="Admin Dashboard", command=self.adminLogin, **button_style
        )
        self.admin_button.grid(row=2, column=0, pady=5)

        self.footer = tk.Label(
            self.root,
            text="© 2024 Taxi Booking System",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#888888"
        )
        self.footer.pack(side="bottom", pady=10)
    def customerPage(self):
        try:
            open_customer_registration()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Customer Page: {e}")
    def driverPage(self):
        try:
            open_driver_page()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Driver Page: {e}")
    def adminPage(self):
        try:
            open_admin_page()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening admin dashboard: {e}")
    def validateCredentials(self, username, password):
        try:
            with open("admin_credentials.txt", "r") as file:
                for line in file:
                    StoredUsername, StoredPassword = line.strip().split(":")
                    if username == StoredUsername and password == StoredPassword:
                        return True
            return False
        except FileNotFoundError:
            messagebox.showerror("Error", "Credentials file not found.")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error reading credentials file: {e}")
            return False
    def adminLogin(self):
        username = simpledialog.askstring("Admin login", "Enter username:")
        password = simpledialog.askstring("Admin login", "Enter password:", show="**")
        if username and password:
            if self.validateCredentials(username, password):
                messagebox.showinfo("Login successful", "Welcome to the Admin Dashboard!")
                self.adminPage()
            else:
                messagebox.showerror("Login failed", "Invalid username/password.")
        else:
            messagebox.showwarning("Input error", "Username & password cannot be empty.")
if __name__ == "__main__":
    root = tk.Tk()
    app = taxiBookingSystem(root)
    root.mainloop()