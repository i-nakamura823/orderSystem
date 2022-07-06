import tkinter as tk
from tkinter import ttk
import threading
import time
from sense_hat import SenseHat
sense = SenseHat()
import comutil
import srvclt

def combo():

    root = tk.Tk()
    root.geometry('500x400')
    
    notebook = ttk.Notebook(root)
    tab_order = tk.Frame(notebook, bg = "white", takefocus = True)
    tab_atikyaku = tk.Frame(notebook, bg = "white")
    tab_mitsugi = tk.Frame(notebook, bg = "white")
    tab_kossori = tk.Frame(notebook, bg = "white")
    tab_megaphone = tk.Frame(notebook, bg = "white")
    

    mode = ('order', 'atikyaku', 'mitsugi', 'kossori', 'megaphone', 'check')
    menu = ('beer','karaage','edamame')
    num = ('1','2','3')
    seat_num = ('1','2','3','4')
    onedarilist_num = ('1','2','3','4','5','6','7','8','9','10')
    

    #v1 = tk.StringVar()
    global menu_selected
    global num_selected
    global seat_num_selected
    global onedarilist_num_selected
    global selectlist
    menu_selected = tk.StringVar()
    num_selected = tk.StringVar()
    seat_num_selected = tk.StringVar()
    onedarilist_num_selected = tk.StringVar()
    """
    selectlist[0] = menu_selected
    selectlist[1] = num_selected
    selectlist[2] = seat_num_selected
    selectlist[3] = onedarilist_num_selected
    """
    
    comboboxlist = []
    #combobox1 = ttk.Combobox(root, textvariable = v1, value = module1)
    #order
    mode_b_order = ttk.Button(tab_order, text = "mode change")
    menu_cb_order = ttk.Combobox(tab_order, textvariable = menu_selected, value = menu)
    num_cb_order = ttk.Combobox(tab_order, textvariable = num_selected, value = num)
    send_b_order = ttk.Button(tab_order, text = "send")
    check_b_order = ttk.Button(tab_order, text = "check")
    
    mode_b_order.bind("<Return>", lambda event:mb())
    send_b_order.bind("<Return>", lambda event:sb())
    
    #atikyaku
    mode_b_atikyaku = ttk.Button(tab_atikyaku, text = "mode change")
    menu_cb_atikyaku = ttk.Combobox(tab_atikyaku, textvariable = menu_selected, value = menu)
    num_cb_atikyaku = ttk.Combobox(tab_atikyaku, textvariable = num_selected, value = num)
    seat_num_cb_atikyaku = ttk.Combobox(tab_atikyaku, textvariable = seat_num_selected, value = seat_num)
    send_b_atikyaku = ttk.Button(tab_atikyaku, text = "send")
    check_b_atikyaku = ttk.Button(tab_atikyaku, text = "check")
    
    mode_b_atikyaku.bind("<Return>", lambda event:mb())
    send_b_atikyaku.bind("<Return>", lambda event:sb())
    
    #mitsugi
    mode_b_mitsugi = ttk.Button(tab_mitsugi, text = "mode change")
    onedarilist_num_cb_mitsugi = ttk.Combobox(tab_mitsugi, textvariable = onedarilist_num_selected, value = onedarilist_num)
    send_b_mitsugi = ttk.Button(tab_mitsugi, text = "send")
    check_b_mitsugi = ttk.Button(tab_mitsugi, text = "check")
    
    mode_b_mitsugi.bind("<Return>", lambda event:mb())
    send_b_mitsugi.bind("<Return>", lambda event:sb())
    
    #kossori
    mode_b_kossori = ttk.Button(tab_kossori, text = "mode change")
    menu_cb_kossori = ttk.Combobox(tab_kossori, textvariable = menu_selected, value = menu)
    num_cb_kossori = ttk.Combobox(tab_kossori, textvariable = num_selected, value = num)
    seat_num_cb_kossori = ttk.Combobox(tab_kossori, textvariable = seat_num_selected, value = seat_num)
    send_b_kossori = ttk.Button(tab_kossori, text = "send")
    check_b_kossori = ttk.Button(tab_kossori, text = "check")
    
    mode_b_kossori.bind("<Return>", lambda event:mb())
    send_b_kossori.bind("<Return>", lambda event:sb())
    
    #megaphone
    mode_b_megaphone = ttk.Button(tab_megaphone, text = "mode change")
    menu_cb_megaphone = ttk.Combobox(tab_megaphone, textvariable = menu_selected, value = menu)
    num_cb_megaphone = ttk.Combobox(tab_megaphone, textvariable = num_selected, value = num)
    send_b_megaphone = ttk.Button(tab_megaphone, text = "send")
    check_b_megaphone = ttk.Button(tab_megaphone, text = "check")
    
    mode_b_megaphone.bind("<Return>", lambda event:mb())
    send_b_megaphone.bind("<Return>", lambda event:sb())
    
    notebook.add(tab_order, text = "order", underline = 0)
    notebook.add(tab_atikyaku, text = "atikyaku", underline = 0)
    notebook.add(tab_mitsugi, text = "mitsugi", underline = 0)
    notebook.add(tab_kossori, text = "kossori", underline = 0)
    notebook.add(tab_megaphone, text = "megaphone", underline = 0)
    notebook.pack(expand = True, fill = "both", padx = 10, pady = 10)
    
    #combobox1.pack(pady = 10)
    #order
    mode_b_order.pack(pady = 10)
    menu_cb_order.pack(pady = 10)
    num_cb_order.pack(pady = 10)
    send_b_order.pack(pady = 10)
    check_b_order.pack(pady = 10)
    
    #atikyaku
    mode_b_atikyaku.pack(pady = 10)
    menu_cb_atikyaku.pack(pady = 10)
    num_cb_atikyaku.pack(pady = 10)
    seat_num_cb_atikyaku.pack(pady = 10)
    send_b_atikyaku.pack(pady = 10)
    check_b_atikyaku.pack(pady = 10)
    
    #mitsugi
    mode_b_mitsugi.pack(pady = 10)
    onedarilist_num_cb_mitsugi.pack(pady = 10)
    send_b_mitsugi.pack(pady = 10)
    check_b_mitsugi.pack(pady = 10)
    
    #kossori
    mode_b_kossori.pack(pady = 10)
    menu_cb_kossori.pack(pady = 10)
    num_cb_kossori.pack(pady = 10)
    seat_num_cb_kossori.pack(pady = 10)
    send_b_kossori.pack(pady = 10)
    check_b_kossori.pack(pady = 10)
    
    #megaphone
    mode_b_megaphone.pack(pady = 10)
    menu_cb_megaphone.pack(pady = 10)
    num_cb_megaphone.pack(pady = 10)
    send_b_megaphone.pack(pady = 10)
    check_b_megaphone.pack(pady = 10)
    
    global nb
    global to
    global ta
    global tmi
    global tko
    global tme
    nb = notebook
    to = tab_order
    ta = tab_atikyaku
    tmi = tab_mitsugi
    tko = tab_kossori
    tme = tab_megaphone
    global partlist
    global state
    #global part
    #global mode
    
    #order
    partlist[0][0] = mode_b_order
    partlist[0][1] = menu_cb_order
    partlist[0][2] = num_cb_order
    partlist[0][3] = send_b_order
    partlist[0][4] = check_b_order
    #atikyaku
    partlist[1][0] = mode_b_atikyaku
    partlist[1][1] = menu_cb_atikyaku
    partlist[1][2] = num_cb_atikyaku
    partlist[1][3] = seat_num_cb_atikyaku
    partlist[1][4] = send_b_atikyaku
    partlist[1][5] = check_b_atikyaku
    #mitsugi
    partlist[2][0] = mode_b_mitsugi
    partlist[2][1] = onedarilist_num_cb_mitsugi
    partlist[2][2] = send_b_mitsugi
    partlist[2][3] = check_b_mitsugi
    #kossori
    partlist[3][0] = mode_b_kossori
    partlist[3][1] = menu_cb_kossori
    partlist[3][2] = num_cb_kossori
    partlist[3][3] = seat_num_cb_kossori
    partlist[3][4] = send_b_kossori
    partlist[3][5] = check_b_kossori
    #megaphone
    partlist[4][0] = mode_b_megaphone
    partlist[4][1] = menu_cb_megaphone
    partlist[4][2] = num_cb_megaphone
    partlist[4][3] = send_b_megaphone
    partlist[4][4] = check_b_megaphone

    root.mainloop()
    
def mb():
    menu_selected.set("")
    num_selected.set("")
    seat_num_selected.set("")
    onedarilist_num_selected.set("")
    
def sb():
    if mode == 1 :
        mode_id = 0
    elif mode == 2:
        mode_id = 1
    elif mode == 3:
        mode_id = 2
    elif mode == 4:
        mode_id = 3
    menu_id = getMenuid()
    msg = comutil.ComUnit(mode_id, '192.168.0.6', menu_id, num_selected.get())
    clt = srvclt.Client('192.168.0.6')
    clt.prepareSocket()
    clt.run()
    clt.send(msg)
    
def getMenuid():
    if menu_selected.get() == "beer" :
        return 0
    elif menu_selected.get() == "karaage" :
        return 1
    elif menu_selected.get() == "edamame" :
        return 2
"""
def bo():
    nb.select(ta)
    mode = 1
    part = 0
    partlist[mode][part].focus_set()
    
def ba():
    nb.select(tmi)
    mode = 2
    part = 0
    partlist[mode][part].focus_set()
    
def bmi():
    nb.select(tko)
    mode = 3
    part = 0
    partlist[mode][part].focus_set()
    
def bko():
    nb.select(tme)
    mode = 4
    part = 0
    partlist[mode][part].focus_set()
    
def bme():
    nb.select(to)
    mode = 0
    part = 0
    partlist[mode][part].focus_set()
"""

nb = ""
to = ""
ta = ""
tmi = ""
tko = ""
tme = ""
menu_selected = ""
num_selected = ""
seat_num_selected = ""
onedarilist_num_selected = ""
#selectlist = [0 for i in range(4)]
partlist = [[0 for i in range(6)] for j in range(5)]
part = 0
global mode
mode = 0
thread1 = threading.Thread(target = combo)
thread1.start()
time.sleep(2)

#nb.select(tabo)
#tabo.focus_set()
partlist[0][0].focus_set()

while True :
    for event in sense.stick.get_events():
        if event.direction == "right" and event.action == "pressed":
            if part != 5 and partlist[mode][part + 1] != 0 :
                part = part + 1
                partlist[mode][part].focus_set()
            else :
                part = 0
                partlist[mode][part].focus_set()
                """
        if event.direction == "down" and event.action == "pressed":
            if part != 5 and partlist[mode][part + 1] != 0 :
                part = part + 1
                partlist[mode][part].focus_set()
            else :
                part = 0
                partlist[mode][part].focus_set()
                """
        elif event.direction == "left" and event.action == "pressed":
            if part != 0 :
                part = part - 1
                partlist[mode][part].focus_set()
            else :
                part = 5
                for k in range(5):
                    if partlist[mode][part] != 0:
                        break
                    part = part - 1
                partlist[mode][part].focus_set()
        elif event.direction == "middle" and event.action == "pressed" and part == 0 :
            if mode == 0 :
                nb.select(ta)
                mode = 1
                part = 0
                partlist[mode][part].focus_set()
            elif mode == 1 :
                nb.select(tmi)
                mode = 2
                part = 0
                partlist[mode][part].focus_set()
            elif mode == 2 :
                nb.select(tko)
                mode = 3
                part = 0
                partlist[mode][part].focus_set()
            elif mode == 3 :
                nb.select(tme)
                mode = 4
                part = 0
                partlist[mode][part].focus_set()
            elif mode == 4 :
                nb.select(to)
                mode = 0
                part = 0
                partlist[mode][part].focus_set()