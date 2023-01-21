from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from application import Application
from database import Service
from register_user import RegisterUser

import tkinter as tk
import tkinter.ttk as ttk

class Login:
    def __init__(self, title):
        self.window = ThemedTk(theme='breeze')
        self.window.resizable(False, False)
        self.window.title(title)
        
        icon = PhotoImage(file='assets/icon.png')
        self.window.iconphoto(False, icon)
        
        frame_logo = Frame(self.window)
        frame_logo.pack(side=LEFT)
        logo = Image.open('assets/logo.png')
        logo = logo.resize((100, 100), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(logo)
        self.label_logo = Label(frame_logo, image=img)
        self.label_logo.image = img
        self.label_logo.grid(row=0, column=0, padx=(10, 0) , pady=20)
        
        frame_info = Frame(self.window)
        frame_info.pack(side=LEFT)
        
        label_login = Label(frame_info, text='Usuário', font=('Arial', 12, 'bold'))
        label_login.grid(row=0, column=0, padx=10, pady=(30, 10))
        self.entry_username = Entry(frame_info, width=30, font=('Arial', 10))
        self.entry_username.grid(row=0, column=1, padx=10, pady=(20, 0))
        
        label_password = Label(frame_info, text='Senha', font=('Arial', 12, 'bold'))
        label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = Entry(frame_info, width=30, show='*', font=('Arial', 10))
        self.entry_password.grid(row=1, column=1, padx=10)
        
        frame_buttons = Frame(frame_info)
        frame_buttons.columnconfigure(1, minsize=20, weight=1)
        frame_buttons.grid(row=2, column=1)
        
        button_login = Button(frame_buttons, text='Log In', width=10, command=self.login)
        button_login.grid(row=0, column=0, padx=(0, 10), pady=(0, 20), sticky='E')
        
        button_quit = Button(frame_buttons, text='Sair', width=10, command=self.quit)
        button_quit.grid(row=0, column=1, pady=(0, 20), sticky='W')
        
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if len(username) != 0 and len(password) != 0:
            db = Service('biometrica.db')
            
            query = """SELECT * 
                        FROM users 
                        WHERE username = '{}' 
                        AND password = '{}'""".format(username, password)
                
            cursor, info = db.select(query)
            
            db.close()
            
            if len(info) != 0:
                self.window.destroy()
                
                app = Application('BIOMETRICA - ' + username, 'http://5293-34-143-131-183.ngrok.io')
                app.window.mainloop()
            else:
                messagebox.showerror(title='Falha no Login', message='O nome de Usuário e/ou a Senha estão incorretos.')
        elif len(username) == 0 and len(password) == 0:
            messagebox.showerror(title='Falha no Login', message='Os campos Usuário e Senha devem ser preenchidos corretamente.')
        elif len(username) == 0:
            messagebox.showerror(title='Falha no Login', message='O campo Usuário deve ser preenchido corretamente.')
        else:
            messagebox.showerror(title='Falha no Login', message='O campo Senha deve ser preenchido corretamente.')
            
    def quit(self):
        self.window.destroy()
        
if __name__ == '__main__':
    login = Login('Login')
    login.window.mainloop()