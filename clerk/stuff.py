import os
import sys
sys.path.append(os.pardir)
import comutil
import menu

from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from functools import partial
import time
import threading

import socket
import pickle

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
    b2 = Button(sub_win, height=10, width=10, bg="#7FFFD4", text="座席 2", command=partial(sendSeatNum, 2))
    b4 = Button(sub_win, height=10, width=10, bg="#7FFFD4", text="座席 4", command=partial(sendSeatNum, 4))
    b6 = Button(sub_win, height=10, width=10, bg="#7FFFD4", text="座席 6", command=partial(sendSeatNum, 6))
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
    tree.insert(parent='', index='end', iid=id, values=(zaseki,name, num, cost))
    id += 1

def add_chicken(tree) :
    global id
    tree.insert(parent='', index='end', iid=id, values=(1,"からあげ", 3, 300))
    id += 1
def add_mame(tree) :
    global id
    tree.insert(parent='', index='end', iid=id, values=(1,"枝豆", 3, 300))
    id += 1

#
def Create_orderList() :
    #列の識別名を指定
    column = ("zaseki", "Name", "num", "cost")
    #メインウインドウの生成
    root = tk.Tk()
    root.title("オーダーリスト")
    root.geometry('400x500')

    #Notebookの作成（タブ管理）
    #notebook = ttk.Notebook(root)
    #orderTree = tk.Frame(root, bg = "white")
    #tab_waitingOrder = tk.Frame(notebook, bg="white")

    #notebookにタブを追加
    #notebook.add(tab_order, text ="order", underline=0)
    #notebook.add(tab_waitingOrder, text ="waiting", underline=0)

    #Treeviewの生成
    tree1 = ttk.Treeview(root, columns = column)
    #tree2 = ttk.Treeview(tab_waitingOrder, columns = column)
    #tab_waitingOrder = ttk.Treeview(root, columns = column)

    #列の設定
    tree1.column("#0", width=0, stretch="no")
    tree1.column('zaseki', anchor='center', width=80)
    tree1.column('Name',anchor='center', width=100)
    tree1.column('num', anchor='center', width=80)
    tree1.column('cost', anchor='center', width=80)
    # 列の見出し設定
    tree1.heading('#0',text='')
    tree1.heading('zaseki', text='座席番号',anchor='center')
    tree1.heading('Name', text='商品名', anchor='center')
    tree1.heading('num', text='個数',anchor='center')
    tree1.heading('cost',text='価格', anchor='center')
    # レコードの追加
    # tree1.insert(parent='', index='end', iid=0 ,values=(1, 'ビール', 1, 400))
    # tree1.insert(parent='', index='end', iid=1 ,values=(2,'からあげ', 2, 350))
    # tree1.insert(parent='', index='end', iid=2, values=(3,'枝豆', 1, 300))
    # tree1.insert(parent='', index='end', iid=3, values=(1,'からあげ', 2, 350))
    # tree1.insert(parent='', index='end', iid=4, values=(3,'ビール', 3, 400))

    # Buttonの生成
    #button = Button(root, text='Increment Price', command=partial(clear_order_fromFocus, tree1))
    button = Button(root, text='Served!', command=clear_order_fromFocus)
    #button_catchOrder = Button(root, text='catch_order', command=catch_order)
    b = Button(root, text="からあげ", command=partial(
        add_chicken, tree1
    ))
    b2 = Button(root, text="枝豆", command=partial(
        add_mame, tree1
    ))
    b3 = Button(root, text="enterShop", command=partial(
        sub_window, 3
    ))
    #button_changeWindow = Button(root, text='catch_window', command=change_window)
    # Styleの設定
    style = ttk.Style()
    style.theme_use("default")
    style.map("Treeview")
    # ウィジェットの配置
    #notebook.pack(expand=True, fill="both", padx=10, pady=10)
    tree1.pack(pady=10)
    #tree2.pack(pady=10)
    global tree
    tree = tree1

    button.pack()
    b.pack()
    b2.pack()
    b3.pack()
    #button_catchOrder.pack()

    root.mainloop()



#button_changeWindow.pack()
def main():
    global tree
    global clt
    thread1 = threading.Thread(target=Create_orderList)
    thread1.start()
    
    clt = Client('192.168.0.5',tree)
    clt.prepareSocket()
    clt.run()

    time.sleep(2)

    tree.focus_set()
    for i in range(3):
        time.sleep(1)
        print('オーダーします')
        unit = comutil.ComUnit(8 ,"192.168.0.5", i, i)
        clt.send(unit)



#注文を受信したらオーダーリストに追加
#catch_order(tree, 6, 1, "bi-ru", 2, 300)

class Client():
    def __init__(self, ip, tree):
        self.CLIENTIP = ip
        self.SERVERIP = '192.168.0.3'
        self.PORT = 334
        self.BUFFER_SIZE = 1024
        self.orderId = 0
        self.tree = tree
        self.iid = 5

    def prepareSocket(self):
        sock = socket.socket(socket.AF_INET)
        sock.connect((self.SERVERIP, self.PORT))
        self.sock = sock

    # データ受信関数
    def recvData(self):
        while True:
            try:
                data = self.sock.recv(self.BUFFER_SIZE)
                if data == b"":
                    break
                content = pickle.loads(data)
                print(f'new order({content.key}):', 'menu:', content.menuId, 'num:', content.num)
                menuId = content.menuId
                if content.mode == 8 :
                    m = menu.Menu()
                    name = m.getName(menuId)
                    price = m.getPrice(menuId)
                    *_, seatNum = content.sender.split('.')
                    seatNum = int(seatNum)/2
                    catch_order(tree, int(seatNum), name, content.num, price)
#                     iid += 1
                elif content.mode == 9 :
                    print('receive!!')
                    sub_window(content.num)
            except ConnectionResetError:
                break

        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        
    def run(self):
        # �f�[�^��M���T�u�X���b�h�Ŏ��s
        thread = threading.Thread(target=self.recvData)
        thread.start()

    def send(self, unit):
        # �f�[�^�����[�v
        try:
            unit.sender = self.CLIENTIP
            unit.key = self.orderId
            self.sock.send(pickle.dumps(unit))
            self.orderId += 1
        except ConnectionResetError:
            pass

    def disconnect(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


if __name__ == "__main__":
    main()
