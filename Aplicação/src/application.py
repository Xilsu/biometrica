from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from ttkthemes import ThemedTk
from tkvideo import tkvideo
from PIL import Image, ImageTk, ImageDraw
from matplotlib import cm
from grid import Grid
from register_user import RegisterUser
from register_role import RegisterRole
from register_employee import RegisterEmployee
from register_template import RegisterTemplate
from search_role import SearchRole
from search_employee import SearchEmployee
from inference import Inference
from logs import Logs
from about import About

import os
import tkinter as tk
import tkinter.ttk as ttk
import threading

class Application:
    def __init__(self, title, http):
        self.window = ThemedTk(theme='breeze')
        self.window.resizable(False, False)
        self.window.title(title)
        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)
        
        icon = PhotoImage(file='assets/icon.png')
        self.window.iconphoto(False, icon)
        
        menubar = Menu(self.window)
        self.window.config(menu=menubar)

        style = Style()
        style.configure('TNotebook.Tab', font=('Arial','12','bold') )
        
        tabs = Notebook(self.window)
        tab_lastdetection = Frame(tabs)
        self.tab_historic = Frame(tabs)
        tabs.add(tab_lastdetection, text='Última Detecção')
        tabs.add(self.tab_historic, text='Histórico de Detecções')
        tabs.pack(expand=1, fill='both')

        self.table_cols = ('data', 'funcionario', 'cargo', 'status')
        self.col_names = ['Data-Hora', 'Funcionário', 'Cargo', 'Status']
        self.grid_historic = Grid(self.tab_historic, self.table_cols, self.col_names, 303)
        self.grid_historic.configure(height=28)
        self.grid_historic.pack()
        
        menu_registration = Menu(menubar, tearoff=0)
        menu_registration.add_command(label='Usuários', font=('Arial', 12), command=self.registration_user)
        menu_registration.add_command(label='Cargos', font=('Arial', 12), command=self.registration_role)
        menu_registration.add_command(label='Funcionários', font=('Arial', 12), command=self.registration_employee)
        menubar.add_cascade(label='Cadastrar', menu=menu_registration, font=('Arial', 12))

        menubar.add_command(label='Templates', font=('Arial', 12), command=self.registration_template)

        menu_search = Menu(menubar, tearoff=0)
        menu_search.add_command(label='Cargos', font=('Arial', 12), command=self.fetch_role)
        menu_search.add_command(label='Funcionários', font=('Arial', 12), command=self.fetch_employee)
        menubar.add_cascade(label='Consultar', menu=menu_search, font=('Arial', 12))

        menu_about = Menu(menubar, tearoff=0)
        menu_about.add_command(label='Sobre', font=('Arial', 12), command=self.show_about)
        menubar.add_cascade(label='Ajuda', menu=menu_about, font=('Arial', 12))
        
        frame_feed = Frame(tab_lastdetection)
        frame_feed.grid(row=0, column=0)
        
        self.status_label = {0 : 'NEGADO', 
                        1 : 'AUTORIZADO'}
        self.status_color = {0 : 'red', 
                        1 : 'green'}
        
        self.employee_name = StringVar()
        self.employee_role = StringVar()
        self.detection_datetime = StringVar()
        self.authorize_status = StringVar()

        label_employee = Label(frame_feed, textvariable=self.employee_name, font=('Arial', 16, 'bold'), width=27, anchor='center')
        label_employee.grid(row=1, column=1)
        
        self.label_avatar = Label(frame_feed, width=200)
        self.label_avatar.grid(row=2, column=1, pady=10)
        
        button_left = Button(frame_feed, text='<', width=1, command=self.turn_left)
        button_left.grid(row=2, column=0, padx=(20, 0), pady=5, sticky='e')
        
        button_right = Button(frame_feed, text='>', width=1, command=self.turn_right)
        button_right.grid(row=2, column=2, padx=(0, 20), pady=5, sticky='w')
        
        label_role = Label(frame_feed, textvariable=self.employee_role, font=('Arial', 12))
        label_role.grid(row=3, column=1, padx=20, pady=5)
        
        label_datetime = Label(frame_feed, textvariable=self.detection_datetime, font=('Arial', 12))
        label_datetime.grid(row=4, column=1, padx=20, pady=5)
        
        self.label_status = Label(frame_feed, textvariable=self.authorize_status, font=('Arial', 16, 'bold'), foreground='green')
        self.label_status.grid(row=5, column=1, padx=20, pady=5)
        
        icon = Image.open('assets/refresh.png')
        icon = icon.resize((50,50), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(icon)
        self.button_refresh = Button(frame_feed, text='Atualizar', image=img, compound=LEFT, command=self.update_logs)
        self.button_refresh.image = img
        self.button_refresh.grid(row=6, column=1, padx=20, pady=10, sticky='s')

        frame_video = Frame(tab_lastdetection)
        frame_video.grid(row=0, column=1, sticky='e')

        label_video = Label(frame_video, relief='solid', borderwidth=1)
        label_video.grid(row=0, column=0, padx=20, pady=20, sticky='e')
        
        self.video = 'assets/lastdetection.avi'
        player = tkvideo(self.video, label_video, loop = 1, size = (800, 600))
        player.play()
        
        self.http = http
        
        self.logs = Logs()
        self.update_logs()
        
        self.thread_inference()
                
    def registration_user(self):
        RegisterUser(self.window, 'Cadastro de Usuários')
    
    def registration_role(self):
        RegisterRole(self.window, 'Cadastro de Cargos')
    
    def registration_employee(self):
        RegisterEmployee(self.window, 'Cadastro de Funcionários')

    def registration_template(self):
        RegisterTemplate(self.window, 'Registro de Templates', self.http)

    def fetch_employee(self):
        SearchEmployee(self.window, 'Consulta de Funcionários')

    def fetch_role(self):
        SearchRole(self.window, 'Consulta de Cargos')

    def show_about(self):
        About(self.window, 'Sobre')
        
    def turn_left(self):
        self.feed_page = (self.feed_page - 1 + self.num_detected) % self.num_detected
        
        self.update_feed()
        
    def turn_right(self):
        self.feed_page = (self.feed_page + 1) % self.num_detected
        
        self.update_feed()
        
    def update_feed(self):
        authorized = self.list_detected[self.feed_page]['status']
        
        self.employee_name.set(self.list_detected[self.feed_page]['name'])
        self.employee_role.set(self.list_detected[self.feed_page]['role'])
        self.detection_datetime.set(self.list_detected[self.feed_page]['datetime'])
        self.authorize_status.set(self.status_label[authorized])
        self.label_status.configure(foreground=self.status_color[authorized])
    
        avatar = Image.open(self.list_detected[self.feed_page]['picture_path']).convert('RGBA')
        avatar = avatar.resize((205,205), Image.Resampling.LANCZOS)
        background = Image.new('RGBA', avatar.size, (0, 0, 0, 0))
        mask = Image.new('RGBA', avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 200, 200), fill='green', outline=None)
        avatar = Image.composite(avatar, background, mask)
        img = ImageTk.PhotoImage(avatar)
        self.label_avatar.configure(image=img)
        self.label_avatar.image = img

    def show_warning(self):
        messagebox.showerror(title='Alerta de Segurança', message='Acesso não autorizado detectado.')

    def write_tofile(self, filename, data):
        with open(filename, 'wb') as f:
            f.write(data)

    def update_logs(self):
        self.list_detected = []
        df = self.logs.get_logs()
        self.grid_historic.delete_rows()
        
        warning = 0
        
        if len(df) != 0:
            last_log = df.iloc[-1]
            last_datetime = last_log['datetime']
            
            for i, row in df.iterrows():
                name = str(row['name'])
                role = str(row['role'])
                datetime = row['datetime']
                authorized = row['authorized']
                blob = row['avatar']
            
                if datetime is not None:
                    authorized = 0 if int(authorized) == False else 1
                    self.grid_historic.insert_row((datetime, name, role, self.status_label[authorized]), i)
                    
                    if datetime == last_datetime:
                        if blob is not None and str(blob) != '' and str(blob) != 'NULL':
                            self.write_tofile(os.path.join('assets', name + '.png'), blob)
                        else:
                            with open('assets/avatar.png', 'rb') as img:
                                f = img.read()
                                self.write_tofile(os.path.join('assets', name + '.png'), bytearray(f))
                        
                        if authorized == 0:
                            warning = 1
                        
                        self.list_detected.append({'name': name, 
                                                    'role': 'Cargo: ' + role,
                                                    'datetime': 'Data: ' + str(datetime),
                                                    'status': int(authorized),
                                                    'picture_path': os.path.join('assets', name + '.png')})
        
        if len(self.list_detected) == 0:
            self.list_detected.append({'name': 'Nome Completo do Funcionário', 
                                        'role': 'Cargo do Funcionário',
                                        'datetime': 'Data: AA/MM/DD HH:MM:SS',
                                        'status': 1,
                                        'picture_path': 'assets/avatar.png'})
        
        self.feed_page = 0
        self.num_detected = len(self.list_detected)
        
        self.update_feed()
                        
        if warning:
            warning = threading.Thread(target=self.show_warning)
            warning.start()
            
    def thread_inference(self):
        self.t = Inference(self.http, self)
        self.t.start()
            
    def on_closing(self):
        self.t.stop = True
        self.window.destroy()