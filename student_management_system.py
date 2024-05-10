from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

# Global variable to store student details in the Admin Panel
student_details = []
student_id_counter = 1  # Initialize a counter for student IDs
student_id_entry = None  # Initialize student_id_entry as a global variable

# Function to create the Admin Panel window
def create_admin_panel():
    def display_student_details():
        student_list_window = Tk()
        student_list_window.geometry('800x600')
        student_list_window.title('Student List')

        # Create a Treeview widget to display student details with a modern look
        style = ttk.Style()
        style.configure("Treeview", font=('Nexa', 15), rowheight=30, background='#E1F2FE')
        style.configure("Treeview.Heading", font=('Nexa', 15, 'bold'), background='#195905', foreground='white')

        tree = ttk.Treeview(student_list_window, columns=("Student ID", "Name", "Gmail ID", "Phone No."), show="headings")
        tree.heading("Student ID", text="Student ID")
        tree.heading("Name", text="Name")
        tree.heading("Gmail ID", text="Gmail ID")
        tree.heading("Phone No.", text="Phone No.")
        tree.pack(fill=BOTH, expand=True)

        # Connect to the MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="Akash",
            password="Akash700377@",
            database="student_management"
        )

        cursor = db.cursor()

        # Fetch student data from the 'students' table
        cursor.execute("SELECT * FROM students")
        student_data = cursor.fetchall()

        # Populate the Treeview with student data
        for student in student_data:
            tree.insert("", "end", values=student)

        # Close the database connection
        cursor.close()
        db.close()

    def search_students():
        global student_id_entry  # Define student_id_entry as a global variable
        student_id_to_search = student_id_entry.get()  # Get the Student ID from the user input
        if not student_id_to_search.isdigit():
            messagebox.showerror('Invalid Input', 'Please enter a valid Student ID (integer).')
            return

        student_list_window = Tk()
        student_list_window.geometry('800x600')
        student_list_window.title('Search Student')

        # Create a Treeview widget to display student details with a modern look
        style = ttk.Style()
        style.configure("Treeview", font=('Nexa', 15), rowheight=30, background='#E1F2FE')
        style.configure("Treeview.Heading", font=('Nexa', 15, 'bold'), background='#195905', foreground='white')

        tree = ttk.Treeview(student_list_window, columns=("Student ID", "Name", "Gmail ID", "Phone No."), show="headings")
        tree.heading("Student ID", text="Student ID")
        tree.heading("Name", text="Name")
        tree.heading("Gmail ID", text="Gmail ID")
        tree.heading("Phone No.", text="Phone No.")
        tree.pack(fill=BOTH, expand=True)

        # Connect to the MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="Akash",
            password="Akash700377@",
            database="student_management"
        )

        cursor = db.cursor()

        # Fetch student data from the 'students' table based on the provided Student ID
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id_to_search,))
        student_data = cursor.fetchall()

        if not student_data:
            messagebox.showinfo('No Match', f'No student found with Student ID {student_id_to_search}.')
            student_list_window.destroy()
            return

        # Populate the Treeview with student data
        for student in student_data:
            tree.insert("", "end", values=student)

        # Close the database connection
        cursor.close()
        db.close()

    def close_admin_panel():
        admin_panel.destroy()

    admin_panel = Tk()
    admin_panel.geometry('1280x720')
    admin_panel.config(bg="light green")
    admin_panel.title('Admin Panel')

    # Heading Label
    Label(admin_panel, text='Admin Panel', font='Nexa 20 bold', bg='yellow', fg='black').pack(fill=X, pady=20)

    # Buttons in Admin Panel
    admin_buttons = [
        ('Students List', display_student_details),
        ('Search Students', search_students),  # Added "Search Students" button
        ('Edit Details', None),  # Placeholder for Edit Details function
        ('Remove', None),  # Placeholder for Remove function
        ('Close', close_admin_panel),  # 'Close' button with close_admin_panel function
    ]

    for button_text, command in admin_buttons:
        if callable(command):
            button = Button(admin_panel, text=button_text, font='Nexa 15 bold', width=20, height=2, bg='#195905', fg='white', command=command)
        else:
            button = Button(admin_panel, text=button_text, font='Nexa 15 bold', width=20, height=2, bg='#195905', fg='white')
        button.pack(pady=10)
        

# Function to create the Student Panel window
def create_student_panel():
    def submit_details():
        global student_id_counter
        student_data = [entry_var.get() for entry_var in entry_vars]

        # Connect to the MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="Akash",
            password="Akash700377@",
            database="student_management"
        )

        cursor = db.cursor()

        # Insert the student data into the 'students' table
        sql = "INSERT INTO students (first_name, last_name, gmail_id, phone_no) VALUES (%s, %s, %s, %s)"
        values = (student_data[0], student_data[1], student_data[2], student_data[3])

        cursor.execute(sql, values)
        db.commit()

        messagebox.showinfo('Submission Successful', 'Student details submitted successfully.\nStudent ID: {}'.format(student_id_counter))
        student_id_counter += 1
        for entry_var in entry_vars:
            entry_var.delete(0, END)

        # Close the database connection
        cursor.close()
        db.close()

    student_panel = Tk()
    student_panel.geometry('1280x720')
    student_panel.config(bg="light green")
    student_panel.title('Student Panel')

    # Heading Label
    Label(student_panel, text='Student Panel', font='Nexa 20 bold', bg='yellow', fg='black').pack(fill=X, pady=20)

    # User Input Fields
    fields = ['First Name', 'Last Name', 'Gmail ID', 'Phone No.']
    entry_vars = []

    for field in fields:
        Label(student_panel, text=field + ':', font='Nexa 15 bold', fg='black').pack(pady=10)
        entry_var = Entry(student_panel, font='Nexa 15')
        entry_var.pack(pady=10)
        entry_vars.append(entry_var)

    # Submit Button
    submit_button = Button(student_panel, text='Submit', font='Nexa 15 bold', width=15, height=2, bg='#195905', fg='white', command=submit_details)
    submit_button.pack(pady=10)

    # Log Out Button
    logout_button = Button(student_panel, text='Log Out', font='Nexa 15 bold', width=15, height=2, bg='#ff0000', fg='white', command=student_panel.destroy)
    logout_button.pack(pady=10)

# Function to open the Admin login page
def open_admin_login():
    create_login_page('Admin', 'Admin', create_admin_panel)

# Function to open the User login page
def open_user_login():
    create_login_page('User', 'User', create_student_panel)

# Function to create a login window
def create_login_page(username, password, success_callback):
    login_window = Tk()
    login_window.geometry('350x450')
    login_window.config(bg="light green")
    login_window.title('Login')

    # Heading Label
    Label(login_window, text='Login', font='Nexa 20 bold', bg='yellow', fg='black').pack(fill=X, pady=20)

    # Username Label and Entry
    Label(login_window, text='Username:', font='Nexa 15 bold', fg='black').pack(pady=10)
    username_entry = Entry(login_window, font='Nexa 15')
    username_entry.pack(pady=10)
    username_entry.insert(0, username)  # Set the default username

    # Password Label and Entry
    Label(login_window, text='Password:', font='Nexa 15 bold', fg='black').pack(pady=10)
    password_entry = Entry(login_window, font='Nexa 15', show='*')
    password_entry.pack(pady=10)
    password_entry.insert(0, password)  # Set the default password

    # Login Button
    def check_login():
        entered_username = username_entry.get()
        entered_password = password_entry.get()
        if entered_username == username and entered_password == password:
            messagebox.showinfo('Login Successful', f'Welcome, {entered_username}!')
            login_window.destroy()
            success_callback()  # Call the appropriate callback function after successful login
        else:
            messagebox.showerror('Login Failed', 'Invalid username or password')

    login_button = Button(login_window, text='Login', font='Nexa 15 bold', width=15, height=2, bg='#195905', fg='white', command=check_login)
    login_button.pack(pady=10)

    # Close Button
    close_button = Button(login_window, text='Close', font='Nexa 15 bold', width=15, height=2, bg='#ff0000', fg='white', command=login_window.destroy)
    close_button.pack(pady=10)

# Create the main window
window = Tk()
window.geometry('1280x720')
window.state('zoomed')
window.config(bg="light green")
window.title('Student Management System')

# Heading Label
Label(window, text='Student Management System', font='Nexa 20 bold', bg='yellow', fg='black').pack(fill=X, pady=20)

# Middle Label
lable_frame = LabelFrame(window, text='Menu', font='Nexa 20 bold', width=222, height=203, bg='yellow', fg='black')
lable_frame.place(x=685, y=330)

# Admin Button
admin_button = Button(window, text='Admin', font='Nexa 15 bold', width=15, height=2, bg='#195905', fg='white', command=open_admin_login)
admin_button.pack(pady=10)
admin_button.place(x=700, y=370)

# User Button
user_button = Button(window, text='User', font='Nexa 15 bold', width=15, height=2, bg='#195905', fg='white', command=open_user_login)
user_button.pack(pady=10)
user_button.place(x=700, y=450)

mainloop()

