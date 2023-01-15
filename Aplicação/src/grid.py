from tkinter import *
from tkinter.ttk import *

import tkinter as tk
import tkinter.ttk as ttk

class Grid(Frame):
    def __init__(self, root, table_columns, columns_names, column_width):
        super().__init__(root)
        
        scrollbar_vertical = Scrollbar(self)
        scrollbar_vertical.pack(side=RIGHT, fill=Y)

        scrollbar_horizontal = Scrollbar(self, orient='horizontal')
        scrollbar_horizontal.pack(side=BOTTOM, fill=X)

        self.table = Treeview(self, yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)
        self.table.pack()
        self.table['columns'] = table_columns
        self.table.column("#0", width=0,  stretch=NO)
        self.table.heading("#0",text="",anchor=CENTER)
        
        scrollbar_vertical.config(command=self.table.yview)
        scrollbar_horizontal.config(command=self.table.xview)
        
        txt = columns_names
        i = 0
        
        for column_name in self.table['columns']:
            self.table.column(column_name, anchor=CENTER, width=column_width)
            self.table.heading(column_name, text=txt[i], anchor=CENTER)
            
            i = i + 1

    def insert_row(self, values, iid):
        self.table.insert(parent='', index='end', iid=iid, text='', values=values)
        self.table.pack()
    
    def delete_rows(self):
        self.table.delete(*self.table.get_children())