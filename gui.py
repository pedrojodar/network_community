import tkinter as tk
from tkinter import ttk
import base64
from tkinter.ttk import *

file_=open('user_stored','r').read().splitlines()

launch = tk.Tk()
existint=ttk.Entry(launch, text='username')
existint.place(x=20, y=20)
def load_graph ():
    import network_creation_analisis
def using_stored_info():
    def use_existint_info():
        select.destroy()
        load_graph()
    def update_info():
        select.destroy()
    select = tk.Tk()
    new=ttk.Button(select, text='Use stored information', command = use_existint_info)
    new.place(x=20, y=20)
    load=ttk.Button(select, text='Use new information',command = update_info)
    load.place(x=20, y=50)

def check_user ():
    import json
    with open("message.json", "r") as j:
        mydata = json.load(j) 
    value = existint.get()
    mydata["user"]=value
    with open("message.json", "w") as j:
        json.dump(mydata, j)   
    if (value in file_):
        using_stored_info()
    else :
        update_info()
    print (value)
new = ttk.Button(launch, text='Create new profile', command=check_user)
new.place(x=20, y=50)
launch.mainloop()