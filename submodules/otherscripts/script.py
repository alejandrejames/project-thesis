#Scripting tool to find the tweets related to the topic keywords generated
import pandas as pd
from tkinter import *
from tkinter import ttk
import tkinter as tk

data = pd.read_csv('improveddata.csv', 
error_bad_lines=False)
# We only need the Headlines text column from the data
data_text = data[['data']]
data_text = data_text.astype('str');
data = data_text.data.values.tolist()
wrds = ['city','tete']

window = Tk()
window.title('Tweet Viewer')
window.geometry('700x900')

variable = StringVar(window)
variable.set(wrds[0]) # default value

lbl = Label(window,text="Words")
w = OptionMenu(window, variable, *wrds)
bttn = Button(window,text="view tweets",command=lambda:searchwrd(variable.get()))
lbl2 = Label(window,text="Tweets")
text1 = Text(window)
text1.config(state="disabled")

def searchwrd(wrd):
    text1.config(state="normal")
    print(wrd)
    text1.delete("1.0",END)
    num = 0
    for y in data:
        if(str(wrd) in y):
            num = num + 1
            text1.insert(END,str(num)+".) "+y+"\n\n")
    text1.config(state="disabled")
    
lbl.pack()
w.pack()
bttn.pack()
lbl2.pack()
text1.pack()

