from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from database import Service

import tkinter as tk
import tkinter.ttk as ttk

class RegisterUser(Toplevel):
    def __init__(self, root, title):
        super().__init__(root)
        
        self.resizable(False, False)
        self.title(title)
        
        icon = PhotoImage(file='assets/icon.png')
        self.iconphoto(False, icon)
        
        label_username = Label(self, text='Usuário:', font=('Arial', 12, 'bold'))
        label_username.grid(row=0, column=0, padx=10, pady=(30, 10))
        self.entry_username = Entry(self, width=30, font=('Arial', 10))
        self.entry_username.grid(row=0, column=1, padx=10, pady=(20, 0))
        
        label_password = Label(self, text='Senha:', font=('Arial', 12, 'bold'))
        label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = Entry(self, width=30, show='*', font=('Arial', 10))
        self.entry_password.grid(row=1, column=1, padx=10)

        label_confirmpassword = Label(self, text='Confirmar Senha:', font=('Arial', 12, 'bold'))
        label_confirmpassword.grid(row=2, column=0, padx=10, pady=10)
        self.entry_confirmpassword = Entry(self, width=30, show='*', font=('Arial', 10))
        self.entry_confirmpassword.grid(row=2, column=1, padx=10)

        self.button_registration = Button(self, text='Cadastrar', width=10, command=self.register)
        self.button_registration.grid(row=3, column=1, padx=10, pady=(0, 20))
    
    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirmpassword = self.entry_confirmpassword.get()
        
        if len(username) != 0 and len(password) != 0:
            if password == confirmpassword:
                db = Service('biometrica.db')
                
                query = """INSERT INTO users (username, password) 
                            VALUES (?, ?)"""
                data = (username, password)
                
                try:
                    db.insert(query, data)
                    
                    messagebox.showinfo(title='Sucesso', message='Usuário cadastrado com sucesso.', parent=self)
                    
                    self.entry_username.delete(0, END)
                    self.entry_password.delete(0, END)
                    self.entry_confirmpassword.delete(0, END)
                except Exception as e:
                    if 'users.username' in str(e):
                        messagebox.showerror(title='Falha no Cadastro', message='Este nome de Usuário já está cadastrado no banco de dados do sistema.', parent=self)
                    else:
                        messagebox.showerror(title='Falha no Cadastro', message='Erro desconhecido ao cadastrar o usuário. Tente novamente.', parent=self)
                finally:
                    db.close()
            else:
                messagebox.showerror(title='Falha no Cadastro', message='A senha e a confirmação da senha não são iguais.', parent=self)
        elif len(username) == 0 and len(password) == 0:
            messagebox.showerror(title='Falha no Cadastro', message='Os campos usuário e senha devem ser preenchidos corretamente.', parent=self)
        elif len(username) == 0:
            messagebox.showerror(title='Falha no Cadastro', message='O campo usuário deve ser preenchido corretamente.', parent=self)
        else:
            messagebox.showerror(title='Falha no Cadastro', message='O campo senha deve ser preenchido corretamente.', parent=self)