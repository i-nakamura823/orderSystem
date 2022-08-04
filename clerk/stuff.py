import os
import sys
sys.path.append(os.pardir)
import comutil
import menu
import srvclt

from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from functools import partial

import threading


tree = ""
id = 0
subwindow = None
clt = None

def sendSeatNum(num):
    global subwindow
    global clt
    print(num)
    unit = comutil.ComUnit(10 ,"192.168.0.7", None, num)
    clt.send(unit)
    subwindow.destroy()

def sub_window(count):
    global subwindow
    sub_win = tk.Toplevel()
    subwindow = sub_win
    sub_win.geometry("420x200")
    sub_win.title("座席の指定")
    label_sub = tk.Label(sub_win, text = str(count) + "名様入店です", font=("","15","bold"))
    b2 = Button(sub_win, height=10, width=10, bg="#7FFFD4", text="座席 1", command=partial(sendSeatNum, 1))
    b4 = Button(sub_win, height=10, width=10, bg="#7FFFD4", text="座席 2", command=partial(sendSeatNum, 2))
    b6 = Button(sub_win, height=10, width=10, bg="#7FFFD4", text="座席 3", command=partial(sendSeatNum, 3))
    label_sub.pack()
    b2.pack(fill = 'x', padx=10, side = 'left')
    b4.pack(fill = 'x', padx=10, side = 'left')
    b6.pack(fill = 'x', padx=10, side = 'left')

#注文を提供したらオーダーリストから消す
def clear_order_fromFocus() :
    selected = tree.focus()
    temp = tree.item(selected, 'values')
    print(temp)
    tree.delete(selected)

#注文が届いたら新たに行を追加
def catch_order(tree, zaseki, name, num, cost) :
    global id
    # tree.insert(parent='', index='end', iid=id, values=(zaseki,name, num, cost))
    tree.insert(parent='', index='end', iid=id, values=(zaseki,name, num))
    id += 1

def Create_orderList() :
    #列の識別名を指定
    column = ("zaseki", "Name", "num", "cost")
    #メインウインドウの生成
    root = tk.Tk()
    root.title("オーダーリスト")
    root.geometry('300x500')

    #Treeviewの生成
    tree1 = ttk.Treeview(root, columns = column, height = 20)

    #列の設定
    tree1.column("#0", width=0, stretch="no")
    tree1.column('zaseki', anchor='center', width=89)
    tree1.column('Name',anchor='center', width=120)
    tree1.column('num', anchor='center', width=89)
    # 列の見出し設定
    tree1.heading('#0',text='')
    tree1.heading('zaseki', text='座席番号',anchor='center')
    tree1.heading('Name', text='商品名', anchor='center')
    tree1.heading('num', text='個数',anchor='center')

    # Buttonの生成
    button = Button(root, text='Served!', command=clear_order_fromFocus)
    # Styleの設定
    style = ttk.Style()
    style.theme_use("default")
    style.map("Treeview")
    # ウィジェットの配置
    tree1.pack(pady=10)
    global tree
    tree = tree1
    button.pack()
    root.mainloop()

def registerOrder(content):
    menuId = content.menuId
    if content.mode == 4 :
        m = menu.Menu()
        name = m.getName(menuId)
        price = m.getPrice(menuId)
        *_, seatNum = content.sender.split('.')
        seatNum = int(seatNum)/2
        catch_order(tree, int(seatNum), name, content.num, price)
    elif content.mode == 9 :
        print('receive!!')
        sub_window(content.num)

def main():
    global tree
    global clt
    thread1 = threading.Thread(target=Create_orderList)
    thread1.start()
    
    clt = srvclt.Client('192.168.0.5')
    clt.setMsgHandler(registerOrder)
    clt.prepareSocket()
    clt.run()

if __name__ == "__main__":
    main()
