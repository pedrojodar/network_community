import tkinter as tk
from tkinter import ttk
import base64
from tkinter.ttk import *


import json


with open("message.json", "r") as j:
    mydata_2 = json.load(j) 

    

if (not mydata_2['is_set_up']):
    set_up_window = tk.Tk()
    set_up_window.title('T.A. set-up')
    info_1=ttk.Entry(set_up_window, text='consumer_key')
    info_1.place(x=20, y=20)
    info_2=ttk.Entry(set_up_window, text='consumer_secret')
    info_2.place(x=20, y=40)    
    info_3=ttk.Entry(set_up_window, text='bearer_token')
    info_3.place(x=20, y=60)
    info_4=ttk.Entry(set_up_window, text='access_token')
    info_4.place(x=20, y=80)
    info_5=ttk.Entry(set_up_window, text='access_token_secret')
    info_5.place(x=20, y=100)
    def save_credentials ():
        f_Cre=open('access_3_val.txt','w')
        f_Cre.write(info_1.get()+'\n')
        f_Cre.write(info_2.get()+'\n')
        f_Cre.write(info_3.get()+'\n')
        f_Cre.close()
        f_Cre_1=open('access_2_cla_val.txt','w')
        f_Cre_1.write('Val\nVal\n')
        f_Cre_1.write(info_4.get()+'\n')
        f_Cre_1.write(info_5.get()+'\n')
        f_Cre_1.close()
        mydata_2['is_set_up']=True 
        with open("message.json", "w") as j:
            json.dump(mydata_2, j)   
        set_up_window.destroy()
    confirm=ttk.Button(set_up_window, text='Load', command=save_credentials)
    confirm.place(x=20, y=120)
    set_up_window.mainloop()


import twitter_analysis
import network_creation_analisis
import statistics


file_=open('user_stored','r').read().splitlines()

launch = tk.Tk()
launch.title('T.A.')
existint=ttk.Entry(launch, text='username')
existint.place(x=20, y=20)
def print_Statistics ():
    info, string = statistics.obtain_statistics()
    root = tk.Tk()
    text = tk.Text(root)
    text.insert(tk.INSERT, string)   
    text.place(x=20, y=20)
    root.mainloop() 
    #new['state']=tk.NORMAL
def load_graph ():
    network_creation_analisis.plot_Graph()
    #new['state']=tk.NORMAL
def options_vision ():
    options = tk.Tk()
    new=ttk.Button(options, text='Network', command = load_graph)
    new.place(x=20, y=20)
    load=ttk.Button(options, text='Statistics',command = print_Statistics)
    load.place(x=20, y=50)
    options.mainloop()
    #new['state']=tk.NORMAL
def load_data_extraction ():
    twitter_analysis.extract_info()
    options_vision()
def using_stored_info():
    def use_existint_info():
        select.destroy()
        options_vision()
    def update_info():
        select.destroy()
        load_data_extraction()
    select = tk.Tk()
    new=ttk.Button(select, text='Use stored information', command = use_existint_info)
    new.place(x=20, y=20)
    load=ttk.Button(select, text='Use new information',command = update_info)
    load.place(x=20, y=50)

def check_user ():
    #new['state']=tk.DISABLED
    with open("message.json", "r") as j:
        mydata = json.load(j) 
    value = existint.get()
    mydata["user"]=value
    with open("message.json", "w") as j:
        json.dump(mydata, j)   
    if (value in file_):
        print ('dentro')
        using_stored_info()
    else :
        load_data_extraction()
    print (value)
new = ttk.Button(launch, text='Create new profile', command=check_user)
new.place(x=20, y=50)
launch.mainloop()