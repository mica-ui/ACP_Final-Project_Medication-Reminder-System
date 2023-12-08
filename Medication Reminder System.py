from tkinter import *
from tkinter import messagebox
import json

USER_DATA_FILE = "user_data.json"

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def create_common_design(parent, title):

    # Design elements for both Sign In and Sign Up pages
    Label(parent, image=img, bg='white').place(x=0, y=10)

    frame = Frame(parent, width=350, height=350, bg="white")
    frame.place(x=480, y=70)

    heading = Label(frame, text=title, fg='#355E3B', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)

    def on_enter(e):
        entry = e.widget
        entry.delete(0, "end")

    def on_leave(e):
        entry = e.widget
        name = entry.get()
        if name == '':
            entry.insert(0, entry.placeholder)

    user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)
    user.placeholder = 'Username'

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11), show='*')
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)
    code.placeholder = 'Password'

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    return frame, user, code

def validate_password(password):
    # Check if the password length is exactly 6 characters
    return len(password) == 6

def signin():
    # Code for the Sign In functionality
    username = user.get()
    password = code.get()

    user_data = load_user_data()

    # Check if the username and password match
    if username in user_data and user_data[username] == password:
        messagebox.showinfo('Success', 'Login successful!')
        root.destroy()
        
        # Add code to navigate to the home page after successful login
    else:
        messagebox.showerror('Error', 'Invalid username or password.')

def signup():
    # Code for the Sign Up functionality
    username = user.get()
    password = code.get()

    # Validate the password length
    if not validate_password(password):
        messagebox.showerror('Error', 'Password must be exactly 6 characters long.')
        return

    user_data = load_user_data()

    # Check if the username already exists
    if username in user_data:
        messagebox.showerror('Error', 'Username already exists. Choose a different username.')
    else:
        # Save the new user data
        user_data[username] = password
        save_user_data(user_data)
        messagebox.showinfo('Success', 'Account created successfully!')

def create_signup_widget():
    # Code for creating the Sign Up widget with the same geometry as the Log In widget
    signup_widget = Toplevel(root)
    signup_widget.title("Sign Up")
    signup_widget.geometry('925x500+300+200')  # Set the same geometry as Log In
    signup_widget.config(bg="white")

    frame, user, code = create_common_design(signup_widget, "Sign Up")

    def signup_new_user():
        # Code for signing up a new user
        new_username = user.get()
        new_password = code.get()

        # Validate the password length
        if not validate_password(new_password):
            messagebox.showerror('Error', 'Password must be exactly 6 characters long.')
            return

        user_data = load_user_data()

        # Check if the new username already exists
        if new_username in user_data:
            messagebox.showerror('Error', 'Username already exists. Choose a different username.')
        else:
            # Save the new user data
            user_data[new_username] = new_password
            save_user_data(user_data)
            messagebox.showinfo('Success', 'Account created successfully!')

    # Create a button to sign up the new user
    signup_button = Button(frame, width=39, pady=7, text='Sign Up', command=signup_new_user, bg='#50C878', fg='white', border=0)
    signup_button.place(x=35, y=204)

# Main application window
root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

# Assuming you have an image named 'img'
img = PhotoImage(file=r'C:\Users\elizabeth macalindol\Downloads\medicare.png')

# Create the common design for Sign In
frame, user, code = create_common_design(root, "Log In")

# Button for Sign In
Button(frame, width=39, pady=7, text='Sign in', bg='#50C878', fg='white', border=0, command=signin).place(x=35, y=204)

# Label for Sign Up
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)

# Button for opening the Sign Up widget
sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#50C878', command=create_signup_widget)
sign_up.place(x=215, y=270)


# Start the Tkinter main loop
root.mainloop()

#=============================================================================================================================================
import tkinter as tk
from tkinter import RIDGE, messagebox
import datetime
import time
from plyer import notification
from tkcalendar import DateEntry
from tkinter import *
from tkinter import ttk  # Add this line to import ttk
import tkinter.messagebox
import pymysql
from PIL import Image, ImageTk

medication_data = []
root =tk.Tk() 
open_database_connector = ()

# Load the logo image
logo_path = r'C:\Users\elizabeth macalindol\Downloads\medicare.png'
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((200, 200), resample=Image.LANCZOS)

  # Resize the logo as needed

# Convert the logo image to Tkinter PhotoImage
logo_photo = ImageTk.PhotoImage(logo_image)

# Create a label for the logo
logo_label = tk.Label(root, image=logo_photo, bg='white')
logo_label.image = logo_photo  # Keep a reference to prevent the image from being garbage collected
logo_label.pack()


def clear_entries():
    medicine_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    pill_count_entry.delete(0, tk.END)
    unit_entry.delete(0, tk.END)
    dose_entry.delete(0, tk.END)

def show_notification(reminder_text, target_time):
    def notify():
        notification_title = "MediTime Reminder"
        notification_text = f"{reminder_text}"
        notification.notify(
            title=notification_title,
            message=notification_text,
            timeout=10  # Set the notification display time (in seconds)
        )

    def check_time():
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        if current_time == target_time:
            notify()
        else:
            root.after(1000, check_time)  # Check again in 1 second

    # Start checking for the target time
    check_time()

def check_medication_reminders():
    current_time = time.strftime("%H:%M")
    
    for item in medication_data:
        if current_time == item['time']:
            reminder_text = f"It's pill o'clock, {item['medicine']}, {item['time']}, take {item['pill_count']} pill(s) only"
            show_notification(reminder_text, item['time'])
            # Remove the medication reminder after notifying
            medication_data.remove(item)
            update_display()
            # Schedule the next check after a delay (adjust as needed)
    notification_delay = 10  # 10 seconds for testing, change as needed
    root.after(notification_delay * 1000, check_medication_reminders)

# Initialize the medication reminder checker
check_medication_reminders()

def add_medication():
    medicine = medicine_entry.get()
    time_val = time_entry.get()
    pill_count = pill_count_entry.get()
    unit = unit_entry.get()
    dose = dose_entry.get()
    date = date_cal.get_date()

    if medicine and time_val and pill_count and unit and dose:
        try:
            input_time = datetime.datetime.strptime(time_val, "%I:%M %p")
            target_time = input_time.strftime("%I:%M %p")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM AM/PM.")
            return

        reminder_text = f"It's pill o'clock, {medicine}, {time_val}, take {pill_count} {unit}(s) of {dose} only"
        display_medication({'medicine': medicine, 'time': target_time, 'pill_count': pill_count, 'unit': unit, 'dose': dose, 'date': date}, len(medication_data))
        medication_data.append({'medicine': medicine, 'time': target_time, 'pill_count': pill_count, 'unit': unit, 'dose': dose, 'date': date})

        # Insert into the database
        try:
            sqlCon = pymysql.connect(host="localhost", user="root", password="SEPTEMBER_82004", database="medicationlog")
            cur = sqlCon.cursor()
            cur.execute("INSERT INTO medicationlog (dosage, medication, unit, date, time, dose) VALUES (%s, %s, %s, %s, %s, %s)",
                        (dose, medicine, unit, date, time_val, pill_count))
            sqlCon.commit()
            sqlCon.close()
            tkinter.messagebox.showinfo("Data Entry Form", "Record Entered Successfully")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            tkinter.messagebox.showerror("Error", f"An error occurred: {str(e)}")

        clear_entries()
        show_notification(reminder_text, target_time)
    else:
        messagebox.showerror("Error", "Please fill in all fields.")



def open_database_connector():
    # Function to open the database connector window
    database_window = Toplevel(root)
    MedicationConnect(database_window)

class MedicationConnect:

    def __init__(self, root):
        self.root = root
        blankSpace = " "
        self.root.title(202 * blankSpace + "MySql Database Connector")
        self.root.geometry("1360x700+0+0")

        # ========================================================================================================

        Med_name = StringVar()
        Unit = StringVar()
        Date = StringVar()
        Time = StringVar()
        Dose = StringVar()

        Search = StringVar()
        Dosage = StringVar()
        # ========================================================================================================
        def iExit():
            if tkinter.messagebox.askyesno("Connector System", "Confirm if you want to exit"):
                root.destroy()

        # ========================================================================================================
        def Reset():
            Med_name.set('')
            Unit.set('')
            Date.set('')
            Time.set('')
            Dose.set('')
            Search.set('')
            Dosage.set('')
        
        # ========================================================================================================

        MainFrame = Frame(self.root, bd=15, width=1370, height=1000, relief=RIDGE, bg='lightgreen')
        MainFrame.grid()
        
        TitleFrames = Frame(MainFrame, bd=7, width=1320, height=100, relief=RIDGE)
        TitleFrames.grid(row=0, column=0)

        TitleFrame = Frame(TitleFrames, bd=7, width=1320, height=100, relief=RIDGE, bg='lightgreen')
        TitleFrame.grid(row=0, column=0)

        SearchFrames = Frame(MainFrame, bd=5, width=1320, height=50, relief=RIDGE)
        SearchFrames.grid(row=1, column=0)

        MidFrame = Frame(MainFrame, bd=5, width=1340, height=500, bg="lightgreen", relief=RIDGE)
        MidFrame.grid(row=3, column=0)

        InnerFrame = Frame(MidFrame, bd=5, width=1340, height=180, padx=24, pady=4, relief=RIDGE)
        InnerFrame.grid(row=0, column=0)
        ButtonFrame = Frame(MidFrame, bd=7, width=1340, height=50, bg="lightgreen", relief=RIDGE)
        ButtonFrame.grid(row=1, column=0)
        TreeviewFrame = Frame(MidFrame, bd=5, width=1340, height=400, padx=4, relief=RIDGE)
        TreeviewFrame.grid(row=2, column=0, padx=5, pady=0)

        # ========================================================================================================
        self.lblInformation = Label(TitleFrames, font=('Microsoft YaHei UI Light', 40, 'bold'), text="Medicine Log", bg="lightgreen", fg="black")
        self.lblInformation.grid(row=0, column=0, padx=152)
        # ========================================================================================================
        
        # ========================================================================================================
        self.lblDosage = Label(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Dosage", bd=7)
        self.lblDosage.grid(row=0, column=0, padx=5, sticky=W)
        self.txtDosage = Entry(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), bd=5, width=35, textvariable=Dosage, justify='left')
        self.txtDosage.grid(row=0, column=1)

        self.lblMedication = Label(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Medication", bd=7)
        self.lblMedication.grid(row=1, column=0, padx=5, sticky=W)
        self.txtMedication = Entry(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), bd=5, width=35, textvariable=Med_name,justify='left')
        self.txtMedication.grid(row=1, column=1)

        self.lblUnit = Label(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Unit", bd=7)
        self.lblUnit.grid(row=2, column=0, padx=5, sticky=W)
        self.txtUnit = Entry(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), bd=5, width=35, textvariable=Unit, justify='left')
        self.txtUnit.grid(row=2, column=1)

        self.lblDate = Label(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Date", bd=7)
        self.lblDate.grid(row=0, column=2, sticky=W, padx=5)
        # Replace the Entry widget with DateEntry widget
        self.txtDate = DateEntry(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), bd=5, width=35, textvariable=Date, justify='left', background='lightgreen', foreground='white')
        self.txtDate.grid(row=0, column=3)

        self.lblTime = Label(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Time", bd=7)
        self.lblTime.grid(row=1, column=2, sticky=W, padx=5)
        self.txtTime = Entry(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), bd=5, width=35, textvariable=Time, justify='left')
        self.txtTime.grid(row=1, column=3)

        self.lblDose = Label(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Dose", bd=7)
        self.lblDose.grid(row=2, column=2, sticky=W, padx=5)
        self.txtDose = Entry(InnerFrame, font=('Microsoft YaHei UI Light', 12, 'bold'), bd=5, width=35, textvariable=Dose, justify='left')
        self.txtDose.grid(row=2, column=3)
        self.cboDose = ttk.Combobox(InnerFrame, width=33, font=('Microsoft YaHei UI Light', 12, 'bold'), state='readonly', textvariable=Dose)

        self.cboDose['values'] = ('', '1', '2', '3', '4', '5')
        self.cboDose.current(0)
        self.cboDose.grid(row=2, column=3)
        # ========================================================================================================
        def addNew():
            if Dosage.get() == "" or Med_name.get() == "" or Unit.get() == "":
                tkinter.messagebox.showerror("Error", "Please fill in all the fields")
            else:
                try:
                    sqlCon = pymysql.connect(host="localhost", user="root", password="SEPTEMBER_82004", database="medicationlog")
                    cur = sqlCon.cursor()
                    cur.execute("INSERT INTO medicationlog (dosage, medication, unit, date, time, dose) VALUES (%s, %s, %s, %s, %s, %s)", (Dosage.get(), Med_name.get(), Unit.get(), Date.get(), Time.get(), Dose.get()))

                    # Add the following line to commit the changes to the database
                    sqlCon.commit()

                    showRecord()
                    sqlCon.close()
                    tkinter.messagebox.showinfo("Data Entry Form", "Record Entered Successfully")
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    tkinter.messagebox.showerror("Error", f"An error occurred: {str(e)}")



        def showRecord():
            sqlCon =pymysql.connect(host="localhost", user="root", password="SEPTEMBER_82004", database="medicationlog")
            cur = sqlCon.cursor()
            cur.execute("SELECT * FROM medicationlog")
            result = cur.fetchall()
            if len(result) != 0:
                self.medication_records.delete(*self.medication_records.get_children())
                for row in result:
                    self.medication_records.insert('', END, values=row)
                sqlCon.commit()
            sqlCon.close()

        def MedicationInfo(event):
            viewInfo = self.medication_records.focus()
            learnerData = self.medication_records.item(viewInfo)
            row = learnerData['values']

            if len(row) >= 6:  # Check if there are at least 6 elements in the list
                Dosage.set(row[0])
                Med_name.set(row[1])
                Unit.set(row[2])
                Date.set(row[3])
                Time.set(row[4])
                Dose.set(row[5])
            else:
    # Handle the case when the list doesn't have enough elements
                print("Not enough elements in the 'row' list.")


        def update():
            sqlCon = pymysql.connect(host="localhost", user="root", password="SEPTEMBER_82004", database="medicationlog")
            cur = sqlCon.cursor()
            cur.execute("UPDATE medicationlog SET dosage=%s, medication=%s, unit=%s, date=%s, time=%s, dose=%s WHERE medication=%s",(Dosage.get(), Med_name.get(), Unit.get(), Date.get(), Time.get(), Dose.get(), Med_name.get()))

            sqlCon.commit()
            showRecord()
            sqlCon.close()
            tkinter.messagebox.showinfo("Data Entry Form", "Record Successfully Updated")

        def deleteDB():
            sqlCon = pymysql.connect(host="localhost", user="root", password="SEPTEMBER_82004", database="medicationlog")
            cur = sqlCon.cursor()
            cur.execute("DELETE FROM medicationlog WHERE medication='%s'" % (Med_name.get()))
            sqlCon.commit()
            showRecord()
            sqlCon.close()
            tkinter.messagebox.showinfo("Delete Data", "Successfully Deleted Record")
            Reset()
        # ========================================================================================================
        def searchDB():
            try:
                sqlCon = pymysql.connect(host="localhost", user="root", password="SEPTEMBER_82004", database="medicationlog")
                cur = sqlCon.cursor()
                cur.execute("SELECT * FROM medicationlog WHERE medication LIKE %s", ("%" + Search.get() + "%",))

                row = cur.fetchone()

                Dosage.set(row[0])
                Med_name.set(row[1])
                Unit.set(row[2])
                Date.set(row[3])
                Time.set(row[4])
                Dose.set(row[5])

                sqlCon.commit()
            except:
                tkinter.messagebox.showinfo("Data Entry Form", "No Such Record Found")
                Search.set("")

            sqlCon.close()
        # ========================================================================================================
        self.txtSearch = Entry(SearchFrames, font=('Microsoft YaHei UI Light', 13), width=26, textvariable=Search, justify='center')
        self.txtSearch.grid(row=0, column=2)
        self.btnSearch = Button(SearchFrames, pady=1, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Search", width=9, height=1,bg='lightgreen', command=searchDB)
        self.btnSearch.grid(row=0, column=3, padx=1)

        # ========================================================================================================
        self.btnAddNew = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Add New", width=16, height=1,bg='lightgreen', command=addNew)
        self.btnAddNew.grid(row=0, column=0, padx=1)
        self.btnShowRecord = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Show Record", width=11,height=1, bg='lightgreen', command=showRecord)
        self.btnShowRecord.grid(row=0, column=1, padx=1)
        self.btnUpdate = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Update", width=16, height=1,bg='lightgreen', command=update)
        self.btnUpdate.grid(row=0, column=2, padx=1)
        self.btnDelete = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Delete", width=16, height=1,bg='lightgreen', command=deleteDB)
        self.btnDelete.grid(row=0, column=3, padx=1)
        self.btnReset = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Reset", width=16, height=1,bg='lightgreen', command=Reset)
        self.btnReset.grid(row=0, column=4, padx=1)
        self.btnExit = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Exit", width=15, height=1,bg='lightgreen', command=iExit)
        self.btnExit.grid(row=0, column=5, padx=1)

        # ========================================================================================================
        scroll_y = Scrollbar(TreeviewFrame, orient=VERTICAL)

        self.medication_records = ttk.Treeview(TreeviewFrame, height=15,columns=("Dosage", "Medication", "Unit", "Date", "Time", "Dose"),yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.medication_records.heading("Dosage", text="Dosage")
        self.medication_records.heading("Medication", text="Medication")
        self.medication_records.heading("Unit", text="Unit")
        self.medication_records.heading("Date", text="Date")
        self.medication_records.heading("Time", text="Time")
        self.medication_records.heading("Dose", text="Dose")

        self.medication_records['show'] = 'headings'

        self.medication_records.column("Dosage", width=210)
        self.medication_records.column("Medication", width=210)
        self.medication_records.column("Unit", width=210)
        self.medication_records.column("Date", width=210)
        self.medication_records.column("Time", width=210)
        self.medication_records.column("Dose", width=210)

        self.medication_records.pack(fill=BOTH, expand=1)
        self.medication_records.bind("<ButtonRelease-1>", MedicationInfo)

        showRecord()

# ========================================================================================================

def display_medication(item, index):
    reminder_text = (
        f"It's pill o'clock, {item['medicine']}, {item['time']}, "
        f"take {item['pill_count']} pill(s) only, "
        f"Date: {item.get('date', 'N/A')}, Unit: {item.get('unit', 'N/A')}, Dose: {item.get('dose', 'N/A')}"
    )
    delete_button = tk.Button(home_display, text="Delete", command=lambda i=index: delete_medication(i), bg='#50C878')
    edit_button = tk.Button(home_display, text="Edit", command=lambda i=index: edit_medication(i), bg="#FFFFFF")
    home_display.insert(tk.END, reminder_text + " ...")
    home_display.window_create(tk.END, window=delete_button)
    home_display.window_create(tk.END, window=edit_button)
    home_display.insert(tk.END, "\n")

def update_display():
    home_display.delete(1.0, tk.END)
    for i, item in enumerate(medication_data):
        display_medication(item, i)

def delete_medication(index):
    medication_data.pop(index)
    update_display()
    clear_entries()  # Clear the entry fields after deleting

def edit_medication(index):
    try:
        item = medication_data[index]
    except IndexError:
        print(f"Error: Index {index} is out of bounds.")
        return

    clear_entries()
    medicine_entry.insert(0, item.get('medicine', ''))
    time_entry.insert(0, item.get('time', ''))
    pill_count_entry.insert(0, item.get('pill_count', ''))
    unit_entry.insert(0, item.get('unit', ''))
    dose_entry.insert(0, item.get('dose', ''))

    # Check for 'date' key in item
    date_value = item.get('date', '')
    if date_value and isinstance(date_value, str):
        try:
            date_cal.set_date(datetime.datetime.strptime(date_value, "%Y-%m-%d").date())
        except ValueError:
            print(f"Error: Invalid date format in item {item}")

    # Mark the item for editing
    item['_edit'] = True
    update_display()

root.title("MediTime")
root.geometry('925x500+300+200')
root.configure(bg="#fff")


# Set the background color
root.configure(bg='#FFFFFF')
# Define fonts and font size
large_font = ('Microsoft YaHei UI Light', 20, 'bold')
medium_font = ('Microsoft YaHei UI Light', 14)
label_font = ('Microsoft YaHei UI Light', 14)
entry_font = ('Microsoft YaHei UI Light', 14)
button_font = ('Microsoft YaHei UI Light', 14, 'bold')


# Create a frame for the "Add Your Medicine" button
button_frame = tk.Frame(root, bg='#FFFFFF')
button_frame.pack()


# Create a frame for centering the "Add Your Medicine" button
center_frame = tk.Frame(root, bg='#FFFFFF')
center_frame.pack(expand=True)

# Set button size
button1 = tk.Button(center_frame, bd=2, relief=RIDGE, text="Add Your Medicine", width=20, command=add_medication, font=button_font, bg='lightgreen')
button1.grid(row=0, column=0, padx=10, pady=10)

# Create a new button to open the database connector
database_button = tk.Button(center_frame, bd=2, relief=RIDGE, text="Open Database", width=20, command=open_database_connector, font=button_font, bg='lightgreen')
database_button.grid(row=0, column=1, padx=10, pady=10)


medicine_label = tk.Label(button_frame, text="Medicine:", font=label_font, bg='#FFFFFF')
medicine_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')  # Align to the west (left) within the cell
medicine_entry = tk.Entry(button_frame, bd=2, relief=RIDGE, bg='#FFFFFF', font=entry_font)
medicine_entry.grid(row=1, column=1, padx=10, pady=10, sticky='e')  # Align to the east (right) within the cell

pill_count_label = tk.Label(button_frame, text="Dose", font=label_font, bg='#FFFFFF')
pill_count_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')  # Align to the west (left) within the cell
pill_count_entry = tk.Entry(button_frame, bd=2, relief=RIDGE, bg='#FFFFFF', font=entry_font)
pill_count_entry.grid(row=2, column=1, padx=10, pady=10, sticky='e')  # Align to the east (right) within the cell

time_label = tk.Label(button_frame, text="Time:", font=label_font, bg='#FFFFFF')
time_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')  # Align to the west (left) within the cell
time_entry = tk.Entry(button_frame, bd=2, relief=RIDGE, bg='#FFFFFF', font=entry_font)
time_entry.grid(row=3, column=1, padx=10, pady=10, sticky='e')  # Align to the east (right) within the cell

date_label = tk.Label(button_frame, text="Date:", font=label_font, bg='#FFFFFF')
date_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')  # Align to the west (left) within the cell
date_entry = tk.Entry(button_frame, bd=2, relief=RIDGE, bg='#FFFFFF', font=entry_font)
date_cal = DateEntry(button_frame, bd=2, relief=RIDGE, bg='#FFFFFF', font=entry_font, background='#50C878', foreground='white', borderwidth=2, showweeknumbers=False)
date_cal.grid(row=4, column=1, padx=10, pady=10, sticky='w')  # Align to the east (right) within the cell

unit_label = tk.Label(button_frame, text="Unit:", bg='#FFFFFF', font=label_font)
unit_label.grid(row=5, column=0, padx=10, pady=10, sticky='w')  # Align to the west (left) within the cell
unit_entry = tk.Entry(button_frame, bd=2, relief=RIDGE, bg='#FFFFFF', font=entry_font)
unit_entry.grid(row=5, column=1, padx=10, pady=10, sticky='e')  # Align to the east (right) within the cell

dose_label = tk.Label(button_frame, text="Dosage:", bg='#FFFFFF', font=label_font)
dose_label.grid(row=6, column=0, padx=10, pady=10, sticky='w')  # Align to the west (left) within the cell
dose_entry = tk.Entry(button_frame, bd=2, relief=RIDGE, bg='#FFFFFF', font=entry_font)
dose_entry.grid(row=6, column=1, padx=10, pady=10, sticky='e' )  # Align to the east (right) within the cell

# Add padding around the text widget
home_display = tk.Text(root,bd=5, relief=RIDGE, bg='#FFFFFF', width=130, height=200)
home_display.pack(padx=30, pady=30)  # Adjust the padx and pady values as needed


# Start the Tkinter main loop
root.mainloop()

#========================================================================================================================