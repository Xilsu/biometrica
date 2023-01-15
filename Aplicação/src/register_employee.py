from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import *
from PIL import Image, ImageTk, ImageDraw
from database import Service

import tkinter as tk
import tkinter.ttk as ttk

class RegisterEmployee(Toplevel):
    def __init__(self, root, title):
        super().__init__(root)
        
        self.resizable(False, False)
        self.title(title)
        
        icon = PhotoImage(file='assets/icon.png')
        self.iconphoto(False, icon)

        label_name = Label(self, text='Nome Completo:', font=('Arial 12 bold'))
        label_name.grid(row=0, column=0, padx=10, pady=(30, 10))
        self.entry_name = Entry(self, width=47, font=('Arial 10'))
        self.entry_name.grid(row=0, column=1, padx=10, pady=(20, 0))
        
        self.get_roles()
        
        label_role = Label(self, text='Cargo:', font=('Arial 12 bold'))
        label_role.grid(row=1, column=0, padx=10, pady=10)
        self.cb_role = Combobox(self, values=self.roles, font=('Arial 10'), width=45)
        self.cb_role.current(0)
        self.cb_role.grid(row=1, column=1, padx=10, pady=10)

        frame_avatar = Frame(self)
        frame_avatar.grid(row=2, column=1, pady=10, padx=10)
        
        self.filename = 'assets/avatar.png'
        avatar = Image.open(self.filename).convert('RGBA')
        avatar = avatar.resize((205, 205), Image.Resampling.LANCZOS)
        background = Image.new('RGBA', avatar.size, (0, 0, 0, 0))
        mask = Image.new('RGBA', avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 200, 200), fill='green', outline=None)
        avatar = Image.composite(avatar, background, mask)
        img = ImageTk.PhotoImage(avatar)
        self.label_avatar = Label(frame_avatar, image=img, width=200)
        self.label_avatar.image = img
        self.label_avatar.grid(row=0, column=0)
        
        frame_buttons = Frame(self)
        frame_buttons.grid(row=3, column=1, pady=10)

        self.button_avatar = Button(frame_buttons, text='Buscar Imagem', width=14, command=self.search_avatar)
        self.button_avatar.grid(row=0, column=0, padx=10, pady=(0,20), sticky='E')
        
        self.button_registration = Button(frame_buttons, text='Cadastrar', width=14, command=self.register)
        self.button_registration.grid(row=0, column=1, padx=10, pady=(0,20), sticky='E')
    
    def get_roles(self):
        db = Service('biometrica.db')
        
        # query = """SELECT id, role FROM roles
        #             WHERE id != 4
        #             ORDER BY id"""
        
        query = """SELECT id, role 
                    FROM roles
                    ORDER BY id"""
                    
        cursor, info = db.select(query)
        
        db.close()
        
        self.roles = []
        self.roles_id = {}
        
        for row in info:
            self.roles.append(row[1])
            self.roles_id[row[1]] = row[0] 

    def search_avatar(self):
        filename = filedialog.askopenfilename(initialdir = 'assets', title = 'Selecione uma imagem', filetypes = (('Imagens', '*.jpg*'), ('Imagens', '*.jpeg*'), ('Imagens', '*.png*')), parent=self)
        
        if len(filename):
            self.filename = filename
            self.update_avatar()
    
    def to_binary(self, filename):
        with open(filename, 'rb') as f:
            blob = f.read()
            
        return blob
    
    def update_avatar(self):
        avatar = Image.open(self.filename).convert('RGBA')
        avatar = avatar.resize((205, 205), Image.Resampling.LANCZOS)
        background = Image.new('RGBA', avatar.size, (0, 0, 0, 0))
        mask = Image.new('RGBA', avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 200, 200), fill='green', outline=None)
        avatar = Image.composite(avatar, background, mask)
        img = ImageTk.PhotoImage(avatar)
        self.label_avatar.configure(image=img)
        self.label_avatar.image = img
        
    def register(self):
        name = self.entry_name.get()
        role = self.cb_role.get()
        role_id = self.roles_id[role]
        
        if len(name) == 0:
            messagebox.showerror(title='Falha no Cadastro', message='Erro ao cadastrar funcionário!', parent=self)
            return
        
        db = Service('biometrica.db')
        
        blob = self.to_binary(self.filename)
        query = """INSERT INTO employees (name, role_id, avatar) 
                    VALUES (?, ?, ?)"""
        data = (name, role_id, blob)
        
        try:
            db.insert(query, data)
            
            messagebox.showinfo(title='Sucesso', message='Funcionário cadastrado com sucesso!', parent=self)
            
            self.entry_name.delete(0, END)
            self.cb_role.current(0)
            self.filename = 'assets/avatar.png'
            
            self.update_avatar()
        except Exception as e:
            messagebox.showerror(title='Falha no Cadastro', message='Erro ao cadastrar funcionário!\n' + str(e), parent=self)
        finally:
            db.close()