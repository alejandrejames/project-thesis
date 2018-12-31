from tkinter import *
from submodules import topicmodel as t2
from submodules import usrmodules as usmdls
import os
import subprocess
import webbrowser

class mnpage:
    def __init__(self, master):
        self.master = master
        master.title("Topic Anlaysis Tool")
        master.minsize(600, 400)
        master.maxsize(600, 400)
        
        menu = Menu(master)
        root.config(menu=menu)

        subMenu = Menu(menu)
        menu.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="Exit", command=master.quit)

        ##Widgets
        #Topic Modelling
        self.title_label = Label(master, text="Topic Modeling")
        self.flname_label = Label(master, text="File name")
        self.flname_entry = Entry()
        self.gener_button = Button(master, text="Generate models", command=lambda: self.genertp(self.flname_entry.get()))
        self.outlbl_label = Label(master, text="")
    
        #Data Collection
        self.title2_label = Label(master, text="Data Collection")
        self.query_label = Label(master, text="Query/Keyword")
        self.query_entry = Entry()
        self.query_button = Button(master, text="Collect Data", command=lambda: self.collectdta(self.query_entry.get()))
        self.outlbl2_label = Label(master, text="aa")
        ##
        
        ##WidgetPlacements
        #Topic Modelling
        self.title_label.grid(columnspan=100)
        self.flname_label.grid(row=1,column=0)
        self.flname_entry.grid(row=1,column=1)
        self.gener_button.grid(row=2,column=1)
        self.outlbl_label.grid(row=3,column=1)
        #Data Collection
        self.title2_label.grid()
        self.query_label.grid(row=5,column=0)
        self.query_entry.grid(row=5,column=1)
        self.query_button.grid(row=6,column=1)
        self.outlbl2_label.grid(row=7)

    def genertp(self,name):
        #from pprint import pprint
        #cleaned = t2.cleaning(name)
        #corpus = t2.mkcorpus(cleaned)
        self.outlbl_label.configure(text=name)
        
    def collectdta(self,query):
        usmdls.collectdata(query)
        self.outlbl2_label.configure(text="Completed")

root = Tk()
mainpage = mnpage(root)
root.mainloop()
