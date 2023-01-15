from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from database import Service

import tkinter as tk
import tkinter.ttk as ttk

class RegisterRole(Toplevel):
    def __init__(self, root, title):
        super().__init__(root)
        
        self.resizable(False, False)
        self.title(title)
        
        icon = PhotoImage(file='assets/icon.png')
        self.iconphoto(False, icon)

        label_role = Label(self, text='Cargo:', font=('Arial 12 bold'))
        label_role.grid(row=0, column=0, padx=10, pady=(30, 10))
        self.entry_role = Entry(self, width=32, font=('Arial 10'))
        self.entry_role.grid(row=0, column=1, padx=10, pady=(20, 0))
        
        label_accesslevel = Label(self, text='Acesso:', font=('Arial 12 bold'))
        label_accesslevel.grid(row=1, column=0, padx=10, pady=10)
        self.cb_accesslevel = Combobox(self, values = [0, 1, 2], font=('Arial 10'), width=30, state='readonly')
        self.cb_accesslevel.current(0)
        self.cb_accesslevel.grid(row=1, column=1, padx=10)

        self.button_registration = Button(self, text='Cadastrar', width=10, command=self.register)
        self.button_registration.grid(row=2, column=1, padx=10, pady=(0, 20))
    
    def register(self):
        role = self.entry_role.get()
        accesslevel = self.cb_accesslevel.get()
        
        if len(role) != 0:
            db = Service('biometrica.db')
            
            query = """INSERT INTO roles (role, access_level) 
                        VALUES (?, ?)"""
            data = (role, accesslevel)
            
            try:
                db.insert(query, data)
                
                messagebox.showinfo(title='Sucesso', message='Cargo cadastrado com sucesso.', parent=self)
                
                self.entry_role.delete(0, END)
                self.cb_accesslevel.current(0)
            except Exception as e:
                if 'roles.role' in str(e):
                    messagebox.showerror(title='Falha no Cadastro', message='Este cargo já está cadastrado no banco de dados do sistema.', parent=self)
                    print(str(e))
                else:
                    messagebox.showerror(title='Falha no Cadastro', message='Erro desconhecido ao cadastrar o cargo. Tente novamente.', parent=self)
            finally:
                db.close()
        else:
            messagebox.showerror(title='Falha no Cadastro', message='O campo Cargo deve ser preenchido corretamente.', parent=self)