import sqlite3
from tkinter import *
from tkinter import messagebox


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("Test.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS angajat (id INTEGER PRIMARY KEY, nume TEXT, prenume TEXT, salar INTEGER, CNP INTEGER)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM angajat")
        rows = self.cur.fetchall()
        return rows

    def insert(self, nume, prenume, salar, CNP):
        self.cur.execute("INSERT INTO angajat VALUES (NULL,?,?,?,?)", (nume, prenume, salar, CNP))
        self.conn.commit()
        self.view()

    def update(self, id, nume, prenume, salar, CNP):
        self.cur.execute("UPDATE angajat SET nume=?, prenume=?, salar=?, CNP=? WHERE id=?", (nume, prenume, salar, CNP, id))
        self.view()

    def delete(self, id):
        self.cur.execute("DELETE FROM angajat WHERE id=?", (id,))
        self.conn.commit()
        self.view()

    '''def search(self, nume="", prenume="", salar="", CNP=""):
        self.cur.execute("SELECT * FROM angajat WHERE nume=? OR prenume=? OR salar=?" "OR CNP=?", (nume, prenume, salar, CNP))
        rows = self.cur.fetchall()
        return rows'''
    def scade(self):
        self.cur.execute("update angajat set salar= 0.95 * salar")
        self.conn.commit()


db = DB()


def get_selected_row(event):
    global selected_tuple
    index = list1.curselection()[0]
    selected_tuple = list1.get(index)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[1])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3])
    e4.delete(0, END)
    e4.insert(END, selected_tuple[4])


def afisare_angajati_command():
    list1.delete(0, END)
    for row in db.view():
        list1.insert(END, row)


def cautare_command():
    list1.delete(0, END)
    for row in db.search(nume_text.get(), prenume_text.get(), salar_text.get(), cnp_text.get()):
        list1.insert(END, row)


def adauga_command():
    db.insert(nume_text.get(), prenume_text.get(), salar_text.get(), cnp_text.get())
    list1.delete(0, END)
    list1.insert(END, (nume_text.get(), prenume_text.get(), salar_text.get(), cnp_text.get()))


def sterge_command():
    db.delete(selected_tuple[0])


def editeaza_command():
    db.update(selected_tuple[0], nume_text.get(), prenume_text.get(), salar_text.get(), cnp_text.get())

def reduce_command():
    db.scade()


window = Tk()

window.title("Lista angajati Apple")


def on_closing():
    dd = db
    if messagebox.askokcancel("Close", "Vrei sa inchizi fereastra?"):
        window.destroy()
        del dd


window.protocol("WM_DELETE_WINDOW", on_closing)  # handle window closing

l1 = Label(window, text="Nume")
l1.grid(row=1, column=0)

l2 = Label(window, text="Prenume")
l2.grid(row=2, column=0)

l3 = Label(window, text="Salar")
l3.grid(row=1, column=2)

l4 = Label(window, text="CNP")
l4.grid(row=2, column=2)

nume_text = StringVar()
e1 = Entry(window, textvariable=nume_text)
e1.grid(row=1, column=1)

prenume_text = StringVar()
e2 = Entry(window, textvariable=prenume_text)
e2.grid(row=2, column=1)

salar_text = StringVar()
e3 = Entry(window, textvariable=salar_text)
e3.grid(row=1, column=3)

cnp_text = StringVar()
e4 = Entry(window, textvariable=cnp_text)
e4.grid(row=2, column=3)

list1 = Listbox(window, height=6, width=35)
list1.grid(row=4, column=3, rowspan=10, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=4, column=5, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b7 = Button(window, text="Reducere salar 5%", width=18,fg="black",bg="light blue", command=reduce_command)
b7.grid(row=5, column=1)

b1 = Button(window, text="Afisare lista angajati", width=18,fg="black",bg="light yellow", command=afisare_angajati_command)
b1.grid(row=6, column=1)

'''b2 = Button(window, text="Cautare angajat", width=18,fg="black",bg="light yellow", command=cautare_command)
b2.grid(row=7, column=1)'''

b3 = Button(window, text="Adaugare angajat", width=18,fg="black",bg="light yellow", command=adauga_command)
b3.grid(row=7, column=1)

b4 = Button(window, text="Editare angajat", width=18,fg="black",bg="light yellow", command=editeaza_command)
b4.grid(row=8, column=1)

b5 = Button(window, text="Stergere angajat selectat", width=18,fg="black",bg="light yellow", command=sterge_command)
b5.grid(row=9, column=1)

b6 = Button(window, text="Inchidere", width=12,fg="black",bg="pink", command=window.destroy)
b6.grid(row=10, column=1)



window.mainloop()
