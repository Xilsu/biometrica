from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

import tkinter as tk
import tkinter.ttk as ttk

class About(Toplevel):
    def __init__(self, root, title):
        super().__init__(root)
        
        self.resizable(False, False)
        self.title(title)
        
        icon = PhotoImage(file='assets/icon.png')
        self.iconphoto(False, icon)

        logo = Image.open('assets/logo.png')
        logo = logo.resize((200, 200), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(logo)
        self.label_logo = Label(self, image=img, width=200, anchor='center')
        self.label_logo.image = img
        self.label_logo.grid(row=0, column=0, padx=10, pady=(20, 0))

        label_app = Label(self, text='BIOMETRICA', font=('Arial', 16, 'bold'))
        label_app.grid(row=1, column=0, padx=10, pady=20)

        label_1 = Label(self, text='Sistema de Reconhecimento Biométrico de Múltiplas Pessoas Baseado na Fusão de Descritores Antropométricos e de Marcha', font=('Arial', 12), foreground='gray')
        label_1.grid(row=2, column=0, padx=10)
        label_2 = Label(self, text='TCC - Bacharelado em Ciência da Computação', font=('Arial', 12), foreground='gray')
        label_2.grid(row=3, column=0, padx=10)
        label_3 = Label(self, text='Aluno: Luis Henrique Morelli', font=('Arial', 12), foreground='gray')
        label_3.grid(row=4, column=0, padx=10)
        label_3 = Label(self, text='Orientador: Aparecido Nilceu Marana', font=('Arial', 12), foreground='gray')
        label_3.grid(row=5, column=0, padx=10, pady=(0, 20))