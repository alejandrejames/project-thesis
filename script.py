#Scripting tool to find the tweets related to the topic keywords generated
import pandas as pd
from tkinter import *
from tkinter import ttk
import tkinter as tk

data = pd.read_csv('orginaldata.csv', 
error_bad_lines=False)
# We only need the Headlines text column from the data
data_text = data[['data']]
data_text = data_text.astype('str');
data = data_text.data.values.tolist()

main = Tk()
main.title('Scripting tool')
main.geometry('1200x600')
main.maxsize(1200,600)
main.minsize(1200,600)
num = 0
for x in data:
    if(x!='nan'):
        print(data[num])
    num = num + 1

def searchres(inp):
    text1.delete('1.0', tk.END)
    print(entry1.get())
    listelem = []
    num = 0
    with open('scriptresults.txt','w') as file:
    
        for num in range(0,9069):
            if(inp in data[num]):
                text = str(num)+'-Tweet = '+data[num]+'\n\n'
                text1.insert(END,text)
                file.write(text)
