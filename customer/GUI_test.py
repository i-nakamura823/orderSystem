import tkinter as tk
from tkinter import ttk
import threading
import time
from sense_hat import SenseHat
sense = SenseHat()
import os
import sys
sys.path.append(os.pardir)
import comutil
import srvclt
import copy

class Menu():
    def __init__(self):
        self.name = ['ビール', '唐揚げ', '枝豆']
        self.price = ['500', '600', '300']
        
    def getName(self, id):
        return self.name[id]
    
    def getPrice(self, id):
        return self.price[id]

class Sub_Window :
    def __init__(self, window, content, clt) : 
        self.window = window
        self.mode = content.mode
        self.content = copy.deepcopy(content)
        self.clt = clt
    
    def send_accept(self) :
        content = self.content
        content.mode = 4
        content.reciever = content.sender
        self.clt.send(content)

        content.reciever = "192.168.0.5"
        self.clt.send(content)

    def send_deny(self) :
        content = self.content
        content.mode = 5
        content.reciever = content.sender
        self.clt.send(content)

    def clear_window(self) :
        self.window.destroy()


def Create_sub_window(content) :
    #商品名を取得
    menu = Menu();
    menuName = menu.getName(int(content.menuId))

    #modeによってあちきゃく、こっそり、受理、拒否を判定
    if content.sender == clt.CLIENTIP:
        return
    if int(content.mode) == 0:
        result = "あちらのお客様からです"
    elif int(content.mode) == 2:
        result = "こっそりおねだり"
    elif int(content.mode) == 4 :
        result = "受理"
        for pastContent in clt.msglog.items() :
            if content.orderId == pastContent.orderId :
                if pastContent.mode == 2 or pastContent.mode == 3 :
                    check_value = check_value + (int(menu.getPrice(int(content.menuId))) * int(content.num)) * 0.7
    elif int(content.mode) == 5 :
        result = "拒否"
    

    #サブウインドウの生成
    sub_win = tk.Toplevel()
    sub_win.geometry("300x100")
    if int(content.mode) == 0 or int(content.mode) == 2:
        label_sub1 = tk.Label(sub_win, text=f"{result}")
        label_sub2 = tk.Label(sub_win, text=f"座席番号：{content.sender}　メニュー：{menuName}　個数：{content.num}")
        label_sub3 = tk.Label(sub_win, text=f"受理：↑")
        label_sub4 = tk.Label(sub_win, text=f"拒否：↓")
        label_sub1.pack()
        label_sub2.pack()
        label_sub3.pack()
        label_sub4.pack()
    elif int(content.mode) == 4 or int(content.mode) == 5:
        label_sub1 = tk.Label(sub_win, text=f"{content.sender}番さんが注文を{result}しました。")
        label_sub2 = tk.Label(sub_win, text=f"メニュー：{menuName}　個数：{content.num}")
        label_sub3 = tk.Label(sub_win, text=f"ウインドウを閉じる：↓")
        label_sub1.pack()
        label_sub2.pack()
        label_sub3.pack()
    sub_win.focus_set()

    #サブウインドウをリストに追加
    sub_windows.append(Sub_Window(sub_win, content, clt))

def combo():

    root = tk.Tk()
    root.geometry('700x600')
    
    notebook = ttk.Notebook(root)
    tab_order = tk.Frame(notebook, bg = "white")
    tab_atikyaku = tk.Frame(notebook, bg = "white")
    tab_mitsugi = tk.Frame(notebook, bg = "white")
    tab_kossori = tk.Frame(notebook, bg = "white")
    tab_megaphone = tk.Frame(notebook, bg = "white")
    

    menu = ('ビール','唐揚げ','枝豆')
    num = ('1','2','3')
    seat_num = ('1','2','3')
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
    
    #order
    mode_b_order = ttk.Button(tab_order, text = "モード変更")
    menu_label_order = ttk.Label(tab_order, text = "メニュー", background = "white")
    menu_cb_order = ttk.Combobox(tab_order, textvariable = menu_selected, value = menu)
    num_label_order = ttk.Label(tab_order, text = "個数", background = "white")
    num_cb_order = ttk.Combobox(tab_order, textvariable = num_selected, value = num)
    send_b_order = ttk.Button(tab_order, text = "送信")
    check_b_order = ttk.Button(tab_order, text = "会計")
    
    mode_b_order.bind("<Return>", lambda event:mb())
    send_b_order.bind("<Return>", lambda event:sb())
    check_b_order.bind("<Return>", lambda event:cb())
    
    #atikyaku
    mode_b_atikyaku = ttk.Button(tab_atikyaku, text = "モード変更")
    menu_label_atikyaku = ttk.Label(tab_atikyaku, text = "メニュー", background = "white")
    menu_cb_atikyaku = ttk.Combobox(tab_atikyaku, textvariable = menu_selected, value = menu)
    num_label_atikyaku = ttk.Label(tab_atikyaku, text = "個数", background = "white")
    num_cb_atikyaku = ttk.Combobox(tab_atikyaku, textvariable = num_selected, value = num)
    seat_num_label_atikyaku = ttk.Label(tab_atikyaku, text = "座席番号", background = "white")
    seat_num_cb_atikyaku = ttk.Combobox(tab_atikyaku, textvariable = seat_num_selected, value = seat_num)
    send_b_atikyaku = ttk.Button(tab_atikyaku, text = "送信")
    check_b_atikyaku = ttk.Button(tab_atikyaku, text = "会計")
    
    mode_b_atikyaku.bind("<Return>", lambda event:mb())
    send_b_atikyaku.bind("<Return>", lambda event:sb())
    check_b_atikyaku.bind("<Return>", lambda event:cb())
    
    #mitsugi
    mode_b_mitsugi = ttk.Button(tab_mitsugi, text = "モード変更")
    list_label_mitsugi = ttk.Label(tab_mitsugi, text = "おねだりリストの番号", background = "white")
    onedarilist_num_cb_mitsugi = ttk.Combobox(tab_mitsugi, textvariable = onedarilist_num_selected, value = onedarilist_num)
    send_b_mitsugi = ttk.Button(tab_mitsugi, text = "送信")
    check_b_mitsugi = ttk.Button(tab_mitsugi, text = "会計")
    
    mode_b_mitsugi.bind("<Return>", lambda event:mb())
    send_b_mitsugi.bind("<Return>", lambda event:sb())
    check_b_mitsugi.bind("<Return>", lambda event:cb())
    
    #kossori
    mode_b_kossori = ttk.Button(tab_kossori, text = "モード変更")
    menu_label_kossori = ttk.Label(tab_kossori, text = "メニュー", background = "white")
    menu_cb_kossori = ttk.Combobox(tab_kossori, textvariable = menu_selected, value = menu)
    num_label_kossori = ttk.Label(tab_kossori, text = "個数", background = "white")
    num_cb_kossori = ttk.Combobox(tab_kossori, textvariable = num_selected, value = num)
    seat_num_label_kossori = ttk.Label(tab_kossori, text = "座席番号", background = "white")
    seat_num_cb_kossori = ttk.Combobox(tab_kossori, textvariable = seat_num_selected, value = seat_num)
    send_b_kossori = ttk.Button(tab_kossori, text = "送信")
    check_b_kossori = ttk.Button(tab_kossori, text = "会計")
    
    mode_b_kossori.bind("<Return>", lambda event:mb())
    send_b_kossori.bind("<Return>", lambda event:sb())
    check_b_kossori.bind("<Return>", lambda event:cb())
    
    #megaphone
    mode_b_megaphone = ttk.Button(tab_megaphone, text = "モード変更")
    menu_label_megaphone = ttk.Label(tab_megaphone, text = "メニュー", background = "white")
    menu_cb_megaphone = ttk.Combobox(tab_megaphone, textvariable = menu_selected, value = menu)
    num_label_megaphone = ttk.Label(tab_megaphone, text = "個数", background = "white")
    num_cb_megaphone = ttk.Combobox(tab_megaphone, textvariable = num_selected, value = num)
    send_b_megaphone = ttk.Button(tab_megaphone, text = "送信")
    check_b_megaphone = ttk.Button(tab_megaphone, text = "会計")
    
    mode_b_megaphone.bind("<Return>", lambda event:mb())
    send_b_megaphone.bind("<Return>", lambda event:sb())
    check_b_megaphone.bind("<Return>", lambda event:cb())
    
    notebook.add(tab_order, text = "注文", underline = 0)
    notebook.add(tab_atikyaku, text = "あち客", underline = 0)
    notebook.add(tab_mitsugi, text = "みつぎ", underline = 0)
    notebook.add(tab_kossori, text = "こっそり", underline = 0)
    notebook.add(tab_megaphone, text = "メガホン", underline = 0)
    notebook.pack(expand = True, fill = "both", padx = 10, pady = 10)
    
    #combobox1.pack(pady = 10)
    #order
    mode_b_order.pack(pady = 10)
    menu_label_order.pack(pady = (10, 0))
    menu_cb_order.pack(pady = (0, 10))
    num_label_order.pack(pady = (10, 0))
    num_cb_order.pack(pady = (0, 10))
    send_b_order.pack(pady = 10)
    check_b_order.pack(pady = 10)
    
    #atikyaku
    mode_b_atikyaku.pack(pady = 10)
    menu_label_atikyaku.pack(pady = (10, 0))
    menu_cb_atikyaku.pack(pady = (0, 10))
    num_label_atikyaku.pack(pady = (10, 0))
    num_cb_atikyaku.pack(pady = (0, 10))
    seat_num_label_atikyaku.pack(pady = (10, 0))
    seat_num_cb_atikyaku.pack(pady = (0, 10))
    send_b_atikyaku.pack(pady = 10)
    check_b_atikyaku.pack(pady = 10)
    
    #mitsugi
    mode_b_mitsugi.pack(pady = 10)
    list_label_mitsugi.pack(pady = (10, 0))
    onedarilist_num_cb_mitsugi.pack(pady = (0, 10))
    send_b_mitsugi.pack(pady = 10)
    check_b_mitsugi.pack(pady = 10)
    
    #kossori
    mode_b_kossori.pack(pady = 10)
    menu_label_kossori.pack(pady = (10, 0))
    menu_cb_kossori.pack(pady = (0, 10))
    num_label_kossori.pack(pady = (10, 0))
    num_cb_kossori.pack(pady = (0, 10))
    seat_num_label_kossori.pack(pady = (10, 0))
    seat_num_cb_kossori.pack(pady = (0, 10))
    send_b_kossori.pack(pady = 10)
    check_b_kossori.pack(pady = 10)
    
    #megaphone
    mode_b_megaphone.pack(pady = 10)
    menu_label_megaphone.pack(pady = (10, 0))
    menu_cb_megaphone.pack(pady = (0, 10))
    num_label_megaphone.pack(pady = (10, 0))
    num_cb_megaphone.pack(pady = (0, 10))
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
    global clt
    global check_value
    menu = Menu()
    menu_id = 0
    menu_id = getMenuid()
    if mode == 0 :
        mode_id = 4
        seatIp = '192.168.0.5'
        check_value = check_value + (int(menu.getPrice(menu_id)) * int(num_selected.get()))
    elif mode == 1 :
        mode_id = 0
        seatIp = getIp(seat_num_selected.get())
    elif mode == 2:
        mode_id = 1
        menu_id = onedarilist_num_selected.get()
        seatIp = '192.168.0.1'
    elif mode == 3:
        mode_id = 2
        seatIp = getIp(seat_num_selected)
    elif mode == 4:
        mode_id = 3
        seatIp = '192.168.0.1'
    msg = comutil.ComUnit(mode_id, seatIp, menu_id, num_selected.get())
    clt.send(msg)

def cb() :
    global check_value
    menu_selected.set("")
    num_selected.set("")
    seat_num_selected.set("")
    onedarilist_num_selected.set("")
    check_win = tk.Toplevel()
    check_win.geometry("300x100")
    label_sub1 = tk.Label(check_win, text="お会計は")
    label_sub2 = tk.Label(check_win, text=f"{check_value}円です")
    label_sub3 = tk.Label(check_win, text="ウインドウを閉じる：↓")
    label_sub1.pack()
    label_sub2.pack()
    label_sub3.pack()
    check_win.focus_set()
    checkContent = comutil.ComUnit(6, '192.168.0.1', 0, 1)
    clt.send(checkContent)
    sub_windows.append(Sub_Window(check_win, checkContent, clt))
    check_value = 0
    
def getMenuid():
    if menu_selected.get() == "ビール" :
        return 0
    elif menu_selected.get() == "唐揚げ" :
        return 1
    elif menu_selected.get() == "枝豆" :
        return 2
    else :
        return 3
    
def getSeatid(ip):
    iptoseat = {"192.168.0.2":1, "192.168.0.4":2, "192.168.0.6":3}
    return iptoseat[ip]

def getIp(seatNum):
    iplist = ['192.168.0.2', '192.168.0.4', '192.168.0.6']
    return iplist[int(seatNum) - 1]
    
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
check_value = 0
sub_windows = []
clt = srvclt.Client('192.168.0.6')
clt.prepareSocket()
clt.run()
clt.msgHandler = Create_sub_window
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

        elif event.direction == "up" and event.action == "pressed" and sub_windows:
            current_window = sub_windows.pop(-1)
            if current_window.mode == 0 or current_window.mode == 2:
                current_window.clear_window()
                current_window.send_accept()
                
                #まだ生成中のサブウインドウがあるなら
                if sub_windows :
                    sub_windows[-1].window.focus_set()
                else:
                    partlist[mode][part].focus_set()

        elif event.direction == "down" and event.action == "pressed" and sub_windows:
            current_window = sub_windows.pop(-1)
            if current_window.mode == 0 or current_window.mode == 2:
                current_window.send_deny()
            current_window.clear_window()
            #まだ生成中のサブウインドウがあるなら
            if sub_windows:
                sub_windows[-1].window.focus_set()
            else:
                partlist[mode][part].focus_set()

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