
from tkinter import *
import pickle
import random
import string
from peewee import *
from login import *


db = SqliteDatabase("passwd.db")

class Pass_manager(Model):
    pass_w = CharField()
    client = CharField()

    class Meta():
        database = db

def create_and_connect():
    db.connect()
    db.create_tables([Pass_manager], safe=True)


def inicia():
    global windows_pass
    global pass_screen
    global enter_pass
    global enter_pass_valid
    global entered_client
    global entered_client_for_delete
    global entered_client_for_custom
    global entered_pass
    global enter_pass_valid
    global entered_pass_valid
    global password
    global password_list

    root = Tk()
    root.title("Pass generator")
    root.config(background="#E6E6E6", padx=50, pady=40)
    root.resizable(0,0)
    root.iconbitmap("padlock.ico")

    pass_screen = StringVar()
    entered_pass = StringVar()
    entered_pass_valid = StringVar()
    entered_client_for_custom = StringVar()
    entered_client_for_delete = StringVar()
    entered_client = StringVar()
    password = ""
    password_list = []


    windows_pass = Entry(root,textvariable=pass_screen)
    windows_pass.grid(row=1, columnspan=5, padx=1, pady=10)
    windows_pass.config(background = "#E6E6E0", fg="#2E2E2E", justify="center",
                        state="readonly")
    windows_pass.selection_range(0, END)

    crea_boton(root, "Delete password",delete_pass_window, 2, 4, 5, 5)
    crea_boton_span(root, "Generate Password", make_pass, 0, 8, 5, 5)
    crea_boton(root, "Save password", enter_client_for_generated_pass, 2, 1, 5, 5)
    crea_boton(root, "Load list", load_pass_list, 2,2,5,5)
    crea_boton(root, "Custom password", defined_pass, 2,3,5,5)
    root.mainloop()

def make_pass():
    global pass_screen
    global password
    global windows_pass
    alphabet = string.ascii_letters + string.digits + ("%&")*5
    while True:
        password = ''.join(random.choice(alphabet) for i in range(8))
        if(any(c.islower() for c in password) and
           any(c.isupper() for c in password)
           and sum(c.isdigit() for c in password) >= 3):
           break
    windows_pass.selection_from(0)
    pass_screen.set(password)
    print(password)



def defined_pass():
    secondary_window = Toplevel()
    secondary_window.geometry("300x160")
    secondary_window.resizable(0,0)
    ask_pass = Label(secondary_window, text="Ingrese la contreseña",
                     pady=5, padx=5)
    ask_pass_valid = Label(secondary_window, text="Reingrese la contreseña",
                               pady=5, padx=5)
    ask_client = Label(secondary_window, text="Ingrese nombre de cuenta",
                           pady=5, padx=5)
    ask_pass.grid(row=0, column=0)
    ask_pass_valid.grid(row=1, column=0)
    enter_pass = Entry(secondary_window, textvariable=entered_pass, show="*")
    enter_pass_valid = Entry(secondary_window,
                             textvariable=entered_pass_valid, show="*")
    enter_client = Entry(secondary_window, textvariable=entered_client_for_custom)
    enter_client.grid(row=2, column=1)
    enter_pass.grid(row=0, column=1)
    enter_pass_valid.grid(row=1, column=1)
    ask_client.grid(row=2, column=0)
    save_def_pass = Button(secondary_window, text="Save pass",
                           command=lambda:save_defined_pass())
    save_def_pass.grid(row=3, column=1)
def save_defined_pass():
    if entered_pass.get() == "" or entered_client_for_custom.get() == "":
        show_error_message()
    elif entered_pass.get() == entered_pass_valid.get():
        password_def_create = Pass_manager.create(password_user_account = entered_pass.get(),
                                                  client = entered_client_for_custom.get()).where()
        entered_pass.set("")
        entered_pass_valid.set("")
        entered_client.set("")
        show_success_message()
    else:
        show_error_message()

def enter_client_for_generated_pass():
    secondary_window = Toplevel()
    ask_client = Label(secondary_window, text="Ingrese nombre de cuenta",
                       pady=5, padx=5)
    ask_client.grid(row=0, column=0)
    enter_client = Entry(secondary_window, textvariable=entered_client)
    enter_client.grid(row=0, column=1)
    crea_boton(secondary_window, "Save pass", save_pass_list, 1, 1, 5, 5)

def delete_pass_window():
    win = Toplevel()
    ask_client = Label(win, text="Ingrese nombre de cuenta que desea borrar",
                       pady=5, padx=5)
    ask_client.grid(row=0, column=0)
    enter_client = Entry(win, textvariable=entered_client_for_delete)
    enter_client.grid(row=0, column=1)
    crea_boton(win, "Delete password", delete_pass, 1, 0, 5,5)

def delete_pass():
    client = entered_client_for_delete.get()
    pass_del = Pass_manager.delete().where(Pass_manager.client == client)
    deleted_entries = pass_del.execute()
    print("{} registros borrados".format(deleted_entries))
    entered_client_for_delete.set("")


def save_pass_list():
    password_list = windows_pass.get()
    if windows_pass.get() == "" or entered_client.get() == "":
        show_error_message()
    else:
        password_create = Pass_manager.create(pass_w = password_list,
                                              client = entered_client.get())
        entered_client.set("")
        show_success_message()
def show_error_message():
    message = Toplevel()
    message.resizable(0,0)
    message.geometry("100x100")
    lab_err = Label(message, text="ERROR!")
    lab_err.pack()
    lab_err.config(background = "#E6E6E6", fg="#2E2E2E", justify="left",
               padx=120, pady=120)

def show_success_message():
    message = Toplevel()
    message.resizable(0,0)
    message.geometry("100x100")
    lab_success = Label(message, text="SUCCESS!")
    lab_success.pack()
    lab_success.config(background = "#E6E6E6", fg="#2E2E2E", justify="left",
               padx=120, pady=120)

def load_pass_list():
    y = Prueba()
    pass_list_window = Toplevel()
    scrollbar = Scrollbar(pass_list_window)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_list = Listbox(pass_list_window, yscrollcommand=scrollbar.set)
    text_list.config(height=25, width=45)
    for i in Pass_manager.select():
        text_list.insert(END, " " + i.pass_w + " " + "|" + " " + i.client + "\n")
        text_list.pack()
        # ------------------- Buttons -------------------------------

def crea_boton_span(wind, text, command, row, columnspan, padx, pady):
    bot = Button(wind, text=text, command=command)
    bot.grid(row=row, columnspan=columnspan, padx = padx, pady = pady)

def crea_boton(wind, text, command, row, column, padx, pady):
    bot = Button(wind, text=text, command=command)
    bot.grid(row=row, column=column, padx = padx, pady = pady)




create_and_connect()
