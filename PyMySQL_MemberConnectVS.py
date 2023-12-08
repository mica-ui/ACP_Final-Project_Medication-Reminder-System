from tkcalendar import DateEntry
from tkinter import *
from tkinter import ttk  # Add this line to import ttk
import tkinter.messagebox
import pymysql


class MedicationConnect:

    def __init__(self, root):
        self.root = root
        blankSpace = " "
        self.root.title(202 * blankSpace + "MySql Database Connector")
        self.root.resizable(width=False, height=False)
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

        MainFrame = Frame(self.root, bd=10, width=1350, height=680, relief=RIDGE, bg='lightblue')
        MainFrame.grid()
        TitleFrames = Frame(MainFrame, bd=7, width=1320, height=100, relief=RIDGE)
        TitleFrames.grid(row=0, column=0)

        TitleFrame = Frame(TitleFrames, bd=7, width=1320, height=100, relief=RIDGE, bg='lightblue')
        TitleFrame.grid(row=0, column=0)

        SearchFrames = Frame(MainFrame, bd=5, width=1320, height=50, relief=RIDGE)
        SearchFrames.grid(row=1, column=0)

        MidFrame = Frame(MainFrame, bd=5, width=1340, height=500, bg="lightblue", relief=RIDGE)
        MidFrame.grid(row=3, column=0)

        InnerFrame = Frame(MidFrame, bd=5, width=1340, height=180, padx=24, pady=4, relief=RIDGE)
        InnerFrame.grid(row=0, column=0)
        ButtonFrame = Frame(MidFrame, bd=7, width=1340, height=50, bg="lightblue", relief=RIDGE)
        ButtonFrame.grid(row=1, column=0)
        TreeviewFrame = Frame(MidFrame, bd=5, width=1340, height=400, padx=4, relief=RIDGE)
        TreeviewFrame.grid(row=2, column=0, padx=5, pady=0)

        # ========================================================================================================
        self.lblInformation = Label(TitleFrames, font=('Microsoft YaHei UI Light', 40, 'bold'), text="Medicine Log", bg="lightblue", fg="black")
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
                sqlCon = pymysql.connect(host="localhost", user="root", password="SEPTEMBER_82004", database="medicationlog")
                cur = sqlCon.cursor()
                cur.execute("INSERT INTO medicationlog (dosage, medication, unit, date, time, dose) VALUES (%s, %s, %s, %s, %s, %s)",(Dosage.get(), Med_name.get(), Unit.get(), Date.get(), Time.get(), Dose.get()))

                sqlCon.commit()
                showRecord()
                sqlCon.close()
                tkinter.messagebox.showinfo("Data Entry Form", "Record Entered Successfully")

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

            if row and len(row) >= 6:
                Dosage.set(row[0])
                Med_name.set(row[1])
                Unit.set(row[2])
                Date.set(row[3])
                Time.set(row[4])
                Dose.set(row[5])
            else:
                print("Not enough elements in the 'row' list or row is empty.")

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
        self.btnSearch = Button(SearchFrames, pady=1, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Search", width=9, height=1,bg='lightblue', command=searchDB)
        self.btnSearch.grid(row=0, column=3, padx=1)

        # ========================================================================================================
        self.btnAddNew = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Add New", width=16, height=1,bg='lightblue', command=addNew)
        self.btnAddNew.grid(row=0, column=0, padx=1)
        self.btnShowRecord = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Show Record", width=11,height=1, bg='lightblue', command=showRecord)
        self.btnShowRecord.grid(row=0, column=1, padx=1)
        self.btnUpdate = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Update", width=16, height=1,bg='lightblue', command=update)
        self.btnUpdate.grid(row=0, column=2, padx=1)
        self.btnDelete = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Delete", width=16, height=1,bg='lightblue', command=deleteDB)
        self.btnDelete.grid(row=0, column=3, padx=1)
        self.btnReset = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Reset", width=16, height=1,bg='lightblue', command=Reset)
        self.btnReset.grid(row=0, column=4, padx=1)
        self.btnExit = Button(ButtonFrame, pady=2, bd=4, font=('Microsoft YaHei UI Light', 12, 'bold'), text="Exit", width=15, height=1,bg='lightblue', command=iExit)
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
        
if __name__ == '__main__':
    root = Tk()
    application = MedicationConnect(root)
    root.mainloop()