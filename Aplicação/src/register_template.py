from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import *
from database import Service

import os
import cv2
import requests
import threading
import tkinter as tk
import tkinter.ttk as ttk

class RegisterTemplate(Toplevel):
    def __init__(self, root, title, http):
        super().__init__(root)
        self.withdraw()
        
        self.get_employees()
        
        if len(self.employees) != 0:
            self.deiconify()
            self.resizable(False, False)
            self.title(title)
            
            icon = PhotoImage(file='assets/icon.png')
            self.iconphoto(False, icon)
            
            frame_info = Frame(self)
            frame_info.grid(row=0, column=0)
            
            label_employee = Label(frame_info, text='Funcionário:', font=('Arial 12 bold'))
            label_employee.grid(row=0, column=0, padx=10, pady=(30, 10))
            
            self.cb_employees = Combobox(frame_info, values=self.employees, font=('Arial 10'), width=40, state='readonly')
            self.cb_employees.grid(row=0, column=1, padx=10, pady=(20, 0))
            self.cb_employees.current(0)
            
            self.str_folder = StringVar()
            self.str_folder.set('Selecione a pasta com a captura')
            self.label_folder = Label(frame_info, textvariable=self.str_folder, font=('Arial 12 bold'))
            self.label_folder.grid(row=1, column=0, padx=10, pady=10)
            
            self.button_search = Button(frame_info, text='Buscar Captura', width=18, command=self.search_folder)
            self.button_search.grid(row=1, column=1, padx=10, pady=10)
            
            frame_button = Frame(self)
            frame_button.grid(row=1, column=0)
            
            self.str_button = StringVar()
            self.str_button.set('Registrar Template')
            self.button_register = Button(frame_button, textvariable=self.str_button, width=18, command=self.thread_registration)
            self.button_register.grid(row=2, column=1, padx=10, pady=(0, 20))
                    
            self.http = http
        else:
            messagebox.showerror(title='Falha no Registro', message='Nenhum funcionário cadastrado.', parent=self)
            self.destroy()
        
    def search_folder(self):
        foldername = filedialog.askdirectory(initialdir='dataset/templates', title='Selecione um diretório', parent=self)
        
        if len(foldername) != 0:
            self.str_folder.set(foldername)
            self.foldername = foldername
  
    def get_employees(self):
        db = Service('biometrica.db')
                    
        query = """SELECT id, name 
                    FROM employees  
                    ORDER BY name"""
                    
        cursor, info = db.select(query)
        
        db.close()
        
        self.employees = []
        self.employees_id = {}
        
        for row in info:
            self.employees.append(row[1])
            self.employees_id[row[1]] = row[0]
    
    def preprocess_video(self, folder, video):
        video_cap = cv2.VideoCapture(os.path.join(folder, video))
        success, image = video_cap.read()
        
        frame = 0
        
        while success:
            cv2.imwrite(os.path.join(folder, str(frame).zfill(8) + '.jpg'), image)
            success, image = video_cap.read()
            
            frame += 1
            
        os.remove(os.path.join(folder, video))
    
    def create_descriptors(self):
        folder = self.foldername
        frames = sorted(os.listdir(folder))
        
        if len(frames) == 1 and '.avi' in frames[0]:
            print(frames[0])
            self.preprocess_video(folder, frames[0])
            frames = sorted(os.listdir(folder))
        elif len(frames) == 0:
            return False
        
        files = []
        
        for frame in frames:
            files.append(('files', (frame, open(os.path.join(folder, frame), 'rb'), 'image/jpeg')))
        
        payload={}
        headers = {}

        response = requests.request('POST', self.http + '/createsingledescriptors', headers=headers, data=payload, files=files)
        
        if response.status_code == 200:
            return response.json()
        
        return False

    def register_template(self):
        try:
            db = Service('biometrica.db')
            
            descriptor = self.create_descriptors()
            
            if not descriptor:
                raise
            
            employee = self.cb_employees.get()
            employee_id = self.employees_id[employee]
            query = """INSERT INTO templates (employee_id, descriptor) 
                        VALUES (?, ?)"""
            data = (employee_id, str(descriptor))
            
            db.insert(query, data)
            
            messagebox.showinfo(title='Sucesso', message='Template registrado com sucesso.', parent=self)
        except Exception as e:
            messagebox.showerror(title='Falha no Registro', message='Erro ao registrar template.\n' + str(e), parent=self)
        finally:
            self.str_button.set('Registrar Template')
            self.button_register.configure(state=NORMAL)
            
            self.str_folder.set('Selecione a pasta com a captura')
            
            self.foldername = ''
            
            db.close()
            
    def thread_registration(self):
        self.str_button.set('Aguarde...')
        self.button_register.configure(state=DISABLED)
        
        t = threading.Thread(target=self.register_template)
        t.start()