from peewee import *
from tkinter import *
from tkinter import messagebox
from pass_generator import *


db = SqliteDatabase("login.db")

valida_interno = ""


class Login(Model):
    user_reg = CharField()
    pass_reg = CharField()

    class Meta():
        database = db

def create_and_connect():
    db.connect()
    db.create_tables([Login], safe=True)


class Prueba(Frame):

    def __init__(self,master = None):
        Frame.__init__(self, master)
        self.user_name_login = StringVar()
        self.password_login = StringVar()
        self.create_widgets(self.user_name_login, self.password_login)

    def crea_usuario(self):
        new_user = Login.create(user_reg = input("Ingrese nombre de usuario"), pass_reg = input("Contra"))

    def create_widgets(self, text_user, text_pass):
        Button(self.master,text="Login", command=lambda:self.login()).grid(column=0, row=2,padx=2,pady=2)
        Button(self.master,text="Registrar", command=lambda:self.crea_usuario()).grid(column=1, row=2,padx=2,pady=2)
        Label(self.master,text="Usuario").grid(column=0, row=0,padx=2,pady=2)
        Label(self.master,text="Contraseña").grid(column=0, row=1,padx=2,pady=2)
        Entry(self.master,textvariable=text_user).grid(column=1, row=0,padx=2,pady=2)
        Entry(self.master,textvariable=text_pass).grid(column=1, row=1,padx=2,pady=2)

    def login(self):
        dict = {"":""}
        for i in Login.select().where(Login.user_reg == self.user_name_login.get()):
            dict = {i.user_reg:i.pass_reg}
        dict_screen = {self.user_name_login.get():self.password_login.get()}
        if dict_screen == dict:
            print("acceso permitido")
            inicia()
        else:
            print("acceso denegado")




create_and_connect()

x = Prueba()
