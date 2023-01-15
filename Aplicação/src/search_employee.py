from tkinter import *
from tkinter.ttk import *
from database import Service
from grid import Grid

import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk

class SearchEmployee(Toplevel):
    def __init__(self, root, title):
        super().__init__(root)
        
        self.resizable(False, False)
        self.title(title)
        
        icon = PhotoImage(file='assets/icon.png')
        self.iconphoto(False, icon)

        tables_columns = ('id', 'name', 'role', 'access_level')
        columns_names = ['ID', 'Nome', 'Cargo', 'Nível de Acesso']
        self.grid_historic = Grid(self, tables_columns, columns_names, 300)
        self.grid_historic.pack()
        self.populate()

    def populate(self):
        db = Service('biometrica.db')
        
        # query = """SELECT employees.id, employees.name, roles.role, roles.access_level
        #             FROM employees
        #             LEFT JOIN roles ON employees.role_id = roles.id 
        #             WHERE employees.id != 5
        #             ORDER BY employees.id"""
                    
        query = """SELECT employees.id, employees.name, roles.role, roles.access_level
                    FROM employees
                    LEFT JOIN roles ON employees.role_id = roles.id 
                    ORDER BY employees.id"""
            
        cursor, result = db.select(query)
        
        db.close()
        
        columns_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=columns_names)
        
        for i, item in enumerate(df.iterrows()):
            _, row = item
            self.grid_historic.insert_row((row['id'], row['name'], row['role'], row['access_level']), i)