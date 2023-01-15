from tkinter import *
from tkinter.ttk import *
from database import Service
from grid import Grid

import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk

class SearchRole(Toplevel):
    def __init__(self, root, title):
        super().__init__(root)
        
        self.resizable(False, False)
        self.title(title)
        
        icon = PhotoImage(file='assets/icon.png')
        self.iconphoto(False, icon)

        table_columns = ('id', 'role', 'access_level')
        columns_names = ['ID', 'Cargo', 'Nível de Acesso']
        self.grid_historic = Grid(self, table_columns, columns_names, 200)
        self.grid_historic.pack()
        self.populate()

    def populate(self):
        db = Service('biometrica.db')
        
        # query = """
        #     SELECT id, role, access_level
        #     FROM cargos
        #     WHERE id != 4
        #     ORDER BY id
        # """
        
        query = """SELECT id, role, access_level
                    FROM roles
                    ORDER BY id"""
        
        cursor, info = db.select(query)
        
        db.close()
        
        columns_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(info, columns=columns_names)
        
        for i, item in enumerate(df.iterrows()):
            _, row = item
            self.grid_historic.insert_row((row['id'], row['role'], row['access_level']), i)